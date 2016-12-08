while read acc 
do 
	[ -e $acc.sam ] && ! [ -e $acc.marked.bam ] && qsub ../src/sam_to_bam.karst -F $acc -N $acc-tobam 
done < ../reads/f2_accession
