#!/bin/bash

source ../src/functions.sh

filename=f2_accession

while read -r accession ;
do
  get_reads accession
done < $filename
