#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i1', type=str, required=True, help='input filename, bed file')
parser.add_argument('-i2', type=str, required=True, help='input filename, bed file')
parser.add_argument('-o', type=str, required=True, help='output filename, txt file')
args = parser.parse_args()

#need to the option for argparse
j = False
def cord_capture(file):
    fa_seqs = {}
    f = open(file)
    with open(file, 'r') as f_embl:
                for line_embl in f_embl:
                    if line_embl == '':
                        break
                    new_line_embl = line_embl.strip('\n').split('\t')
                    new_line_embl[1:] = list(map(int, new_line_embl[1:]))
                    if new_line_embl[0] not in fa_seqs.keys():
                        fa_seqs[new_line_embl[0]] = [new_line_embl]
                    else:
                        fa_seqs[new_line_embl[0]].append(new_line_embl)
    return fa_seqs

file1_dict = cord_capture(args.i1)
file2_dict = cord_capture(args.i2)

#get a list of keys
winning_key = []
for key in file1_dict:
    if len(file1_dict[key]) > len(file2_dict[key]):
        winning_key.append([1])
    else:
        winning_key.append(2)


with open(args.o, 'w') as outputfile:
    for item in winning_key:
        if item == 1:
            pass
    for key in file1_dict:
        for i in range(len(file1_dict[key])):
            if len(file2_dict[key]) == 0:
                break
            if file2_dict[key][0][1] > file1_dict[key][i][2]:
                continue
            match = 0
            if file1_dict[key][i][1] > file2_dict[key][0][2]:
                file2_dict[key] = file2_dict[key][1:]
            for f in range(len(file2_dict[key])):
                overlap = min(file1_dict[key][i][2], file2_dict[key][f][2]) - max(file1_dict[key][i][1], file2_dict[key][f][1])
                if match == 0:
                    if overlap > 0:
                        if j == True:
                            file1_dict[key][i][1:] = list(map(str, file1_dict[key][i][1:]))
                            file2_dict[key][f][1:] = list(map(str, file2_dict[key][f][1:]))
                            x = file1_dict[key][i] + file2_dict[key][f]
                            line = "\t".join(x)
                            outputfile.writelines(line + "\n")
                            file1_dict[key][i][1:] = list(map(int, file1_dict[key][i][1:]))
                            file2_dict[key][f][1:] = list(map(int, file2_dict[key][f][1:]))
                        else:
                            file1_dict[key][i][1:] = list(map(str, file1_dict[key][i][1:]))
                            line = "\t".join(file1_dict[key][i])
                            outputfile.writelines(line + "\n")
                            file1_dict[key][i][1:] = list(map(int, file1_dict[key][i][1:]))
                        match += 1
                    else:
                        continue
                if match > 0:
                    if overlap > 0:
                        if j == True:
                            file1_dict[key][i][1:] = list(map(str, file1_dict[key][i][1:]))
                            file2_dict[key][f][1:] = list(map(str, file2_dict[key][f][1:]))
                            x = file1_dict[key][i] + file2_dict[key][f]
                            line = "\t".join(x)
                            outputfile.writelines(line + "\n")
                            file1_dict[key][i][1:] = list(map(int, file1_dict[key][i][1:]))
                            file2_dict[key][f][1:] = list(map(int, file2_dict[key][f][1:]))
                        else:
                            file1_dict[key][i][1:] = list(map(str, file1_dict[key][i][1:]))
                            line = "\t".join(file1_dict[key][i])
                            outputfile.writelines(line + "\n")
                            file1_dict[key][i][1:] = list(map(int, file1_dict[key][i][1:]))
                if match > 0 and overlap <= 0:
                    break
            
