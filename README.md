### Description

In this little project we attempt to replicate the results in [this paper](http://www.nature.com/nature/journal/v523/n7561/full/nature14649.html) which is also freely available [here](http://opus.bath.ac.uk/46581/1/Parent_progeny_sequencing_indicates_higher_mutation_rates_in_heterozygotes._.pdf).

This work was done for [Matthew Hahn](http://www.bio.indiana.edu/faculty/directory/profile.php?person=mwh)'s *SNP Discovery and Population Genomics* class in the Fall of 2016.

### Requirements

Thhe main workflow requires :

  * [sra-tools](https://github.com/ncbi/sra-tools) for acquiring the reads
  * [TAIR10 reference genome](ftp://ftp.arabidopsis.org/home/tair/Sequences/whole_chromosomes/) for arabidopsis
  * [RepeatMasker](http://www.repeatmasker.org/) to mask the reference
  * [bwa](http://bio-bwa.sourceforge.net/) to map the reads to the reference genome
  * [Picard](https://broadinstitute.github.io/picard/) to do some post processing on the mapping
([direct download](https://github.com/broadinstitute/picard/releases/download/2.7.2/picard.jar))
  * [GATK](https://software.broadinstitute.org/gatk/) to call variants

The rest of the analysis is implemented in Python. It requires :

  * [Biopython](http://biopython.org/) to parse the reference
  * [PyVCF](http://pyvcf.readthedocs.io/en/latest/http://pyvcf.readthedocs.io/en/latest/) to parse the VCF files
  * [NumPy](http://www.numpy.org/) for efficient computations

#### Availability

The RepeatMasker database is commercial, but free for acedemic use.
This requires an application and takes a few days to clear, likely the most problematic part in running the full workflow.
GATK also requires agreement to a non-commercial licence but this is straight forward.
All remaining software, including our analysis code is free and open source.


### Structure

This repository no data but all the scripts needed to reproduce the work.
The [src/environment]() should be sourced from the project root, it sets up environment variables.
The major steps to reproduce the work are embedded in bash functions in [src/functions.sh]().

These steps are roughly :
  1. Download and RepeatMask the reference
  2. Download reads from ncbi
  3. Map reads to reference
  4. Call variants from mapping files
  5. Run analysis script on the resulting vcf file

An example run which would theoretically replicate the whole thing is included in [src/example_run.sh](), but this is not advised as this workflow is computationally demanding, most significantly on storage, requiring up to 2 tb of space for intermediate files.

Most of the work was done on [Karst](https://kb.iu.edu/d/bezu) at Indiana University.
The relevant job files can be found in the src folder.

The resulting vcf file is in the order of few gbs and can be readily processed on a personal computer.
