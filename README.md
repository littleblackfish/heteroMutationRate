### Description

In this little project we attempt to replicate the results in [this paper](http://www.nature.com/nature/journal/v523/n7561/full/nature14649.html) which is also freely available [here](http://opus.bath.ac.uk/46581/1/Parent_progeny_sequencing_indicates_higher_mutation_rates_in_heterozygotes._.pdf).

This work was done for [Matthew Hahn](http://www.bio.indiana.edu/faculty/directory/profile.php?person=mwh)'s *SNP Discovery and Population Genomics* class in the Fall of 2016.

### Requirements

This project uses :

  * [sra-tools](https://github.com/ncbi/sra-tools) for acquiring data
  * [TAIR10 reference genome](ftp://ftp.arabidopsis.org/home/tair/Sequences/whole_chromosomes/) for arabidopsis
  * [bwa](http://bio-bwa.sourceforge.net/) to map the reads to the reference genome
  * [Picard](https://broadinstitute.github.io/picard/) to do some post processing on the mapping
  * [GATK](https://software.broadinstitute.org/gatk/) to call variants

The rest of the analysis is implemented in Python.

### Structure

This workflow is computationally intensive, most significantly on storage. 
Most of the work was done in [Brendel Group](http://www.brendelgroup.org/)'s computers in addition to [Karst](https://kb.iu.edu/d/bezu) at Indiana University.
This repository has all the scripts needed to reproduce the work.
Each folder has a shell script that would run the commands that would fill the folder.
