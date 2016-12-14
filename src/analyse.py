#!/usr/bin/env python2

from argparse import ArgumentParser
from Bio import SeqIO
from Bio.Alphabet import generic_dna
from numpy import array,searchsorted,vstack,min,mean,std,abs,log
from random import randint
from collections import Counter,defaultdict
import vcf

# takes a chromosome
# returns a list of ranges that are masked (as 'N's)

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
        if end > position >= begin :
            if position < end :
            #    print begin, end, position, True
                return True
        if position < begin :
            #    print begin, end, position, False
                return False


# samples random mutation positions that do not hit masked regions of a chromosome
# these positions would not be called even if they had actual mutations

def sample_mutations(nSamples, maskedList, chrSize=None) :

    if not chrSize :
        chrSize=maskedList[-1][1]+10

    # sample positions
    positionList=list()
    for i in range(nSamples) :
        position = randint(0, chrSize-1)
        # resample if the position is in a masked region
        while in_masked(position, maskedList) :
            position = randint(0, chrSize-1)

        positionList.append(position)

    #return as sorted numpy array for efficiency
    return array(sorted(positionList), dtype=int)


# gets heterozygous variants satisfying quality criteria
# returns two dictionaries for SNPs and indels
# each indexed by key

def get_hetero_variants(vcfFile, snpMinGQ=50, indelMinGQ=30, minAD=5)  :

    vcfIter = vcf.Reader(filename=vcfFile)
    samples = vcfIter.samples

    heteroSNPs = defaultdict(dict)
    heteroIndels = defaultdict(dict)

    for record in vcfIter :
        # we are dealing with heterozygous variants
        # either heterozygous in the parent (f1)
        # or hetero through denovo mutation

        if record.num_het :
            GTcount = Counter()

            variants = record.get_hets()

            # filter by genotype quality (GQ)
            if record.is_snp :
                variants = filter(lambda call: call.data.GQ > snpMinGQ, variants)
            elif record.is_indel :
                variants =  filter(lambda call: call.data.GQ > indelMinGQ, variants)

            if len(variants) == 0 :
                continue

            # filter by alelle depth (AD)
            for variant in variants :
                if min (variant.data.AD) >= minAD  :
                    GTcount[variant.data.GT] += 1

            if len(GTcount) == 0 :
                continue

            if record.is_snp :
                heteroSNPs[record.CHROM][record.POS]   =  GTcount
            elif record.is_indel :
                heteroIndels[record.CHROM][record.POS] =  GTcount

        # work on 1st chromosome only for debugging
#        if record.CHROM != 'Chr1' :
#            break

    return heteroSNPs, heteroIndels

def process_hetero_variants (variants, minInherit=10, maxDenovo=1) :

    inheritedSNPs = list()
    denovoSNPs = list()

    for pos in variants :
        var=variants[pos]
        if var['0/1'] >= minInherit :
            inheritedSNPs.append(pos)
        elif var['0/1'] <= maxDenovo :
            denovoSNPs.append(pos)

    return array(sorted(inheritedSNPs),dtype=int), array(sorted(denovoSNPs),dtype=int)


# samples random mutations, returns their distance from hetero positions

def get_hetero_distances(mutationPos, heteroPos) :

    # find the closest hetero points RIGHT of each mutation

    rightHeteros = searchsorted(heteroPos, mutationPos)

    # dirty little hack to compensate for searchsorted behaviour.
    # make sure mutationPos is sorted for this to work
    # clear zeros from the beginning
    i = 0
    while rightHeteros[i] == 0 :
        rightHeteros[i] += 1
        i+=1
    # clear len(heteroPos) from the end
    i = -1
    while rightHeteros[i] == len(heteroPos) :
        rightHeteros[i] -= 1
        i -= 1

    # get the other closest hetero point LEFT of each mutation
    leftHeteros = rightHeteros-1

    # get distances to the closest hetero positions
    # from left and right
    rightDist = abs(heteroPos[rightHeteros] - mutationPos)
    leftDist  = abs(mutationPos - heteroPos[leftHeteros])

    # get the minimum distance from either left or right
    dist = min (vstack((rightDist, leftDist)), axis=0)

    return dist


# given a list of distances
# returns discrete probability distribution

def get_discrete_dist(samples) :
    dist = Counter()
    for sample in samples:
        dist[sample] +=1

    total = float (sum(dist.values()))

    for item in dist :
        dist[item] /= total

    return dist


# returns D_KL(P||Q)
# note that P(i) must be 0 when Q(i)=0
def kl_dist(P, Q) :
    KLdist = 0
    for item in P :
        KLdist += P[item] * log(P[item]/Q[item])

    return KLdist

# returns JSD (P||Q)

def js_dist(P, Q) :
    PuQ = set(P).union(set(Q))

    M = {item:(P[item]+Q[item])*0.5 for item in PuQ }

    return 0.5*(kl_dist(P, M) + kl_dist(Q, M))

if __name__ == '__main__' :

    # Define program parameters
    parser = ArgumentParser(description='Generic Hidden Markov Model solver')
    parser.add_argument('-f', help='fasta file containing full genome')
    parser.add_argument('-v', help='vcf file containing variation')
    #args = parser.parse_args()
#    chromosomes = [ record for record in SeqIO.parse(args.f, 'fasta', alphabet=generic_dna) ]

#    maskedList { chromosome.name:get_masked_ranges(chromosomes[0])
