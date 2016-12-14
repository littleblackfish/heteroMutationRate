## Description

This project attempts to replicate the results in [this paper](http://www.nature.com/nature/journal/v523/n7561/full/nature14649.html) which is also freely available [here](http://opus.bath.ac.uk/46581/1/Parent_progeny_sequencing_indicates_higher_mutation_rates_in_heterozygotes._.pdf).
Although it is set up to use the original data deposited to [BioProject](https://www.ncbi.nlm.nih.gov/bioproject) servers, it can easily be used as a scaffold to run a similiar analysis on arbitrary data.

This work was done for [Matthew Hahn](http://www.bio.indiana.edu/faculty/directory/profile.php?person=mwh)'s *SNP Discovery and Population Genomics* class in the Fall of 2016.

## Requirements

The variant calling workflow requires :

  * [sra-tools](https://github.com/ncbi/sra-tools) for acquiring the reads
  * [TAIR10 reference genome](ftp://ftp.arabidopsis.org/home/tair/Sequences/whole_chromosomes/) for arabidopsis
  * [RepeatMasker](http://www.repeatmasker.org/) to mask the reference
  * [bwa](http://bio-bwa.sourceforge.net/) to map the reads to the reference genome
  * [Picard](https://broadinstitute.github.io/picard/) to do some post processing on the mapping
  * [GATK](https://software.broadinstitute.org/gatk/) to call variants

Note that you will need to have a copy (or link) of [picard.jar](https://github.com/broadinstitute/picard/releases/download/2.7.2/picard.jar) and [GenomeAnalysisTK.jar](https://software.broadinstitute.org/gatk/download/) in the src directory for the variant calling to work.
Other requirements only need to be in your PATH.

The rest of the analysis is implemented in Python. It requires :

  * [Biopython](http://biopython.org/) to parse the reference
  * [PyVCF](http://pyvcf.readthedocs.io/en/latest/http://pyvcf.readthedocs.io/en/latest/) to parse the VCF files
  * [NumPy](http://www.numpy.org/) for efficient computations
  * [Seaborn](http://seaborn.pydata.org/) for plotting

#### Availability

The RepeatMasker database is commercial, but free for acedemic use.
This requires an application that takes a few days to clear, and likely is the bottleneck in running the full workflow.
GATK also requires agreement to a non-commercial licence but this is straight forward.
All remaining software including our analysis code is free and open source.

## Usage

### Variant calling

Note that this repository **includes no data** but a list of accession numbers needed to obtain the data in addition to a script to download it.

After cloning the repository, the [environment script](src/environment) should be sourced from the project root, like so :

``` bash
git clone https://github.com/muzcuk/heteroMutationRate.git
cd heteroMutationRate
source src/environment
```

This will set up the environment for the rest of the workflow. The major steps to reproduce the work are implemented as bash functions in a seperate [script](src/functions.sh).

These steps are roughly :
  1. Download and RepeatMask the reference
  2. Download reads from ncbi
  3. Map reads to reference
  4. Call variants from mapping files
  5. Do the analysis on the resulting vcf file

An [example run](src/example.sh) which would execute the workflow up to the analysis step is included, but this is not advised on a personal computer as this workflow is computationally demanding, requiring up to 2 tb of space for intermediate files.

Most of the work was done on [Karst](https://kb.iu.edu/d/bezu) at Indiana University.
The relevant job files can be found in the src folder; they make use of the same functions and produce an identical result to the example run.

The resulting vcf file containing all the genotypes is in the order of few gbs and can be readily processed on a personal computer.

### Hypothesis testing

The hypothesis proposed by Yang et al. was tested using slightly different methodology.
The functions necessary for the analysis is implemented in a single [pyhton script](src/analyse.py).
The actual analysis is done and presented in a [jupyter notebook](analysis.ipynb).
