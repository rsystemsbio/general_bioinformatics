#!/usr/bin/env python3

import sys
import os
#grab the knownGene.txt
f1 = sys.argv[1]
#grab the kgXref.txt
f2 = sys.argv[2]

os.system('makeblastdb -in ' + f1 + ' -dbtype nucl')
os.system('makeblastdb -in ' + f2 + ' -dbtype nucl')

os.system("blastn -db " + f2 + " -query " + f1 + " -out " + f1[:-6] + ".out -outfmt '7 qseqid sseqid evalue' -evalue 1e-6 -num_threads 4")

os.system("blastn -db " + f1 + " -query " + f2 + " -out " + f2[:-6] + ".out -outfmt '7 qseqid sseqid evalue' -evalue 1e-6 -num_threads 4")

f2_name = f2[:-6] + ".out"
f1_name = f1[:-6] + ".out"

#filter for the best hit for input blast 2
f_2 = open(f2_name)
output2 = []
filter_pair2 = {}
while (True):
    line = f_2.readline()
    split_string = line.split("\t")
    if line == '':
        break
    if line.startswith('#'):
        pass
    else:
        if split_string[0] not in output2:
            compareable_eval2 = split_string[2]
            output2.append(split_string[0])
            filter_pair2[split_string[0]] = split_string
        else:
            if split_string[2] < compareable_eval2:
                compareable_eval2 = split_string[2]
                filter_pair2[split_string[0]] = split_string
f_2.close()

#filter for the best hit for input blast 1
f_1 = open(f1_name)
output1 = []
filter_pair1 = {}
while (True):
    line = f_1.readline()
    split_string = line.split("\t")
    if line == '':
        break
    if line.startswith('#'):
        pass
    else:
        if split_string[0] not in output1:
            compareable_eval = split_string[2]
            output1.append(split_string[0])
            filter_pair1[split_string[0]] = split_string
        else:
            if split_string[2] < compareable_eval:
                compareable_eval = split_string[2]
                filter_pair1[split_string[0]] = split_string
f_1.close()

a = open("_find_ortholog.output", "w")
orth_list1 = []
for key1 in filter_pair1:
    for key2 in filter_pair2:
        if filter_pair1[key1][1] == key2 and filter_pair2[key2][1] == key1:
            orth_list1.append(key2)
            a.write(key2 + '\t' + key1 + '\n')
a.close()

f = open("_README.txt ", "w")
f.write("\n"+str(len(filter_pair1.keys())) + " blast best blast hits were found comparing " + f1[:-6] + " against " + f2[:-6])
f.write("\n"+str(len(filter_pair2.keys())) + " blast best blast hits were found comparing " + f2[:-6] + " against " + f1[:-6])
f.write("\n"+str(len(orth_list1)) + " best reciprocal orthologous genes were found.")
f.close()

os.system("rm " + f1 + ".*")
os.system("rm " + f2 + ".*")
os.system("rm " + f1_name)
os.system("rm " + f2_name)
