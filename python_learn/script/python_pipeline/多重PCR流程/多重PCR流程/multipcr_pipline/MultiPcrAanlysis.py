"""
@File   : MultiPcrAanlysis.py
@Time   : 2022/8/15 16:18
@Author : Tian Chen
@Email  : chentian@genomics.cn
"""
import os
import json
import sys
import argparse
import logging
import pandas as pd
import numpy as np
from collections import defaultdict, Counter
from multiprocessing import Pool

import pipeline as pipe

class JSONObject:
    def __init__(self, d):
        self.__dict__ = d


def init(code_dir):
    global software
    with open(f'{code_dir}/software.json', 'r') as f:
        data = json.dumps(json.load(f))
    software = json.loads(data, object_hook=JSONObject)


def build_primer_index(path: str, primer_file: str, adapter_flag: bool):
    """
    primer_file column: name_id,chr,primer1_name,primer1,start1,end1,strand1,primer2_name,primer2,start2,end2,strand2
    """
    work_dir = os.getcwd()
    cmd = f'mkdir -p {path}/database && cp -p {primer_file} {path}/database'
    pipe.run_shell(cmd, 'create database')
    os.chdir(f'{path}/database/')
    primer_path = path+'/database/'+primer_file
    try:
        if '.xlsx' in primer_file:
            primer = pd.read_excel(primer_path)
        else:
            seps = ',' if '.csv' in primer_file else '\s+'
            primer = pd.read_csv(primer_path, sep=seps)
    except IOError as e:
        logging.error(e)
        sys.exit(2)
    if adapter_flag:
        primer['primer1'] = primer['primer1'].apply(lambda x: x[21:])
        primer['primer2'] = primer['primer2'].apply(lambda x: x[17:])
    with open('primer.fa', 'w') as pw, open('primers_info.txt', 'w') as f:
        f.write(f"name_id\tFchrs\tFprimer_id\tFprimer\tFstart\tFend\tFstrand\t"
                f"Rchrs\tRprimer_id\tRprimer\tRstart\tRend\tRstrand\n")
        primer_f, primer_r = dict(), dict()
        for idx, row in primer.iterrows():
            if row.chr1== row.chr2 and row.start1 > row.start2:
                row.primer1, row.chr1, row.start1, row.end1, row.strand1, row.primer2, row.chr2,row.start2, row.end2,\
                row.strand2 = row.primer2, row.chr2,row.start2, row.end2, row.strand2, row.primer1, row.chr1,\
                              row.start1, row.end1, row.strand1
            if row.primer1 not in primer_f.keys():
                pw.write(f">{row.name_id}-F\n{row.primer1}\n")
                primer_f[row.primer1] = f"{row.name_id}-F"
                f_name = f"{row.name_id}-F"
            else:
                logging.info(f'{row.name_id} Fprimer and {primer_f[row.primer1]} are the same.')
                f_name  = primer_f[row.primer1]
            if row.primer2 not in primer_r.keys():
                pw.write(f">{row.name_id}-R\n{row.primer2}\n")
                primer_r[row.primer2] = f'{row.name_id}-R'
                r_name = f"{row.name_id}-R"
            else:
                logging.info(f'{row.name_id} Rprimer and {primer_r[row.primer2]} are the same')
                r_name = primer_r[row.primer2]

            f.write(f"{row.name_id}\t{row.chr1}\t{f_name}\t{row.primer1}\t{row.start1}\t{row.end1}\t{row.strand1}\t"
                    f"{row.chr2}\t{r_name}\t{row.primer2}\t{row.start2}\t{row.end2}\t{row.strand2}\n")

    blastdb = lambda x: f'{software.makeblastdb} -in {x}rimer.fa -dbtype nucl -out {x}idx && ' \
                        f'{software.makembindex} -iformat blastdb -input {x}idx'
    pipe.run_shell(blastdb('p'), 'build fprimer blastdb')

    primer.loc[:, 'amp_start'] = np.where(primer["strand1"] == "+", primer["start1"], primer["start2"])
    primer.loc[:, 'amp_end'] = np.where(primer["strand1"] == "+", primer["end2"], primer["end1"])
    primer.loc[:, 'amp_start1'] = np.where(primer["strand1"] == "+", primer["end1"]+1, primer["end2"]+1)
    primer.loc[:, 'amp_end1'] = np.where(primer["strand1"] == "+", primer["start2"]-1, primer["start1"]-1)

    bed_file = primer[primer.chr1 == primer.chr2][['chr1', 'amp_start1', 'amp_end1', 'name_id']]
    new_bed = get_unique_amp_bed(bed_file)
    new_bed.loc[:, 'amp_start'] = new_bed['amp_start'] - 1  # The first base in a chromosome is numbered 0 in bed file
    bed_file.loc[:, 'amp_start1'] = bed_file['amp_start1'] - 1
    bed_file.to_csv('primers.bed', sep='\t', index=False, header=False)
    os.system(f'{software.bedtools} sort -i primers.bed |{software.bedtools} merge -i - >cov_vcf.bed')
    new_bed.to_csv('primers_unique_region.bed', sep='\t', index=False, header=False)

    os.chdir(work_dir)


