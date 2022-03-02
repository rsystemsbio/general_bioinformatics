#!/usr/bin/env python3
#Customizing an output file from multiple outputs
import sys
#grab the knownGene.txt
f1 = open(sys.argv[1])
#grab the kgXref.txt
f2 = open(sys.argv[2])
#grab the InfectiousDisease-GeneSets.txt
f3 = open(sys.argv[3])

#set up the dictionary of desired columns
final_dict = {}


while (True):
    line = f2.readline()
    #split the string into a list based on the tab character
    split_string = line.split("\t")
    if line == '':
        break
    #set the gene name as the virst value in the dict list based the UCSC ID
    final_dict[(split_string[0])] = [split_string[4]]
f2.close()

while (True):
    line = f1.readline()
    #split the string into a list based on the tab character
    split_string = line.split("\t")
    if line == '':
        break
    #add the chromosome name
    final_dict[(split_string[0])].append(split_string[1])
    #add the start position
    final_dict[(split_string[0])].append(split_string[3])
    #add the stop position
    final_dict[(split_string[0])].append(split_string[4])
    #once the items are added, replace the key name with the first value already in the dict key
    final_dict[final_dict[(split_string[0])][0]] = final_dict[(split_string[0])]
    #delete the redundant key
    del final_dict[(split_string[0])]
f1.close()

final_list = []
#print the column titles to stdout
print("Gene","\t","Chr", "\t", "Start", "\t", "Stop", file=sys.stdout)
while (True):
    line = f3.readline()
    if line == '':
        break
    if line.rstrip() in final_dict.keys():
        #grab keys based from final_dict based on the gene name in infectious disease genesets
        final_list = final_dict[line.rstrip()]
        #print each of the items in the desired list in tab seperated format to stdout
        print(final_list[0],"\t",final_list[1],"\t",final_list[2],"\t",final_list[3], file=sys.stdout)
f3.close()
