import argparse

import pysam
import six

from contextlib2 import ExitStack

from .cigar import alternative_alignment_cigar_is_better, cigartuples_to_cigarstring
from .io import (
    BamAlignmentWriter as Writer,
    BamAlignmentReader as Reader,
)


TAG_TEMPLATE = "R:{ref:s},POS:{pos:d},QSTART:{qstart:d},QEND:{qend:d},CIGAR:{cigar:s},S:{sense:s},MQ:{mq:d}"


class SamTagProcessor(object):

    tag_template = TAG_TEMPLATE

    def __init__(self, source_path, tag_prefix_self, tag_prefix_mate, tag_mate=True):
        self.tag_mate = tag_mate
        self.tag_prefix_self = tag_prefix_self
        self.tag_prefix_mate = tag_prefix_mate
        self.detail_tag_self = tag_prefix_self + 'D'
        self.detail_tag_mate = tag_prefix_mate + 'D'
        self.reference_tag_self = tag_prefix_self + 'R'
        self.reference_tag_mate = tag_prefix_mate + 'R'
        self.source_alignment = pysam.AlignmentFile(source_path)
        self.tid_to_reference_name = {self.source_alignment.get_tid(rname):rname for rname in (d['SN'] for d in self.source_alignment.header['SQ'])}
        self.source_path = source_path
        self.result = self.process_source()
        if self.tag_mate:
            self.add_mate()

    def compute_tag(self, r):
        """
        Adds tags for downstream processing:
            - Reference
            - Pos
            - Sense
            - Aligned position
            - MD
        Returns a tag of the form:
        [('AA'), ('R:gypsy,POS:1,MD:107S35M,S:AS')]
        'AA' stands for alternative alignment,
        'MA' stands for mate alignment.
        :param r: AlignedSegment
        """
        tags = (r.tid,
                r.reference_start,
                r.cigar,
                r.is_reverse,
                r.mapping_quality,
                r.qstart,
                r.qend)
        return tags

    def is_taggable(self, r):
        """
        Decide if a read should be tagged
        :param r: AlignedSegment
        :type r: pysam.Alignedread
        """
        return not r.is_unmapped and not r.is_secondary and not r.is_supplementary and not r.is_qcfail

    def process_source(self):
        tag_d = {}
        with Reader(self.source_path) as source_alignment:
            for r in source_alignment:
                if self.is_taggable(r):
                    if r.query_name in tag_d:
                        tag_d[r.query_name][r.is_read1] = {'s': self.compute_tag(r)}
                    else:
                        tag_d[r.query_name] = {r.is_read1: {'s': self.compute_tag(r)}}
        return tag_d

    def add_mate(self):
        for tag_d in six.itervalues(self.result):
            for k, v in tag_d.items():
                if (not k) in tag_d:
                    v['m'] = tag_d[(not k)]['s']

    def format_tag_value(self, t):
        """
        :param t:
        :return:
        >>> t = (0, 362603, [(4, 2), (0, 37)], False, 4, 0, 37)
        """
        d = dict(ref=self.tid_to_reference_name[t[0]], pos=t[1], cigar=cigartuples_to_cigarstring(t[2]), sense='AS' if t[3] else 'S', mq=t[4], qstart=t[5], qend=t[6])
        return self.tag_template.format(**d)

    def format_tags(self, tags):
        """
        >>> tags = {'m': (0, 362603, [(4, 2), (0, 37)], False, 4, 0, 37)}
        """
        formatted_tags = []
        for k, v in tags.items():
            if k == 's':
                formatted_tags.append((self.detail_tag_self, self.format_tag_value(v)))
                formatted_tags.append((self.reference_tag_self, self.tid_to_reference_name[v[0]]))
            else:
                formatted_tags.append((self.detail_tag_mate, self.format_tag_value(v)))
                formatted_tags.append(((self.reference_tag_mate, self.tid_to_reference_name[v[0]])))
        return formatted_tags

    def get_other_tag(self, other_r):
        """
        convenience method that takes a read object `other_r` and fetches the
        annotation tag that has been processed in the instance
        """
        other_r_reverse = other_r.is_read1
        tagged_mates = self.result.get(other_r.query_name)
        if tagged_mates:
            return tagged_mates.get(other_r_reverse, None)
        else:
            return None

