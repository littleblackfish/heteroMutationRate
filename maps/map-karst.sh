while read acc 
do 
	! [ -e $acc.sam ] && qsub ../src/map.karst -F $acc -N $acc 
done < ../reads/f2_accession
