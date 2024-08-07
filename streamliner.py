# To be used to a (mod. prob. calculated & deduplicated) result file of bedtools intersect -wao
# Input should have a specific column dedicated to containing the identification no. of overlapped element
# Last column should be the no. of bp of overlap

import re

wao_filename = input("What is the name of your input agg. file (bedtools intersect -wao result after QC)?:")
wao_file = open(wao_filename, "r")
out = open('.'.join(['.'.join(re.split(r"\.", wao_filename)[:-1]), "summ"]), "w")
numElem = int(input("How many elements did you use for -b in bedtools intersect?:"))
elemCol = int(input("Which column of input file contains the element identifier number?:"))-1

temp_coord = ["0", "0", "0", "0"] # An array to assign bed coordinates as items 0, 1 and 2 and current element number as item 3
temp_overlap = [] # An array to assign overlap length of each elements in respective positions
for line in wao_file:
    if re.split("\t", line)[0]==temp_coord[0] and re.split("\t", line)[1]==temp_coord[1] and re.split("\t", line)[2]==temp_coord[2]: # old coordinate
        if temp_coord[3]==re.split("\t", line)[elemCol]: # 2nd+ overlap of the previous line's element
            temp_overlap[-1] = str(int(temp_overlap[-1].rstrip()) + int(re.split("\t", line)[-1]))
        else: # new element
            for i in range(int(temp_coord[3]),int(re.split("\t", line)[elemCol])-1):
                temp_overlap.append("0")
            temp_overlap.append(re.split("\t", line)[-1].rstrip())
            temp_coord[3] = re.split("\t", line)[elemCol]

    else: # new coordinate
        if temp_coord!=["0","0","0","0"]: # not the first line
            for i in range(len(temp_overlap),numElem):
                temp_overlap.append("0")
            out.write('\t'.join([str(temp_coord[0]), str(temp_coord[1]), str(temp_coord[2]), ','.join(temp_overlap)])) # 이전 꺼 처리
            out.write("\n")
            temp_overlap = []

        if re.split("\t", line)[elemCol]!=".": # overlap exists (not ".")
            for i in range(int(re.split("\t", line)[elemCol])-1):
                temp_overlap.append("0")
            temp_overlap.append(re.split("\t", line)[-1].rstrip())
            temp_coord[0] = re.split("\t", line)[0]
            temp_coord[1] = re.split("\t", line)[1]
            temp_coord[2] = re.split("\t", line)[2]
            temp_coord[3] = re.split("\t", line)[elemCol]
        else: # new coordinate, no overlap (".")
            for i in range(numElem):
                temp_overlap.append("0")
            temp_coord[0] = re.split("\t", line)[0]
            temp_coord[1] = re.split("\t", line)[1]
            temp_coord[2] = re.split("\t", line)[2]

for i in range(int(temp_coord[3])+1, numElem-1):
    temp_overlap.append("0")
out.write('\t'.join([temp_coord[0], temp_coord[1], temp_coord[2], ','.join(temp_overlap)]))
out.write('\n')