class SamAnnotator(object):

    def __init__(self,
                 annotate_file,
                 samtags,
                 output_path="test.bam",
                 allow_dovetailing=False,
                 discard_bad_alt_tag=True,
                 discarded_writer=None,
                 verified_writer=None):
        """
        Compare `samtags` with `annotate_file`.
        Produces a new alignment file at output_path.
        :param annotate_file: 'Path to bam/sam file'
        :type annotate_file: str
        :param samtags: list of SamTagProcessor instances
        :type samtags: List[SamTagProcessor]
        :param allow_dovetailing: Controls whether or not dovetailing should be allowed
        :type allow_dovetailing: bool
        """
        self.annotate_file = annotate_file
        self.output_path = output_path
        self.samtags = samtags
        self.detail_tag_self = self.samtags[0].detail_tag_self  # urgs ... probably bad design here :(.
        self.detail_tag_mate = self.samtags[0].detail_tag_mate
        self.reference_tag_self = self.samtags[0].reference_tag_self
        self.reference_tag_mate = self.samtags[0].reference_tag_mate
        self.template = pysam.AlignmentFile(annotate_file).header
        if allow_dovetailing:
            self.max_proper_size = self.get_max_proper_pair_size(pysam.AlignmentFile(annotate_file))
            if not self.max_proper_size:
                allow_dovetailing = False
        self.process(allow_dovetailing, discard_bad_alt_tag, discarded_writer, verified_writer)


    def process(self, allow_dovetailing=False, discard_bad_alt_tag=True, discarded_writer=None, verified_writer=None):
        kwds = {'reader': {Reader: {'path': self.annotate_file}},
                'main_writer': {Writer: { 'path': self.output_path, 'header': self.template}},
                'discarded_writer': {Writer: { 'path': discarded_writer, 'header': self.template}},
                'verified_writer': {Writer: {'path': verified_writer, 'header': self.template}}}
        args = {'allow_dovetailing': allow_dovetailing,
                'discard_bad_alt_tag': discard_bad_alt_tag}
        with ExitStack() as stack:
            for arg, cls_arg_d in kwds.items():
                for cls, cls_args in cls_arg_d.items():
                    if cls_args['path']:
                        args[arg] = stack.enter_context(cls(**cls_args))
                    else:
                        args[arg] = None
            self._process(**args)

    def _process(self, reader, main_writer, discarded_writer=None, verified_writer=None, allow_dovetailing=False, discard_bad_alt_tag=True):
        for read in reader:
            discarded_tags = []
            verified_tags = []
            for samtag in self.samtags:
                alt_tag = samtag.get_other_tag(read)
                if alt_tag and discard_bad_alt_tag:
                    verified_tag = self.verify_alt_tag(read, alt_tag)
                    if discarded_writer and len(verified_tag) < len(alt_tag):
                        discarded_tag = samtag.format_tags({k: v for k, v in alt_tag.items() if k not in verified_tag})
                        discarded_tags.extend(discarded_tag)
                    alt_tag = verified_tag
                if alt_tag:
                    verified_tag = samtag.format_tags(alt_tag)
                    verified_tags.extend(verified_tag)
            if allow_dovetailing:
                read = self.allow_dovetailing(read, self.max_proper_size)
            if discarded_tags:
                discarded_read = read.__copy__()
                discarded_read.tags += discarded_tags
                discarded_writer.write(discarded_read)
            if verified_tags:
                read.tags += verified_tags
                if verified_writer:
                    verified_writer.write(read)
            main_writer.write(read)

    def verify_alt_tag(self, read, alt_tag):
        """
        Take a read and verify that the alternative tags are really better
        :param read: A pysam read
        :type read: pysam.AlignedRead
        :return: read
        :type read: pysam.AlignedRead
        """
        # TODO: Make this available as a standalone function by explcitly passing in the tags to look at
        if read.is_unmapped:
            return read
        tags_to_check = ((v, 's', read.cigar) if k == 's' else (v, 'm', read.get_tag('MC')) if read.has_tag('MC') else (None, None, None) for k, v in alt_tag.items())
        verified_alt_tag = {}
        for (alt_tag, s_or_m, cigar) in tags_to_check:
            if cigar:
                # Can only check if read has cigar/alt_cigar
                alt_is_reverse = alt_tag[3]
                same_orientation = alt_is_reverse == (read.is_reverse if s_or_m == 's' else read.mate_is_reverse)
                keep = alternative_alignment_cigar_is_better(current_cigar=cigar,
                                                             alternative_cigar=alt_tag[2],
                                                             same_orientation=same_orientation)
                if keep:
                    verified_alt_tag[s_or_m] = alt_tag
        return verified_alt_tag


    @classmethod
    def get_max_proper_pair_size(cls, alignment_file):
        """
        iterate over the first 1000 properly paired records in alignment_file
        and get the maximum valid isize for a proper pair.
        :param alignment_file: pysam.AlignmentFile
        :type alignment_file: pysam.AlignmentFile
        :rtype int
        """
        isize = []
        for r in alignment_file:
            if r.is_proper_pair and not r.is_secondary and not r.is_supplementary:
                isize.append(abs(r.isize))
            if len(isize) == 1000:
                alignment_file.reset()
                return max(isize)
        alignment_file.reset()
        if isize:
            return max(isize)
        else:
            return None

    @classmethod
    def allow_dovetailing(cls, read, max_proper_size=351):
        """
        Manipulates is_proper_pair tag to allow dovetailing of reads.
        Precondition is read and mate have the same reference id, are within the maximum proper pair distance
        and are either in FR or RF orientation.
        :param read: aligned segment of pysam.AlignmentFile
        :type read: pysam.AlignedSegment
        :rtype pysam.AlignedSegment
        """
        if not read.is_proper_pair and not read.is_reverse == read.mate_is_reverse and read.reference_id == read.mrnm and abs(read.isize) <= max_proper_size:
            read.is_proper_pair = True
        return read


