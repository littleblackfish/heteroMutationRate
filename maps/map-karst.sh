while read ACCESSION 
do 

	! [ -e $ACCESSION.sam ] && qsub -q preempt ../src/map.karst -F $ACCESSION -N $ACCESSION-map
done < ../reads/f2_accession