def get_unique_amp_bed(amp_df):
    # get the amplicons' unique region to evaluate the depth
    amp_dic = defaultdict(list)
    for idx, row in amp_df.iterrows():
        amp_dic[row.chr1].extend([_ for _ in range(int(row.amp_start1), int(row.amp_end1+1))])
    new_res = []
    # print(Counter(amp_dic['nCov']))
    chr_dic = {}
    for name in set(amp_df.chr1.values.tolist()):
        chr_dic[name] = Counter(amp_dic[name])
    for idd, row in amp_df.iterrows():
        counter = chr_dic[row.chr1]
        start, end = 0, row.amp_end1
        for idx in range(row.amp_start1, row.amp_end1+1):
            # print(row.chr, idx, counter[idx])
            if start == 0 and counter[idx] == 1:
                start = idx
            if start > 0 and counter[idx] > 1:
                end = idx - 1
                break
        # print(row.chr, start, end, row.name_id)
        if not start:  # the amplicon may covered by others amplicon.
            start = end
        new_res.append([row.chr1, start, end, row.name_id])
    df = pd.DataFrame(data=new_res, columns=['chr', 'amp_start', 'amp_end', 'name_id'])
    return df


def get_opt():
    """check and parsing the opts"""
    parser = argparse.ArgumentParser(prog='MultiPcrAnalysis',
                                     description="MultiPcrAnalysis: A analysis program with multiplex-PCR "
                                                 "sequencing data",
                                     usage="%(prog)s.py [options] -i sample_path_list_file -o primer_info_file", )
    parser.add_argument('-i', '--infile', nargs='?', type=argparse.FileType('r'), required=True,
                        help='[required] The sample path list file for multiple-PCR data. [file]')
    parser.add_argument('--samples', nargs="?", type=argparse.FileType('r'), required=True,
                        help="[optional] The samples' name file. [file]")
    parser.add_argument('-o', '--output_dir', type=str, required=False, default='output',
                        help="[Required] The project name for output folder path. [string]")
    parser.add_argument('--ref', type=str, required=False, default='hg19',
                        help="[optional] The reference prefix name, default = 'hg19'. [str]")
    parser.add_argument('--fqtype', type=str, choices=['PE100', 'PE150', 'SE100'], required=False, default='PE100',
                        help="[optional] The sample sequencing types, default = 'PE100'. [str]")
    parser.add_argument('--cut_r2', type=int, choices=[0, 1], default=0,
                        help="[optional] choose to cut the 10bp barcode in R2 tail, default=0. [0, 1]")
    parser.add_argument('-a', '--adapter', type=int, choices=[0, 1], default=0,
                        help='[optional] choose to cut adapter, default=1. [0, 1]')

    options = parser.parse_args()

    return options

def main():
    opt = get_opt()
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s',
                        level=logging.DEBUG,
                        filename=f'MultiPcrAnalysis.log',
                        filemode='w')

    logging.info("step0: build primer index")
    script_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
    init(script_dir)
    # path = os.getcwd()
    out_path = opt.output_dir
    if not os.path.exists(out_path):
        os.system(f'mkdir -p {out_path}')
    else:
        logging.info(f'{out_path} already exits.')
    out_path = os.path.abspath(out_path)
    logging.info(f"out_path: {out_path}")
    if not os.path.exists(out_path + '/database'):
        build_primer_index(out_path, opt.infile.name, opt.adapter)
        logging.info('build primer index have done')
    else:
        logging.info('primer index already exists.')
    try:
        sample_info = pd.read_csv(opt.samples.name, sep='\s+', header=None)
        sample_info.columns = ['sample_name', 'fq1file', 'fq2file'] if 'PE' in opt.fqtype else ['sample_name', 'fqfile']
    except IOError as e:
        raise e

    for idx, row in sample_info.iterrows():
        P = pipe.Pipeline(software, opt.ref, out_path, opt.fqtype, row[0], row[1], row[2])
        P.pipeline()

if __name__ == '__main__':
    main()