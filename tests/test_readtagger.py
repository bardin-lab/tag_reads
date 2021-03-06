from readtagger.readtagger import (
    SamTagProcessor,
    SamAnnotator,
    TagManager,
)
from readtagger.cli.readtagger_cli import readtagger
from readtagger.bam_io import (
    BamAlignmentReader as Reader,
    BamAlignmentWriter as Writer,
)
from .helpers import (  # noqa: F401
    namedtuple_to_argv,
    reference_fasta
)

import pysam
from collections import namedtuple

TEST_SAM = 'testsam_a.sam'
TEST_SAM_B = 'testsam_b.sam'
TEST_BAM_A = 'dm6.bam'
TEST_BAM_B = 'pasteurianus.bam'
TEST_SAM_ROVER_DM6 = 'rover_single_mate_dm6.sam'
TEST_SAM_ROVER_FBTI = 'rover_single_mate_fbti.sam'
EXTENDED_QUERYNAME = 'extended_and_annotated_roi.bam'

ARGS_TEMPLATE = namedtuple('args', ['source_paths',
                                    'target_path',
                                    'reference_fasta',
                                    'allow_dovetailing',
                                    'discard_suboptimal_alternate_tags',
                                    'discard_if_proper_pair',
                                    'discarded_path',
                                    'verified_path',
                                    'output_path',
                                    'cores'])


def test_samtag_processor(datadir_copy):  # noqa: D103
    # test that tag_mate=False really skips tagging mates
    p_mate_false = get_samtag_processor(datadir_copy, tag_mate=False)
    for qname, tag_d in p_mate_false.result.items():
        assert qname == 'DISCARD_R1_KEEP_R2:1'
        assert len(tag_d) == 1
    p_mate_true = get_samtag_processor(datadir_copy, tag_mate=True)
    # Make sure that the mate gets tagged as well
    for qname, tag_d in p_mate_true.result.items():
        assert len(tag_d) == 2
        # Need some more data to make more meaningful tests


def test_samtag_annotator(datadir_copy, tmpdir):  # noqa: D103
    p = get_samtag_processor(datadir_copy, tag_mate=True)
    output_path = tmpdir.join('testout.bam')
    with Reader(str(datadir_copy[TEST_SAM_B]), sort_order='queryname') as annotate_bam:
        header = annotate_bam.header
        annotate_reads = [r for r in annotate_bam]
    with Writer(output_path.strpath, header=header) as output_writer:
        a = SamAnnotator(samtag_instances=[p],
                         annotate_bam=annotate_reads,
                         output_writer=output_writer,
                         allow_dovetailing=False,
                         discard_suboptimal_alternate_tags=True, )
        assert isinstance(a, SamAnnotator)
    output_path.check()


def test_main_keep_suboptimal(datadir_copy, tmpdir):  # noqa: D103
    # Annotate dm6 with pasteurianus reads, keep suboptimal tags
    discarded, verified, output = get_output_files(tmpdir)
    source_paths = [str(datadir_copy[TEST_BAM_B])]
    target_path = str(datadir_copy[TEST_BAM_A])
    TagManager(source_paths=source_paths, target_path=target_path, reference_fasta=None, allow_dovetailing=True, discard_suboptimal_alternate_tags=True,
               discard_if_proper_pair=False, output_path=output.strpath, discarded_path=discarded.strpath, verified_path=verified.strpath,
               cores=1)


def test_multicore(datadir_copy, tmpdir):  # noqa: D103
    # Annotate dm6 with pasteurianus reads, keep suboptimal tags
    discarded, verified, output = get_output_files(tmpdir)
    source_paths = [str(datadir_copy[TEST_BAM_B])]
    target_path = str(datadir_copy[TEST_BAM_A])
    TagManager(source_paths=source_paths, target_path=target_path, reference_fasta=None, allow_dovetailing=True, discard_suboptimal_alternate_tags=True,
               discard_if_proper_pair=False, output_path=output.strpath, discarded_path=discarded.strpath, verified_path=verified.strpath,
               cores=2)


def test_main_discard_suboptimal(datadir_copy, tmpdir):  # noqa: D103
    # Annotate dm6 with pasteurianus reads, keep suboptimal tags
    discarded, verified, output = get_output_files(tmpdir)
    source_paths = [str(datadir_copy[TEST_BAM_B])]
    target_path = str(datadir_copy[TEST_BAM_A])
    TagManager(source_paths=source_paths, target_path=target_path, reference_fasta=None, allow_dovetailing=True, discard_suboptimal_alternate_tags=False,
               discard_if_proper_pair=False, output_path=output.strpath, discarded_path=discarded.strpath, verified_path=verified.strpath,
               cores=1)


def test_main_discard_suboptimal_discard_if_proper(datadir_copy, tmpdir):  # noqa: D103
    # Annotate dm6 with pasteurianus reads, keep suboptimal tags, discard proper pairs
    discarded, verified, output = get_output_files(tmpdir)
    source_paths = [str(datadir_copy[TEST_BAM_B])]
    target_path = str(datadir_copy[TEST_BAM_A])
    TagManager(source_paths=source_paths, target_path=target_path, reference_fasta=None, allow_dovetailing=True, discard_suboptimal_alternate_tags=False,
               discard_if_proper_pair=True, output_path=output.strpath, discarded_path=discarded.strpath, verified_path=verified.strpath,
               cores=1)


