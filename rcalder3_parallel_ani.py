#!/usr/bin/env python3

import argparse
from multiprocessing import Pool
import os
t=3
parser = argparse.ArgumentParser()
parser.add_argument('-t', type=str, required=True, help='number of threads')
parser.add_argument('-o', type=str, required=True, help='output filename, txt file')
args, unknownargs = parser.parse_known_args()

if args.t:
    t = int(args.t)

my_result = []
index = []
for i in range(0,len(unknownargs)): 
    for j in range(i,len(unknownargs)): 
            my_result.append([unknownargs[i],unknownargs[j]])
            index.append([i,j])

def work_log(files):
    unique_output = files[0]+files[1]
    os.system('dnadiff -p ' + unique_output + ' ' + files[0]+ ' ' + files[1])
    line_count = 0
    with open(unique_output+'.report', 'r') as file:
                for line in file:
                    new_line = line.strip('\n').split('\t')
                    if line_count == 18:
                        print(new_line[-1][-7:])
                        val = new_line[-1][-7:]
                        break
                    line_count +=1
    os.system('rm ' + unique_output + '*')
    return(val)       

if __name__ == "__main__":
    p = Pool(int(args.t))
    results = list(p.map(work_log, my_result))
    output_mat = []
    for i in range(0,len(unknownargs)):
        empty_list = [0]*len(unknownargs)
        output_mat.append(empty_list)
    for i in range(len(results)):
        f1 = index[i][0]
        f2 = index[i][1]
        #print(results[i])
        if float(results[i]) <=0:
            output_mat[f2][f1] = '100'
        else:
            output_mat[f2][f1] = str(results[i])

    for i in range(0,len(unknownargs)): 
        for j in range(i,len(unknownargs)): 
            if (i!=j):
                output_mat[i][j] = output_mat[j][i] 
    with open(args.o,'w') as file:
        for i in range(0,len(unknownargs)):
            #write the text line
            if i == 0:
                file.write("\t".join((['']+unknownargs[:-1]+unknownargs[-1:]))+'\n')
                file.write("\t".join(([unknownargs[i]]+output_mat[i]))+'\n')
            else:
                file.write("\t".join(([unknownargs[i]]+output_mat[i]))+'\n')
    p.close()
    p.join()


