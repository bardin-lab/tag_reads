import os
import subprocess
import tempfile
from collections import OrderedDict
from functools import partial

from concurrent.futures import ThreadPoolExecutor
from BCBio import GFF
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, FeatureLocation


def write_cluster(clusters, header, output_path, sample='sample', threads=1):
    """Write clusters as GFF entries."""
    with open(output_path, "w") as out_handle:
        tp = ThreadPoolExecutor(threads)
        futures = []
        records = OrderedDict((tid, SeqRecord(Seq(""), sn)) for tid, sn in enumerate(header.references))
        for i, cluster in enumerate(clusters):
            if not cluster.exclude:
                func = partial(get_feature, cluster, sample, i)
                futures.append(tp.submit(func))
        for future in futures:
            tid, feature = future.result()
            records[tid].features.append(feature)
        GFF.write(records.values(), out_handle)
        tp.shutdown(wait=True)


def get_feature(cluster, sample, i):
    """Turn a cluster into a biopython SeqFeature."""
    qualifiers = OrderedDict(ID="%s_%d" % (sample, i))
    for attr in cluster.exportable:
        qualifiers[attr] = getattr(cluster, attr.lower())
    feature = SeqFeature(FeatureLocation(cluster.start, cluster.end), type=cluster.type, strand=1, qualifiers=qualifiers)
    if cluster.feature_args:
        seqfeature_args = cluster.feature_args
        base_args = {'location': FeatureLocation(cluster.start, cluster.end), 'strand': 1}
        subfeatures = []
        for feature_args in seqfeature_args:
            feature_args = feature_args.to_feature_args()
            args = base_args.copy()
            args.update(feature_args)
            subfeatures.append(SeqFeature(**args))
        feature.sub_features = subfeatures
    return cluster.tid, feature


def sort_gff(input_path, output_path):
    """Sort gff file at input path."""
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(output_path))
    header_lines = []
    with open(input_path) as gff_in, open(tmp, 'w') as out:
        for line in gff_in:
            if line.startswith('#'):
                header_lines.append(line)
            else:
                out.write(line)
        out.close()
    with open(output_path, 'w') as out:
        p = subprocess.Popen(['sort', '-k', '1,1', '-k4,4n', tmp], stdout=subprocess.PIPE, close_fds=True)
        out.write("\n".join(header_lines))
        for line in p.stdout:
            out.write(line.decode())
    os.close(fd)
