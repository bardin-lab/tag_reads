try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__VERSION__ = '0.1.6'

requirements = ['contextlib2', 'pysam', 'six', 'shutilwhich']

ENTRY_POINTS = '''
        [console_scripts]
        tag_reads=tag_reads.tag_reads:main
        allow_dovetailing=tag_reads.allow_dovetailing:main
'''

setup(
    name='tag_reads',
    version=__VERSION__,
    packages=['tag_reads'],
    install_requires=requirements,
    entry_points=ENTRY_POINTS,
    keywords='Bioinformatics',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Operating System :: POSIX',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    extras_require={
        'testing': ["pytest", "pytest-datadir", "tox", "planemo", "cookiecutter", "bumpversion"],
    },
    url='https://github.com/bardin-lab/tag_reads',
    license='MIT',
    author='Marius van den Beek',
    author_email='m.vandenbeek@gmail.com',
    description='Tags reads in BAM files based on alignments in additional BAM files.'
)
