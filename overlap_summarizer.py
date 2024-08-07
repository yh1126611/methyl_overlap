# Use this on result output of bedtools intersect -C
# ∴ this code assumes that the 10th column is number denoting which -b file overlapped with the -a file and the 11th column is overlap length (bp)
# This file should have n identical rows, n being no. of -b .bed files you entered in bedtools intersect -C run to compute overlaps with -a.

import re

aggregate_filename = input("Name of your resulting .bed file from bedtools intersect -C:")
aggregate = open(aggregate_filename, "r")
no_of_elements = int(input("How many .bed files did you overlap for this?:"))

out_filename = r"\.".join(re.split(r"\.", aggregate_filename)[:-1]) + ".summ"
out = open(out_filename, "w")

temp = []
for aggregate_line in aggregate:
    if int(re.split("\t", aggregate_line)[-2])==no_of_elements: # in the line corresponding to last -b overlap element
        temp.append(re.split("\t", aggregate_line)[-1].rstrip("\n"))
        out.write('\t'.join([re.split("\t", aggregate_line)[0], re.split("\t", aggregate_line)[1], re.split("\t", aggregate_line)[2], re.split("\t", aggregate_line)[3], ','.join(temp)]))
        out.write("\n")
        temp=[]
    else: # in all other lines
        temp.append(re.split("\t", aggregate_line)[-1].rstrip("\n"))