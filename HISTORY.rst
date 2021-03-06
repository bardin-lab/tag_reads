.. :changelog:

History
-------

.. to_doc

---------------------
0.5.24 (2020-04-07)
---------------------
Various updates to plot_coverage tool

---------------------
0.5.23 (2020-03-23)
---------------------
Release a non-broken version, (conda-build problem in 0.5.22)

---------------------
0.5.22 (2020-03-23)
---------------------
Allow one or more alignment files in plot_coverage tool

---------------------
0.5.21 (2020-01-12)
---------------------
Make normalize_readsizes more efficient (again)

---------------------
0.5.20 (2020-01-11)
---------------------
Make normalize_readsizes more efficient for large datasets

---------------------
0.5.19 (2020-01-11)
---------------------
Fix file opening in normalize_readsizes

---------------------
0.5.18 (2019-12-18)
---------------------
Drop recursion from normalize_readsizes, didn't seem to work

---------------------
0.5.17 (2019-11-05)
---------------------
Add summarize_fragments command
Normalize length of multiple long read fastq files
Update dependencies

---------------------
0.5.16 (2019-09-05)
---------------------
Annotate clusters that are composed exclusively of proper pairs

---------------------
0.5.15 (2019-09-04)
---------------------
Relax cluster merging requirement

---------------------
0.5.14 (2019-09-03)
---------------------
Allow 15 instead of 10 nt between split and TE start

---------------------
0.5.13 (2019-09-03)
---------------------
Fix aligned_segment_corresponds_to_transposable_element

---------------------
0.5.12 (2019-09-02)
---------------------
Write fasta and re-align with bwa after last join_clusters
Test and fix TE overlap annotation

---------------------
0.5.11 (2019-09-01)
---------------------
Annotate overlaps of insertions of the same kind

---------------------
0.5.10 (2019-09-01)
---------------------
Write out matching softclip cluster

---------------------
0.5.9 (2019-08-31)
---------------------
Fix crash when corrected start/end can't be calculated.

---------------------
0.5.8 (2019-08-31)
---------------------
Improve joining of clusters

---------------------
0.5.7 (2019-08-29)
---------------------
Don't mark clusters incompatible after splitting them out from original cluster
Use corrected or uncorrected start/end when finding reachable clusters
Also allow joining with downstream reverse cluster
Detect local maximum proper pair size

---------------------
0.5.6 (2019-08-28)
---------------------
Always produce contig fasta, required for refining cluster positions
Allow +/- 10 nucleotides between alignment and insert start/end

---------------------
0.5.5 (2019-08-27)
---------------------
* Add timeout to cap3 call
* Update dependencies

---------------------
0.5.4 (2019-07-29)
---------------------
* Bump pysam dependency to 0.15.3, contains important fixes

---------------------
0.5.3 (2019-07-28)
---------------------
* Sort 'extract_variants' output alignment

---------------------
0.5.2 (2019-07-28)
---------------------
* Add 'extract_variants' tool for extracting insertion evidence from long reads

---------------------
0.5.1 (2019-06-13)
---------------------
* Only associate clipping pattern with insertion if pattern matches breakpoint sequence

---------------------
0.5.0 (2019-06-12)
---------------------
* Drop support for Python 2

---------------------
0.4.20 (2019-06-12)
---------------------
* Keep all associated softclip patterns when merging adjacent read clusters

---------------------
0.4.19 (2019-02-15)
---------------------
* Fix findcluster crash when reference contains colon.

---------------------
0.4.18 (2019-02-14)
---------------------
* Use logger.warning instead of deprecated logger.warn
* Drop now unused qname_cmp_func
* Fix alignment splitting, fixes untagged reads and speed issues

---------------------
0.4.17 (2019-02-10)
---------------------
* Fix a bug that would lead to wrong chunk sizes

---------------------
0.4.16 (2019-01-28)
---------------------
* Drop samtools, do everything via pysam

---------------------
0.4.15 (2019-01-15)
---------------------
* Add missing samtools dependency

---------------------
0.4.14 (2019-01-15)
---------------------
* Build Conda package for python 3 only

---------------------
0.4.13 (2019-01-14)
---------------------
* Update pinned dependencies
* Fix travis deployment

---------------------
0.4.12 (2018-08-21)
---------------------
* Allow multiple inputs to readtagger
* Allow passing multiple control files to confirm_insertions script
* Fix matching of short 3p clipped sequences

