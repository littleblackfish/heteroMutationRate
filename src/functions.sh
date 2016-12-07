#!/bin/bash

PICARD="java -jar /home/muroztur/GATK/picard.jar"
FDUMP="/home/muz/sra-tools/bin/fastq-dump"

# checks existence of reads for a given accession number
# downloads from ncbi if it does not exist
# requires fastq-dump from sratools

function get_reads {
	ACC=$1
	if [ -e ${ACC}_1.fastq.gz ]  && [ -e ${ACC}_2.fastq.gz ]
	then
		echo $ACC exists
	else
		echo $ACC does not exist
		$FDUMP -split-3 --gzip $ACC
	fi
}

# maps reads to reference
# first argument is reference basename
# second argument is read basename (accession number)
# generates readBaseName.sam

function map_reads {
	REFERENCE=$1
	ACCESSION=$2
	bwa mem ${REFERENCE} \
	${ACCESSION}_1.fastq.gz ${ACCESSION}_2.fastq.gz \
	> ${ACCESSION}.sam
}

# function to convert sam to bam
# adds dummy 'read group' fields and
# sorts the bam file at the same time
# takes the accession no as an input an looks for the *.sam file
# requires PICARD

function sam_to_bam {
	ACC=$1
	if [ -e ${ACC}.bam ]
	then
		echo ${ACC} already exists
	else
		echo ${ACC} begin.
	# add readgroups, sort and convert to bam with index
	  ${PICARD} AddOrReplaceReadGroups \
		  I=${ACC}.sam \
		  O=${ACC}.bam \
		  SORT_ORDER=coordinate \
		  CREATE_INDEX=True \
		  RGID=foo \
		  RGLB=bar \
		  RGPL=illumina \
		  RGSM=${ACC} \
		  RGPU=blank
  fi
}

# marks duplicate mappings
# this is necessary for GATK tools to work
# requires PICARD
# generates accession-marked.bam
# generates accession-marked.bai

function mark_duplicates {
	ACCESSION=$1

 ${PICARD} MarkDuplicates \
  	I=${ACCESSION}.bam \
		O=${ACCESSION}.marked.bam \
		M=${ACCESSION}-metrics.txt \
		CREATE_INDEX=True
}

# calls variants using GATK
# generates gvcf files

function call_variants {
	REFERENCE=$1
	ACCESSION=$2
	${GATK} -R ${REFERENCE} \
		-T HaplotypeCaller  \
		-I ${ACCESSION}.marked.bam\
		-ERC GVCF \
		-o ${ACCESSION}.g.vcf
	}




#add_groups $1
