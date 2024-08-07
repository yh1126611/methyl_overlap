# Assumes you have conducted bedtools intersect -wao with -b as the file with pb-CpG-tools output (CG sites w/ mod. prob. scores)

import pandas as pd
import re

aggregate_filename = input("Name of your resulting .bed file from bedtools intersect -wao:")
aggregate = pd.read_csv(aggregate_filename, sep="\t", header=None, low_memory=False)

out_filename = "".join([str(r"\.".join(re.split(r"\.", aggregate_filename)[:-1])), "_summarized.csv"])
print(out_filename)

modProb_col = int(input("Which column contains mod. prob. scores in your file?:"))-1
aggregate = aggregate[[0,1,2,modProb_col]]
print(aggregate.groupby([0, 1, 2]).mean())

summ_result = aggregate.groupby([0, 1, 2]).mean()
summ_result.to_csv(out_filename, index=True, header=False)