---------------------
0.4.11 (2018-05-18)
---------------------
* Add a script that merges findlcuster VCF output
* Allow 5 nt overlaps at cluster consistency check
* Include VALID_TSD in INFO field and write out PE support
* Sort output VCF file
* Generate IDs using reference_name start and cluster order
* Improve support for arbitrary insertion names

---------------------
0.4.10 (2018-03-30)
---------------------
* Include unmapped but tagged mates in veriefied tags
* Update findcluster galaxy tool and fix softclip cluster ids
* Use a unique ID as variant ID
* Stop collection evidence once we reach 10000 reads
* Speed up finding of soft clip clusters
* Implement VCF output
* Make loglevel configurable for findcluster script and add option to output log to file
* Look for softclipped reads in a 15nt window and compare 5p clips by their end
* Add script and tool to confirm/reject insertions
* Refine the detection of TE clusters that are very close to each other
* Verify that reads really support a specific insertion
* Fix sorting to CRAM output
* Move sorting of softclip clusters to merging phase
* Skip finding softclipped clusters when skipping TE clusters
* Annotate softclips as part of TEs
* Embedd SoftClipClusterFinder in ClusterFinder
* Fix softclipped positions when read contains deletions

---------------------
0.4.9 (2018-01-23)
---------------------
* Fix deployment to PyPI

---------------------
0.4.8 (2018-01-23)
---------------------
* Update test data output and allow `:`
* Add edlib to requirements in setup.py
* Add softclip finder test
* Build on python-3.6
* Make futures library conditional for python2
* Drop temporary from requirements
* Extend testcoverage
* Drop `external_bin` from BamAlignmentWriter
* Many small simplifications, bugfixes and enhaced tests
* Improve reporting of 5p and 3p clips
* Add some wigglespace for finding the most likely TSD position
* Keep insertions associated with deletion intact
* Add testcase for a cluster that should not be split
* Fix if/else logic for genotypes
* Skip "genomic sinks" with lots of TE evidence
* Continue on RuntimeError
* Improve splitting of input file
* Need to `fetch` reads in the specified region if using `external_bin=False`
* Don't use external samtools when finding clusters
* Identify decoy regions based on cluster density
* Drop reraise_with_stack, doesn't work on py3
* Fix outdated min/max coordinates leading to dropped chunks
* Re-raise any exceptions when processing chunks
* Fix OrderedDict syntax for py2 compatibility
* Improve logging when splitting input into chunks
* Don't remove read that isn't present anymore
* Fix return value when assembling too many reads
* Fix limiting of region when using multiple threads
* Report maximum MAPQ of read evidence for a cluster
* Bump minimum MAPQ to 4 by default and make it configurable
* Refactor cap3 assembly (so it can be exchanged more easily) and add limit to how many reads it will assemble
* Fix and apply read_is_compatible to all read with BD tag
* Generalize marking clusters as compatible or incompatible and apply at every cluster split or join
* Estimate nref/nalt using overlap of start and end if start and end are more than 50nt apart
* Skip clusters of reads that are inconsistent
* Remove redundant parenthesis, fix typo
* Allow non-proper pairs when counting evidence
* Account for max. mate distance when joining cluster
* Add new dependencies to conda recipe
* Prevent joining clusters that we previously split explicitly
* Don't thread/cache joining of cluster
* Use lru_cache for some cigar operations
* Use cigar_to_max function consistently
* Make use of new AlignmentHeader object (old method now very slow)
* Use edlib align instead of Cap3Assembly
* Fix evidence_against functionality
* Output reads that count as non-support
* Allow picking up location of reference_fasta via env var for quicker test execution
* Fix 3p evidence bam, fix nref with 1 breakpoint
* Update test-data
* Assign left/right based on AD if AD and BD are set
* Make counting more accurate, cleanup various Cluster counts and write out split reads found via `evidence_for_five/three_p`
* Collect evidence for insertions
* Fix a typo in `get_breakpoint_sequence`
* Fix resolving consensus ties if tie contains `N`
* Upgrade to pysam 0.14
* Make split_ads a property since the splits can update
* Fix typo in dumb_consensus help
* Add IUPAC to nucleotides dict
* Restructure non_evidence so that evidence for and against can be counted
* Use `reference_start` instead of deprecated `pos`
* Implement `get_breakpoint_sequence` as a method of TargetSiteDuplication
* Add `evidence_for` function
* Update planemo from 0.46.1 to 0.48.0
* Refine the cluster merging logic
* Fix the overlap calculation, in case the re-aligned contig ends up at a different position
* Update test data output, genotype outputs with higher precision (sigh)

