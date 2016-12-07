# This is the log script
# to prepare the TAIR10 reference genome for Arabidopsis
# obtained from ftp://ftp.arabidopsis.org/home/tair/Sequences/whole_chromosomes/
# for variant calling via GATK
# written by murat in 2016

# Paths to programs used

REPEATMASKER=~/RepeatMasker/RepeatMasker
SAMTOOLS=~/samtools/samtools
PICARD="java -jar ~/GATK/picard.jar"
BWA="~/bwa.kit/bwa"

# Download all the chromosomes and append to make a combined multifasta file

until shasum -cs TAIR10.shasum ; do
  [ -e TAIR10.fas ] && rm TAIR10.fas
  echo 'Reference does not exist or does not match hash.'
  echo 'Downloading and concatenating the TAIR10 reference...'
  for c in {1,2,3,4,5,C,M} ; do
    wget ftp://ftp.arabidopsis.org/home/tair/Sequences/whole_chromosomes/TAIR10_chr$c.fas -q -O - \
    >> TAIR10.fas
  done
done

echo 'Reference downloaded and validated.'


# Run repeatmasker on whole genome
$REPEATMASKER -species arabidopsis TAIR10.fas

mv TAIR10.fas.masked TAIR10-masked.fa

# Create bwa index for mapping
$BWA index TAIR10-masked.fa

# Create index
$SAMTOOLS faidx TAIR10-masked.fa

# Create dictionary with picard
$PICARD CreateSequenceDictionary R=TAIR10-masked.fa O=TAIR10-masked.fa.dict
