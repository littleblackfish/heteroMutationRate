#!/usr/bin/env python2

from argparse import ArgumentParser
from Bio import SeqIO
from Bio.Alphabet import generic_dna
from numpy import array,searchsorted,vstack,min
from random import randint
from collections import Counter
import vcf

# takes a chromosome
# returns a list of ranges that are masked (as Ns) 

def get_masked_ranges(chromosome) :
    
    masked = list()
    inmasked = False

    for i, char in enumerate(chromosome) : 
        # beginning of masked range (inclusive)
        if char == 'N' and not inmasked : 
            masked_begin = i
            inmasked = True
        # end of masked range (exclusive)
        elif char != 'N' and inmasked :
            masked_end = i 
            masked_range = (masked_begin, masked_end)
            masked.append(masked_range)
            inmasked = False

    return masked


# checks whether given position is in a masked region

def in_masked(position, maskedList) :
    for begin, end in maskedList :
        if begin <= position < end :
            return True
    return False


# samples random mutation positions that do not hit masked regions of a chromosome
# these positions would not be called even if they had actual mutations

def sample_mutations(nSamples, chromosome) :

    maskedList = get_masked_ranges(chromosome) 

    chromosomeSize = len(chromosome)

    # sample positions
    positionList=list()
    for i in range(nSamples) :
        position = randint(0, chromosomeSize-1)
        # resample if the position is in a masked region
        while in_masked(position, maskedList) :
            position = randint(0, chromosomeSize-1)
        positionList.append(position)
    
    #return as sorted numpy array for efficiency
    return array(sorted(positionList))


# gets positions that are heterozygous in multiple samples

def get_hetero_positions(vcfFile, minGQ=30, minInherit=10)  :

    vcfIter = vcf.Reader(filename=vcfFile)
    samples = vcfIter.samples 

    heteroList = dict() 

    for record in vcfIter :
        GTcount = Counter()
        for sample in samples :
            GT = record.genotype(sample)
            # take only heteros
            if GT.is_het :
                GTdata=GT.data
                # filter for genotype quality
                if GTdata.GQ >= minGQ and GTdata.GT != '0/0':
                    GTcount[GTdata.GT] += 1
        heteroList[record.POS] = GTcount 
        # work on 1st chromosome only for debugging
        if record.CHROM != 'Chr1' :
            break

    heteroParent = list()
    denovoMutation = list()
    for pos in heteroList :
        if len(heteroList[pos]) == 1 and heteroList.values()[0] ==1 :
            denovoMutation.append(pos)
            continue

        for gt in heteroList[pos] :
            if heteroList[pos][gt] >= minInherit :
                heteroParent.append(pos)
                break

    return heteroList, heteroParent, denovoMutation
        


    return tmp



    #return array(sorted([randint(0, 30427671) for i in range (100000)]))

# samples random mutations, returns their distance from hetero positions

def sample_hetero_distances(nsamples, chromosome, heteroList) :

    positionList = sample_mutations(nsamples, chromosome)

    heteroList = get_hetero_positions()

    # find the closest hetero points for each sampled position
    # from left and right

    rightHeteros = searchsorted(heteroList, positionList) 
    leftHeteros = rightHeteros-1

    # get distances to the closest hetero positions
    # from left and right
    rightDist = heteroList[rightHeteros] - positionList
    leftDist  = positionList - heteroList[leftHeteros]

    # get the minimum distance from either left or right
    dist = min (vstack((rightDist, leftDist)), axis=0)


    return dist



        

if __name__ == '__main__' :
	

    # Define program parameters
    parser = ArgumentParser(description='Generic Hidden Markov Model solver')
    parser.add_argument('-f', help='fasta file containing full genome')
    parser.add_argument('-v', help='vcf file containing variation')
    args = parser.parse_args()

    chromosomes = [ record for record in SeqIO.parse(args.f, 'fasta', alphabet=generic_dna) ] 

    print len(chromosomes)

