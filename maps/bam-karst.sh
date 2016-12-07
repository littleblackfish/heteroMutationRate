while read acc 
do 
	[ -e $acc.sam ] && ! [ -e $acc.bam ] qsub ../src/sam_to_bam.karst -F $acc -N $acc 
done < ../reads/f2_accession
