

import os
import csv

cwd = os.getcwd()

def get_file(pattern,type, path = cwd):
    '''get the file list of a certain pattern, e.g. '.fasta'. default path for the files is current work directory'''
    file_list = []
    files = os.listdir(path)
    for f in files:
        if pattern in f and type in f:
            file_list.append(f)
    return file_list


trim_out_file = get_file('trim','.out')
res = [['file', 'Input Read Pairs', 'Both Surviving', 'Forward Only Surviving', 'Reverse Only Surviving', 'Dropped']]
for file in trim_out_file:
    for lines in open(file):
        if lines.startswith('SRR'): #need to be consistent with the echo $value , which should be printed before trimming. (see sbatch submission file)
            trim_1file = [lines.strip()] #add the file name being trimmed
            #trim_1file.append(lines.strip())
        if 'Input Read Pairs' in lines:
            items = lines.strip().split(' ')
            input, bth, f, r, d = items[3], '\t'.join(items[6:8]), '\t'.join(items[11:13]), '\t'.join(items[16:18]), '\t'.join(items[19:21])
            stat = [input, bth, f, r, d]
            trim_1file += stat
            res.append(trim_1file)
        elif 'Input Reads' in lines:
            items = lines.strip().split(' ')
            input, surv, d = items[2], '\t'.join(items[4:6]), '\t'.join(items[7:])
            stat = [input, surv, 'na', 'na', d]
            trim_1file += stat
            res.append(trim_1file)
        else:
            continue

with open('trim_res.csv', 'w') as handle:
    writer = csv.writer(handle, dialect='excel')
    for row in res:
        writer.writerow(row)