---------------------
0.4.7 (2018-01-23)
---------------------
* Fix Exception that occurs when cluster doesn't have an associated contig
* Fix TE alignment logic when using pre-indexed transposon references
* Control which reads extend a cluster during cluster refinement
* Add a safeguard to avoid merging unrelated, far-away clusters

---------------------
0.4.6 (2017-12-13)
---------------------
* Deploy to conda on py3 as well
* Make sure cluster chunks are ordered
* Avoid hangs due to expection in multiprocessing tasks

---------------------
0.4.2 (2017-12-13)
---------------------
* Fix passing of region specification to pileup engine
* Point out typical useage of --reference_fasta and --reference_index
* Fix cheetah bwa index variable for findcluster galaxy tool

---------------------
0.4.1 (2017-11-20)
---------------------
* Add matplotlib and pandas to dependencies
* Add a script that can plot coverage as an area plot between two bam files
* Update dependencies
* If either three_p or five_p of a tsd is unknown assign the available use the available side to test of a read belongs to the left or right side of an insertion
* Fix crash for unaligned(?) reads
* Change deprecacted alen, pos and mpos to current replacements
* Tune clusterfinding for misaligned long reads

---------------------
0.4.0 (2017-11-09)
---------------------
* Fixes for CRAM input and output
* Adjust chunk-size in readtagger based on readlength (for pacbio/nanopore reads)
* Cleanup temporary bwa indexes
* Dependency updates

---------------------
0.3.25 (2017-06-21)
---------------------
* Refine cluster coordinates using an Assembly strategy
* Fix GFF sorting on python 3
* Improve BWA alignment settings (default to intractg plus -Y) and add align_contigs method to SimpleAligner
* Add pysamtools_view command
* Improve cluster-splitting
* Add multiprocessing-logging recipe
* Only output BWA stderr if the exit code is not zero
* Add a function to sort gff files
* Close open file descriptors
* Make imprecise insertion sites more realistic
* Fix read_index property
* Adapt readtagger to higher coverage datasets
* Fix readtagger crash when not producing discard tag file.
* Add number of mates for left and right support to GFF
* Split clusters that start with reverse reads conatining only BD tags

---------------------
0.3.24 (2017-05-11)
---------------------
* Split cluster if there are multiple polarity switches between Forward and Reverse orientation
* Manipulate copy of cigarlist to avoid numpy issue

---------------------
0.3.23 (2017-05-09)
---------------------
* Expose reference fasta option in bam_readtagger.xml

---------------------
0.3.22 (2017-05-09)
---------------------
* Move readtagger CLI form argparse to click
* Index bamfile if neccesary
* Replace multipocessing pool with ProcessPoolExecutor
* Set the matesequence while tagging reads
* Fix false positives in readtagger module
* Do cap3 assembly in shared memory if passing --shm_dir or if SHM_DIR environment variable is defined
* Parallelize findlcluster by splitting input bam
* Add check_call.py script for rapidly verifying IGV screenshots

---------------------
0.3.21 (2017-04-27)
---------------------
* Fix crash when determining reference name

---------------------
0.3.20 (2017-04-27)
---------------------
* Guess the best TE match and write it into GFF Parent
* Fix case where input files are already sorted
* Remove blast from requirements

---------------------
0.3.19 (2017-04-27)
---------------------
* Skip creating tempdirs in current working directory
* Remove blast-specific files
* Switch to using BWA for annotating detected insertions
* Add more logging and default to not changing sort order unless specifically demanded
* Do dovetailing on coordinate-sorted file

---------------------
0.3.18 (2017-04-25)
---------------------
* Fix small outputs due to switching of `-t` and `-a` options

---------------------
0.3.17 (2017-04-25)
---------------------
* Fix file seeking
* Update dependencies

---------------------
0.3.16 (2017-04-23)
---------------------
* Parallelize readtagger

---------------------
0.3.15 (2017-04-20)
---------------------
* Do not count reads as support if both AD and BD tag contribute to an insertion
* Remove sambamba support

---------------------
0.3.14 (2017-04-19)
---------------------
* Perform readtagging on readname sorted files.
* Catch possible errors
* Add BWA alignment module to replace Blast

---------------------
0.3.13 (2017-04-05)
---------------------
* Add possibility to output cluster contigs as fasta

