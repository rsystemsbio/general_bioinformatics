#!/usr/bin/env python3

import sys
#take the desired column to select
n = int(sys.argv[1])
#take the input file
f = open(sys.argv[2])
line = f.readline()

while (True):
    line = f.readline()
    #split the string into a list based on the tab character
    split_string = line.split("\t")
    if line == '':
        break
    #select the correct item in the list, but adjust the indexer
    print(split_string[n-1], file=sys.stdout)
f.close()