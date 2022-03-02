#!/usr/bin/env python3
#this script counts existing kmers
import sys

#take the input kmer value
n = int(sys.argv[1])
#take the input file
f = open(sys.argv[2])

#read line in input file
line = f.readline()

#create and empty list to store sequence values
sequences = []

while (True):
    line = f.readline()
    #do not consider empty lines
    if line == '':
        break
    #do not consider fasta headers
    if ">" not in line:
        #append the line but remove the new line character
        sequences.append(line.rstrip())
f.close()

#combine the list of strings into one long string
sequences_comb = "".join(sequences)

#create an empty dictionary to store kmer counts
sum_seqs = {}

#loop through the genome
for i in range(len(sequences_comb)):
    #grab a slice based on a window with a moving starting position and the slice length
    sliced = sequences_comb[i:(n+i)]
    #make sure the slice window does not extend past the end of the string
    if (n+i) > len(sequences_comb):
        break
    #add the item to the dictionary if it does not exist
    if sliced not in sum_seqs:
        sum_seqs[sliced] = 1
    #increase the value in the dictionary if it already exists
    else:
        sum_seqs[sliced] += 1
#print the output to std.out in tab seperated format
for key in sorted(sum_seqs):
    print(key, '\t', sum_seqs[key], file=sys.stdout)