def test_main_with_argparse(datadir_copy, tmpdir, mocker):  # noqa: D103
    # Annotate dm6 with pasteurianus reads, keep suboptimal tags, discard proper pairs
    # and test that argparse argument parsing works as expected.
    discarded, verified, output = get_output_files(tmpdir)
    source_paths = [str(datadir_copy[TEST_BAM_B])]
    target_path = str(datadir_copy[TEST_BAM_A])
    args = ARGS_TEMPLATE(source_paths=source_paths, target_path=target_path, reference_fasta=None, allow_dovetailing=True,
                         discard_suboptimal_alternate_tags=False,
                         discard_if_proper_pair=True, output_path=output.strpath, discarded_path=discarded.strpath, verified_path=verified.strpath,
                         cores='1')
    argv = namedtuple_to_argv(args, 'readtagger.py')
    mocker.patch('sys.argv', argv)
    try:
        readtagger()
    except SystemExit:
        pass


def test_main_rover(datadir_copy, tmpdir, mocker, reference_fasta):  # noqa: D103, F811
    discarded, verified, output = get_output_files(tmpdir)
    source_paths = [str(datadir_copy[TEST_SAM_ROVER_FBTI])]
    target_path = str(datadir_copy[TEST_SAM_ROVER_DM6])
    args = ARGS_TEMPLATE(source_paths=source_paths, target_path=target_path, allow_dovetailing=True, discard_suboptimal_alternate_tags=False,
                         reference_fasta=None, discard_if_proper_pair=True, output_path=output.strpath,
                         discarded_path=discarded.strpath, verified_path=verified.strpath, cores='1')
    argv = namedtuple_to_argv(args, 'readtagger.py')
    mocker.patch('sys.argv', argv)
    try:
        readtagger()
    except SystemExit:
        pass
    assert len([r for r in pysam.AlignmentFile(verified.strpath)]) == 0  # 1 if discard_suboptimal_alternate_tags is really False, but difficult to test ...
    # Now test with 2 cores
    args = ARGS_TEMPLATE(source_paths=source_paths, target_path=target_path, reference_fasta=None, allow_dovetailing=True,
                         discard_suboptimal_alternate_tags=False,
                         discard_if_proper_pair=True, output_path=output.strpath, discarded_path=discarded.strpath, verified_path=verified.strpath,
                         cores='2')
    argv = namedtuple_to_argv(args, 'readtagger.py')
    mocker.patch('sys.argv', argv)
    try:
        readtagger()
    except SystemExit:
        pass
    assert len([r for r in pysam.AlignmentFile(verified.strpath)]) == 0  # 1 if discard_suboptimal_alternate_tags is really False, but difficult to test ...


def test_tag_manager_small_chunks(datadir_copy, tmpdir, reference_fasta):  # noqa: D103, F811
    discarded, verified, output = get_output_files(tmpdir)
    source_paths = [str(datadir_copy[EXTENDED_QUERYNAME])]
    target_path = str(datadir_copy[EXTENDED_QUERYNAME])
    args = {'source_paths': source_paths,
            'target_path': target_path,
            'output_path': output.strpath,
            'discarded_path': discarded.strpath,
            'verified_path': verified.strpath,
            'reference_fasta': reference_fasta,
            'discard_suboptimal_alternate_tags': False,
            'tag_mate': True,
            'allow_dovetailing': True,
            'cores': 1,
            'chunk_size': 10}
    TagManager(**args)
    assert len([r for r in pysam.AlignmentFile(verified.strpath)]) == 39


def test_tag_manager_big_chunks(datadir_copy, tmpdir):  # noqa: D103
    discarded, verified, output = get_output_files(tmpdir)
    source_paths = [str(datadir_copy[EXTENDED_QUERYNAME])]
    target_path = str(datadir_copy[EXTENDED_QUERYNAME])
    args = {'source_paths': source_paths,
            'target_path': target_path,
            'output_path': output.strpath,
            'discarded_path': discarded.strpath,
            'verified_path': verified.strpath,
            'discard_suboptimal_alternate_tags': False,
            'tag_mate': True,
            'allow_dovetailing': True,
            'cores': 1,
            'chunk_size': 1000}
    TagManager(**args)
    assert len([r for r in pysam.AlignmentFile(verified.strpath)]) == 39


def get_samtag_processor(datadir_copy, tag_mate):  # noqa: D103
    source_paths = str(datadir_copy[TEST_SAM])
    header = pysam.AlignmentFile(source_paths).header
    return SamTagProcessor(Reader(source_paths, sort_order='queryname').__enter__(), header=header, tag_mate=tag_mate)


def get_output_files(tmpdir):  # noqa: D103
    return tmpdir.join('discarded.bam'), tmpdir.join('verified.bam'), tmpdir.join('output.bam')
