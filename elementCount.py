#
#!/usr/bin/env python3
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, required=True, help='input filename, bed file')
args = parser.parse_args()



fa_seqs = {}
f = open(args.i)

with open(args.i, 'r') as f_embl:
            for line_embl in f_embl:
                new_line_embl = line_embl.strip('\n').split('\t')
                new_line_embl[1:] = list(map(int, new_line_embl[1:]))
                if new_line_embl[0] not in fa_seqs.keys():
                    maxi = max(new_line_embl[1:])
                    mini = min(new_line_embl[1:])
                else:
                    if maxi < max(new_line_embl[1:]):
                        maxi = max(new_line_embl[1:])
                    if mini > min(new_line_embl[1:]):
                        mini = min(new_line_embl[1:])
                fa_seqs[new_line_embl[0]] = [mini, maxi]
for key in fa_seqs:
    first_row = []
    overlap = []
    for i in range(fa_seqs[key][0], fa_seqs[key][1]):
        first_row.append(i)
        overlap.append(0)
        
    with open(args.i, 'r') as f_embl:
            for line_embl in f_embl:
                if line_embl == '':
                    break
                new_line_embl = line_embl.strip('\n').split('\t')
                if new_line_embl[0] == key:
                    for i in range((int(new_line_embl[1]))-fa_seqs[key][0], int(new_line_embl[2])-fa_seqs[key][0]):
                        overlap[i] += 1
    set_val = overlap[0]
    begin_cord = first_row[0]
    start = first_row[0]
    for i in range(0, len(overlap)):
        if overlap[i] != set_val:
            if overlap[i-1] != 0:
                print(key + '\t' + str(start) + '\t' + str(first_row[i]) + '\t' + str(overlap[i-1]))
            start = first_row[i]
            set_val = overlap[i]
