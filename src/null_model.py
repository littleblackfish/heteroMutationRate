#!/usr/bin/env python2

from argparse import ArgumentParser
from Bio import SeqIO
from Bio.Alphabet import generic_dna
from numpy import zeros, argmax, ones

def 


if __name__ == '__main__' :
	

    # Define program parameters
    parser = ArgumentParser(description='Generic Hidden Markov Model solver')
    parser.add_argument('-f', help='fasta file containing full genome')
    parser.add_argument('-v', help='vcf file containing variation')
    args = parser.parse_args()

    chromosomes = [ record for record in SeqIO.parse(args.f, 'fasta', alphabet=generic_dna) ] 

    print len(chromosomes)

