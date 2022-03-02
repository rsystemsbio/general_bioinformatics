#!/usr/bin/env python3
import sys

f1 = open(sys.argv[1])

f2 = open(sys.argv[2])

while (True):
    line = f1.readline()
    #do not consider empty lines
    if line == '':
        break
    #do not consider fasta headers
    if ">" not in line:
        #append the line but remove the new line character
        sequence1 = line.rstrip()
f1.close()

while (True):
    line = f2.readline()
    #do not consider empty lines
    if line == '':
        break
    #do not consider fasta headers
    if ">" not in line:
        #append the line but remove the new line character
        sequence2 = line.rstrip()
f2.close()

startval = 0
match = 1
mismatch = -1
gap = -1
val = 0
scoremat = []
for q in range(len(sequence1)+1):
    new_row = []
    if q == 0:
        for f in range(len(sequence2)+1):
            new_row.append((gap*f))
        scoremat.append(new_row)
    else:
        for i in range(len(sequence2)+1):
            if i == 0:
                new_row.append(q*gap)
            else:
                diag = scoremat[(q-1)][i-1]
                top = scoremat[(q-1)][i] + gap
                left = new_row[(i-1)] + gap
                if sequence1[q-1] != sequence2[i-1]:
                    diag += mismatch
                    maxi = max(diag, top, left)
                    new_row.append(maxi)
                else:
                    diag += match
                    maxi = max(diag, top, left)
                    new_row.append(maxi)
        scoremat.append(new_row)
###############
#walking it back
###############
seq1_align = ""
seq2_align = ""
alignvals = ""

lenseq1 = len(sequence1)
lenseq2 = len(sequence2)

while (lenseq1 > 0 and lenseq2 > 0):
    top = scoremat[lenseq1-1][lenseq2] + mismatch
    left = scoremat[lenseq1][lenseq2-1] + mismatch
    if sequence1[lenseq1-1] == sequence2[lenseq2-1]:
        diag = scoremat[lenseq1-1][lenseq2-1] + match
    else:
        diag = scoremat[lenseq1-1][lenseq2-1] + mismatch
    maxi = max(diag, top, left)
    
    if diag == maxi:
        #adding to the string in reverse
        seq1_align = sequence1[lenseq1-1] + seq1_align
        seq2_align = sequence2[lenseq2-1] + seq2_align
  
        if sequence1[lenseq1-1] == sequence2[lenseq2-1]:
            alignvals = "|" + alignvals
        else:
            alignvals = "*" + alignvals
        lenseq1 -= 1
        lenseq2 -= 1
    if left == maxi:
        seq1_align = "_" + seq1_align
        seq2_align = sequence2[lenseq2-1] + seq2_align
        lenseq2 -= 1
        alignvals = " " + alignvals
    if top == maxi:
        seq2_align = "_" + seq2_align
        seq1_align = sequence1[lenseq1-1] + seq1_align
        lenseq1 -= 1 
        alignvals = " " + alignvals

print(seq1_align)
print(alignvals)
print(seq2_align)
print("Alignment score: " + str(scoremat[lenseq1-1][lenseq2-1]))