---------------------
0.3.12 (2017-03-31)
---------------------
* Fix and accelerate the calculation of nref (=non support evidence)
* Update priors and genotype frequrencies to a more realistic model

---------------------
0.3.11 (2017-03-28)
---------------------
* Add a testcase for genotyping module
* Stream over full alignment file instead of fetching regions,
  pysam.AlignmentFile.fetch is too slow

---------------------
0.3.10 (2017-03-26)
---------------------
* Revert local conda dependency resolution
* Fix readtagger.add_mate to work also if one mate is unmapped

---------------------
0.3.9 (2017-03-26)
---------------------
* Add a genotyping module
* Keep tags for alternative alignments if mates are not in a proper pair

---------------------
0.3.4 (2017-03-02)
---------------------
* Speed up assembly steps using multithreading
* Implement a cache for the Cluster.can_join method

---------------------
0.3.3 (2017-03-02)
---------------------
* Fix a crash when writing GFF for a cluster of hardclipped reads
* Change confusing variable names and copypasted docstring

---------------------
0.3.2 (2017-03-02)
---------------------
* Fix another crash when tuple starts with 1,2,7 or 8

---------------------
0.3.1 (2017-03-02)
---------------------
* Fix a crash when a mismatch is the last item in a cigartuple

---------------------
0.3.0 (2017-03-02)
---------------------

* Add a galaxy tool for the findcluster script
* Add new script that finds clusters of reads and outputs GFF or BAM files with these clusters.
* Implement writing clusters as GFF files
* Implement writing out reads with cluster number annotated in CD tag.
* Implement merging of clusters based on whether reads contribute to common contigs
* Use cached-property where it makes sense
* Add module to find, join and annotate clusters of reads
* Represent cigartuple as namedtuple
* Add a Roadmap file
* Add more logic for finding ends of insertions and
* Manipulate cluster of reads to find TSDs
* Add module for cap3 assembly and manipulation of assembled reads
* Fix conda recipe script entrypoints

---------------------
0.2.0 (2017-02-21)
---------------------
* Reformat help text in galaxy wrappers
* Add add_matesequence script to add the sequence of the mate of the current read as a tag
* Add option to discard alternative tag if read is a proper pair
* Stitch cigars that are separated by I or D events
* Add a tag tuple that knows how to format itself
* Update README.rst example with current default tag prefix
* Test with and without discarding verified reads
* Symlink test-files that are shared with the galaxy test, add testcase for allow_dovetailing script
* Fix HISTORY.rst formatting

---------------------
0.1.13(2017-02-17)
---------------------
* Add instructions for development
* Install planemo in deployment step

---------------------
0.1.12(2017-02-17)
---------------------
* Test deployment again

---------------------
0.1.11 (2017-02-17)
---------------------
* Test deployment

---------------------
0.1.10 (2017-02-17)
---------------------
* Fix toolshed deployment

---------------------
0.1.9 (2017-02-17)
---------------------
* Add automated deployment to Galaxy Toolshed
* Add instructions for development and release process

---------------------
0.1.8 (2017-02-17)
---------------------
* Minor release to test release process

---------------------
0.1.7 (2017-02-17)
---------------------
* Extend testing with coverage testing
* Automate deployment to pypi and conda
* Register project with pyup.io

---------------------
0.1.6 (2017-02-16)
---------------------
* Rename to readtagger
* Fix bug with stdin closing file descriptor too early, leading to corrupt
  BAM files
* Extend testing

---------------------
0.1.5 (2017-02-12)
---------------------
* Add option (-wd) to write suboptimal tag into separate BAM file
* Add option (-wv) to write verified tags into separate BAM file
* Performance improvments by letting sambamba handle BAM reading
  and writing. Also elimininate regualr expression to parse cigarstring

---------------------
0.1.4 (2017-02-10)
---------------------
* Add option (-k) to keep alternative tags if they do not
  explain the softclipped read any better.
  Default is to discard them.

---------------------
0.1.3.2 (2017-02-08)
---------------------
* Fix dovetailing script

---------------------
0.1.3 (2017-02-07)
---------------------
* Add option to allow dovetailing in alignment files when tagging reads
* Add separate entrypoint for standalone script

---------------------
0.1.2 (2017-02-05)
---------------------
* Add conda recipe
* Python3 string fix

---------------------
0.1.0 (2017-02-05)
---------------------
* Initial version