def parse_file_tags(filetags):
    """
    :param filetags: string with filepath.
                     optionally appended by the first letter that should be used for read and mate
    :return: annotate_with, tag_prefix, tag_prefix_mate

    >>> filetags = ['file_a:A:B', 'file_b:C:D', 'file_c']
    >>> annotate_with, tag_prefix, tag_prefix_mate = parse_file_tags(filetags)
    >>> annotate_with == ['file_a', 'file_b', 'file_c'] and tag_prefix == ['A', 'C', 'A'] and tag_prefix_mate == ['B', 'D', 'B']
    True
    >>>
    """
    annotate_with = []
    tag_prefix = []
    tag_prefix_mate = []
    for filetag in filetags:
        if ':' in filetag:
            filepath, tag, tag_mate = filetag.split(':')
            annotate_with.append(filepath)
            tag_prefix.append(tag.upper())
            tag_prefix_mate.append(tag_mate.upper())
        else:
            annotate_with.append(filetag)
            tag_prefix.append('A')  # Default is A for read, B for mate
            tag_prefix_mate.append('B')
    return annotate_with, tag_prefix, tag_prefix_mate


def parse_args():
    p = argparse.ArgumentParser(description="Tag reads in an alignment file based on other alignment files",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('-t', '--tag_file', help="Tag reads in this file.", required=True)
    p.add_argument('-a', '--annotate_with',
                   help="Tag reads in readfile if reads are aligned in these files."
                        "Append `:A:B` to tag first letter of tag describing read as A, "
                        "and first letter of tag describing the mate as B",
                   nargs = "+",
                   required=True)
    p.add_argument('-o', '--output_file', help="Write bam file to this path", required=True)
    p.add_argument('-d', '--allow_dovetailing',
                   action='store_true',
                   help="Sets the proper pair flag (0x0002) to true if reads dovetail [reads reach into or surpass the mate sequence].")
    p.add_argument('-k', '--keep_suboptimal_alternate_tags', action='store_true',
                   help="By default cigar strings of the alternative tags are compared and alternates that are not explaining the current cigar strings are discarded."
                        "Use this option to keep the alternative tags (effectively restoring the behaviour of tag_reads < 0.1.4)")
    p.add_argument('-wd', '--write_discarded', default=False, required=False, help="Write discarded reads into separate file")
    p.add_argument('-wv', '--write_verified', default=False, required=False,
                   help="Write verified reads into separate file")
    return p.parse_args()

def main():
    args = parse_args()
    files_tags = zip(*parse_file_tags(args.annotate_with))
    samtags = [SamTagProcessor(filepath, tag_prefix_self=tag, tag_prefix_mate=tag_mate) for (filepath, tag, tag_mate) in files_tags ]
    SamAnnotator(annotate_file=args.tag_file,
                 samtags=samtags,
                 output_path=args.output_file,
                 allow_dovetailing=args.allow_dovetailing,
                 discard_bad_alt_tag=not args.keep_suboptimal_alternate_tags,
                 discarded_writer=args.write_discarded,
                 verified_writer=args.write_verified)

if __name__ == "__main__":
    main()