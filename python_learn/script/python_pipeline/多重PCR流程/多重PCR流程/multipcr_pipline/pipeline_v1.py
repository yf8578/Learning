"""
@File   : pipeline.py
@Time   : 2022/8/15 16:17
@Author : Tian Chen
@Email  : chentian@genomics.cn
"""
import logging
import os
import sys
import asyncio
import re
import json
import time
import numpy as np
import pandas as pd

from subprocess import Popen, PIPE
from collections import Counter, defaultdict

import CutPrimer as cp


class JSONObject:
    def __init__(self, d):
        self.__dict__ = d


def init(code_dir):
    # global software
    with open(f'{code_dir}/software.json', 'r') as f:
        data = json.dumps(json.load(f))
    software = json.loads(data, object_hook=JSONObject)
    return software

def run_shell(cmd: str, msg: str):
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if p.poll():
        logging.error(f'{msg} get an error as fllows:\n{stderr.decode("utf-8")}')
        sys.exit(2)
    else:
        logging.info(f'{msg} have been done.')


class JSONObject:
    def __init__(self, d):
        self.__dict__ = d


def init(code_dir):
    global software
    with open(f'{code_dir}/software.json', 'r') as f:
        data = json.dumps(json.load(f))
    software = json.loads(data, object_hook=JSONObject)


def build_primer_index_old(path: str, primer_file: str, adapter_flag: bool):
    """
    primer_file column: name_id,chr,primer1_name,primer1,start1,end1,strand1,primer2_name,primer2,start2,end2,strand2
    """
    work_dir = os.getcwd()
    cmd = f'mkdir -p {path}/database && cp -p {primer_file} {path}/database'
    run_shell(cmd, 'create database')
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
    with open('fprimer.fa', 'w') as fw, open('rprimer.fa', 'w') as rw, open('primers_info.txt', 'w') as f:
        f.write(f"name_id\tchrs\tFprimer_id\tFprimer\tFstart\tFend\tFstrand\t"
                f"Rprimer_id\tRprimer\tRstart\tRend\tRstrand\n")
        for idx, row in primer.iterrows():
            if row.start1 < row.start2:
                fw.write(f">{row.primer1_name}\n{row.primer1}\n")
                rw.write(f">{row.primer2_name}\n{row.primer2}\n")
                f.write(f"{row.name_id}\t{row.chr1}\t{row.primer1_name}\t{row.primer1}\t{row.start1}\t{row.end1}\t{row.strand1}\t"
                        f"{row.chr2}\t{row.primer2_name}\t{row.primer2}\t{row.start2}\t{row.end2}\t{row.strand2}\n")
            else:
                rw.write(f">{row.primer1_name}\n{row.primer1}\n")
                fw.write(f">{row.primer2_name}\n{row.primer2}\n")
                f.write(f"{row.name_id}\t{row.chr2}\t{row.primer2_name}\t{row.primer2}\t{row.start2}\t{row.end2}\t{row.strand2}\t"
                        f"{row.chr2}\t{row.primer1_name}\t{row.primer1}\t{row.start1}\t{row.end1}\t{row.strand1}\n")
    blastdb = lambda x: f'{gl.software.makeblastdb} -in {x}primer.fa -dbtype nucl -out {x}idx && ' \
                        f'{gl.software.makembindex} -iformat blastdb -input {x}idx'
    run_shell(blastdb('f'), 'build fprimer blastdb')
    run_shell(blastdb('r'), 'build rprimer blastdb')

    primer.loc[:, 'amp_start'] = np.where(primer["strand1"] == "+", primer["start1"], primer["start2"])
    primer.loc[:, 'amp_end'] = np.where(primer["strand1"] == "+", primer["end2"], primer["end1"])
    primer.loc[:, 'amp_start1'] = np.where(primer["strand1"] == "+", primer["end1"]+1, primer["end2"]+1)
    primer.loc[:, 'amp_end1'] = np.where(primer["strand1"] == "+", primer["start2"]-1, primer["start1"]-1)

    bed_file = primer[primer.chr1 == primer.chr2][['chr1', 'amp_start1', 'amp_end1', 'name_id']]
    new_bed = get_unique_amp_bed(bed_file)
    new_bed.loc[:, 'amp_start'] = new_bed['amp_start'] - 1  # The first base in a chromosome is numbered 0 in bed file
    bed_file.loc[:, 'amp_start1'] = bed_file['amp_start1'] - 1
    bed_file.to_csv('primers.bed', sep='\t', index=False, header=False)
    os.system(f'{gl.software.bedtools} sort -i primers.bed |{gl.software.bedtools} merge -i - >cov_vcf.bed')
    new_bed.to_csv('primers_unique_region.bed', sep='\t', index=False, header=False)

    os.chdir(work_dir)


def load_read_primer_info(path, tag):
    try:
        df = pd.read_csv(path + f'/cut_read_{tag}p.txt', sep=',', header=None)
        df.columns = ['read_id', f'{tag}_amp_name', f'{tag}_other_aln', f'{tag}_aln_info']
    except IOError as e:
        raise e
    return df


def load_read_primer_bias(path, tag):
    try:
        df = pd.read_csv(path + f'/cut_read_{tag}.blast', sep='\s+', header=None)
        df.columns = ['read_id', f'{tag}_primer_name']
        df.drop_duplicates(subset=['read_id'], inplace=True)
    except IOError as e:
        raise e
    return df

class dimer_evaluate:
    def __init__(self,sample_path, sample_name, fqtype="PE"):
        self.path = sample_path
        self.prefix = sample_name
        self.fqtype = fqtype

    def __generate_dimer_info(self, fp, rp, dimer_dict):
        with open(fp, 'r') as f1, open(rp, 'r') as f2:
            aln_f = f1.readlines()
            aln_r = f2.readlines()
        for line1 in aln_f:
            f_info = line1.strip().split()
            dimer_dict[f_info[0]].append(f_info[1])
        for line2 in aln_r:
            r_info = line2.strip().split()
            dimer_dict[r_info[0]].append(r_info[1])
            
        print(dimer_dict.values())
        try:
            dimer_info = pd.DataFrame(data=list(dimer_dict.values()),
                                      columns=['dimer', 'r1_ratio', 'r2_ratio', 'r1_primer', 'r2_primer'])
            dimer_info.to_csv(f'{self.path}/dimer_info.csv', index=False)
        except:
            logging.info(f"{self.prefix} find dimer info failed")

    def __cal_dimer_seq_rate(self, tag):
        try:
            df = pd.read_csv(f'{self.path}/reads{tag}_adapter_sort.txt', sep='\s+', header=None)
            df.columns = ['count', 'dimer']
        except OSError:
            logging.error(f"{self.prefix} Load adapter_sort file failed")
            sys.exit(2)
        total_count = df['count'].sum()
        df['ratio'] = df['count'].apply(lambda x: round(x / total_count, 4))
        df = df[['dimer', 'count', 'ratio']]
        df.to_csv(f'{self.path}/reads{tag}_adapter_sort.csv', index=False)
        os.system(f'rm {self.path}/reads{tag}_adapter_sort.txt')

    def __pe_ada_fa(self, rate_threshold= 0.05):
        dimer1 = pd.read_csv(f"{self.path}/reads_1_adapter_sort.csv")
        dimer1 = dimer1[dimer1['ratio'] >= rate_threshold]
        dimer2 = pd.read_csv(f'{self.path}/reads_2_adapter_sort.csv')
        dimer2 = dimer2[dimer2['ratio'] >= rate_threshold]
        cnt = 0
        f1 = open(f'{self.path}/severe_dimer_r1.fa', 'w')
        f2 = open(f'{self.path}/severe_dimer_r2.fa', 'w')
        dimer = defaultdict(list)
        for seq1, seq2 in zip(dimer1.values, dimer2.values):
            cnt += 1
            if seq1[0] == cp.rev_com(seq2[0]):
                dimer[f'dimer{cnt}'].extend([seq1[0], seq1[-1], seq2[-1]])
                cut_len = 20 if len(seq1[0]) > 20 else None
                f1.write(f">dimer{cnt}\n{seq1[0][:cut_len]}\n")
                f2.write(f">dimer{cnt}\n{seq2[0][:cut_len]}\n")
            else:
                dimer[f'dimer{cnt}'].extend([seq1[0], seq1[-1], None])
                cut_len1 = 20 if len(seq1[0]) > 20 else None
                f1.write(f">dimer{cnt}\n{seq1[0][:cut_len1]}\n")
                f2.write(f">dimer{cnt}\n{cp.rev_com(seq1[0][:cut_len1])}\n")
                cnt += 1
                cut_len2 = 20 if len(seq2[0]) > 20 else None
                f1.write(f">dimer{cnt}\n{cp.rev_com(seq2[0][:cut_len2])}\n")
                f2.write(f">dimer{cnt}\n{seq2[0][:cut_len2]}\n")
                dimer[f'dimer{cnt}'].extend([seq2[0], None, seq2[-1]])
        f1.close()
        f2.close()
        return dimer


    def __se_ada_fa(self, rate_threshold= 0.05):
        dimer1 = pd.read_csv(f"{self.path}/reads_adapter_sort.csv")
        dimer1 = dimer1[dimer1['ratio'] >= rate_threshold]
        cnt = 0
        f1 = open(f'{self.path}/severe_dimer_r1.fa', 'w')
        f2 = open(f'{self.path}/severe_dimer_r2.fa', 'w')
        dimer = defaultdict(list)
        for seq1 in dimer1.values:
            cnt += 1
            dimer[f'dimer{cnt}'].extend([seq1[0], seq1[-1], None])
            f1.write(f">dimer{cnt}\n{seq1[0]}\n")
            f2.write(f">dimer{cnt}\n{cp.rev_com(seq1[0])}\n")
        f1.close()
        f2.close()
        return dimer

    def _run_blast(self, blastn, res_dir, tag, thread=4):
        cmd = f'{blastn} -query {self.path}/severe_dimer_{tag}.fa -db {res_dir}/database/pidx -num_threads {thread} ' \
              f'-task blastn -word_size 11 -max_target_seqs 2 -dust no -outfmt "6 qseqid sseqid ' \
               f'pident  length mismatch gapopen qstart qend sstart send" | sort -nrk 4 -|awk \'$7<3&&$9<3\' -| ' \
               f'cut -f1,2 >{self.path}/{tag}_adap_ori.blast'
        return cmd

    def get_adapter_type(self, blastn, prj_path, dimer_threshold=0.05):
        dimer_seq = lambda x: f'grep -v "^>" {self.path}/{self.prefix}{x}.adapt.fa |sort|uniq -c|sort -nrk 1 >{self.path}/reads{x}_adapter_sort.txt'
        if self.fqtype == 'PE':
            d1 = Popen(dimer_seq('_1'), shell=True)
            d2 = Popen(dimer_seq('_2'), shell=True)
            d1.wait()
            d2.wait()
            self.__cal_dimer_seq_rate('_1')
            self.__cal_dimer_seq_rate('_2')
            dimer_dict = self.__pe_ada_fa(dimer_threshold)
        else:
            run_shell(dimer_seq(''), f'{self.prefix} count dimer')
            self.__cal_dimer_seq_rate('')
            dimer_dict = self.__se_ada_fa(dimer_threshold)

        fa1 = Popen(self._run_blast(blastn, prj_path, 'r1', 4), shell=True)
        fa2 = Popen(self._run_blast(blastn, prj_path, 'r2', 4), shell=True)
        fa1.wait()
        fa2.wait()
        self.__generate_dimer_info(f'{self.path}/r1_adap_ori.blast', f'{self.path}/r2_adap_ori.blast', dimer_dict)


class Primer:
    def __init__(self, name, fchr, rchr, start, end):
        self.name = name
        self.fchr = fchr
        self.rchr = rchr
        self.start = start
        self.end = end
        self.amp_len = end - start + 1 if fchr == rchr else None
        self.fr_cnt = 0
        self.f_cnt = 0
        self.r_cnt = 0
        self.f_bias = 0
        self.r_bias = 0
        self.f_other = []
        self.r_other = []


class Pipeline:
    def __init__(self, software, ref, prj_path, fqtypes, sample_name, fq1, fq2=None, threads_num=8, dimer_thres=0.05,
                 primer_flank=5):
        #self.soft = init(code_dir)
        self.soft = software
        self.name = sample_name
        self.prj_path = prj_path
        self.sample_path = prj_path + '/' + self.name
        self.fq1 = fq1
        self.fq2 = fq2
        self.ref = ref
        self.fqtype, self.fqlen = fqtypes[:2], int(fqtypes[2:])
        self.threads = threads_num
        self.d_th = dimer_thres
        self.p_flk = primer_flank

    def __build_primer_dict(self):
        try:
            data = pd.read_csv(self.prj_path+'/database/primers_info.txt', sep='\t')
        except IOError:
            logging.info(f"load primer_dict failed")
            print(f"No found {self.prj_path}/database/primers_info.txt, load primer_dict failed")
            sys.exit(2)
        f_dic, r_dic = defaultdict(list), defaultdict(list)
        f_name, r_name = set(), set()
        data.loc[:, "Flen"] = data['Fend'] - data['Fstart'] + 1
        data.loc[:, 'Rlen'] = data['Rend'] - data['Rstart'] + 1
        amp_name_dic, primer_dict = dict(), dict()
        for idx, row in data.iterrows():
            amp_key = f'{row.Fprimer_id}:{row.Rprimer_id}'
            if row.Fprimer_id not in f_name:
                f_dic[row.Fchrs].append([row.Fprimer_id, row.Fstart, row.Fend, row.Flen])
                f_name.add(row.Fprimer_id)
            if row.Rprimer_id not in r_name:
                r_dic[row.Rchrs].append([row.Rprimer_id, row.Rstart, row.Rend, row.Rlen])
                r_name.add(row.Rprimer_id)
            amp_name_dic[amp_key] = row.name_id
            primer_dict[row.name_id] = Primer(row.name_id, row.Fchrs, row.Rchrs, row["Fstart"], row["Rend"])
        return f_dic, r_dic, amp_name_dic, primer_dict

    def __merge_primer_aln_info(self):
        fp_aln = load_read_primer_info(self.sample_path, tag='f')
        rp_aln = load_read_primer_info(self.sample_path, tag='r')
        fp_aln = fp_aln.merge(rp_aln, left_on='read_id', right_on='read_id', how='left')
        f_p = load_read_primer_bias(self.sample_path, tag='f')
        r_p = load_read_primer_bias(self.sample_path, tag='r')
        fp_aln = fp_aln.merge(f_p, left_on='read_id', right_on='read_id', how='left')
        fp_aln = fp_aln.merge(r_p, left_on='read_id', right_on='read_id', how='left')
        fp_aln.to_csv(self.sample_path + '/sam2primerInfo.csv', index=False)
        fp_aln.fillna(value=False, inplace=True)

        return fp_aln.values

    def __output_primer_efficiency(self, sam2primer_lst, amp_names, primer_dic):
        # sam2primerInfo.csv: '1': Fprimer_name, '2': Rprimer_name, '3':F_bias, '4': R_bias,
        # '5': [other_info_F], '6': [other_info_R], '7': F_aln_info, '8': R_aln_info
        unexpected_dict = defaultdict(list)
        for row in sam2primer_lst:
            # print(row)
            amp_name = f'{row[1]}:{row[4]}'
            if row[1] and row[4]:
                if amp_name in amp_names.keys():
                    primer_dic[amp_names[amp_name]].fr_cnt += 2
                else:
                    primer_dic[row[1][:-2]].f_cnt += 1
                    primer_dic[row[4][:-2]].r_cnt += 1
                if row[2]:
                    primer_dic[row[1][:-2]].f_other.extend(row[2].split(';'))
                if row[5]:
                    primer_dic[row[4][:-2]].r_other.extend(row[5].split(';'))
            elif not row[1] and not row[4]:
                if row[7] and row[8]:
                    primer_dic[row[7][:-2]].f_bias += 1
                    primer_dic[row[8][:-2]].r_bias += 1
                unexpected_dict[f'{row[7]}:{row[8]}'].append(f'{row[3]}-{row[6]}')
            elif row[1] and not row[4]:
                primer_dic[row[1][:-2]].f_cnt += 1
                if row[8]:
                    primer_dic[row[8][:-2]].r_bias += 1
                unexpected_dict[f'{row[1]}:{row[8]}'].append(f'{row[3]}-{row[6]}')
            elif not row[1] and row[4]:
                primer_dic[row[4][:-2]].r_cnt += 1
                if row[7]:
                    primer_dic[row[7][:-2]].f_bias += 1
                unexpected_dict[f'{row[7]}:{row[4]}'].append(f'{row[3]}-{row[6]}')

        res_lst = list()
        for amp_name, sub in primer_dic.items():
            f_other = str(Counter(sub.f_other).most_common(5))[1:-1]
            r_other = str(Counter(sub.r_other).most_common(5))[1:-1]
            res_lst.append([sub.name, sub.fchr, sub.rchr, sub.start, sub.end, sub.amp_len, sub.fr_cnt, sub.f_cnt,
                            sub.r_cnt, sub.f_bias, sub.r_bias, f_other, r_other])
        result = pd.DataFrame(data=res_lst, columns=['amp_name', 'fchr', 'rchr', 'amp_start', 'amp_end', 'amp_len',
                                                     'fr_cnt', 'f_cnt', 'r_cnt', 'f_bias', 'r_bias', 'f_other',
                                                     'r_other'])
        result['target_reads_cnt'] = result['fr_cnt'] + result['f_cnt'] + result['r_cnt']
        result['primer_reads'] = result['target_reads_cnt'] + result['f_bias'] + result['r_bias']
        result['primer_efficiency(%)'] = result['target_reads_cnt'] / (result['primer_reads'] + 1)
        result['primer_efficiency(%)'] = result['primer_efficiency(%)'].apply(lambda x: round(x * 100, 2))
        result = result[
            ['amp_name', 'fchr', 'rchr', 'amp_start', 'amp_end', 'amp_len', 'target_reads_cnt', 'fr_cnt',
             'f_cnt', 'r_cnt', 'f_bias', 'r_bias', 'primer_reads', 'primer_efficiency(%)', 'f_other',
             'r_other']]
        result.to_excel(f"{self.sample_path}/{self.name}_efficiency.xlsx", index=False)
        unexpected = []
        for key, value in unexpected_dict.items():
            unexpected.append([key, len(value), str(Counter(value).most_common(4))[1:-1]])
        result2 = pd.DataFrame(data=unexpected, columns=['fprimer:rprimer', 'count', 'top4 info'])
        result2.sort_values(by='count', ascending=False, inplace=True)
        result2.to_excel(f"{self.sample_path}/{self.name}_unexpected.xlsx", index=False)

        return result['target_reads_cnt'].sum()

    def __get_summary_indicator(self, map_reads, map_target_reads):
        res = [self.name]
        with open(f'{self.sample_path}/fastp.json', 'r') as f:
            fastp = json.load(f)
        raw_data = fastp["summary"]["before_filtering"]["total_reads"]
        q30 = round(fastp["summary"]["before_filtering"]["q30_rate"]*100, 2)
        # gc = round(fastp["summary"]["before_filtering"]["gc_content"]*100, 2)
        dup_rate = round(fastp["duplication"]["rate"]*100, 2)
        with open(f'{self.sample_path}/{self.name}.qc.log') as f:
            logs = f.readlines()
        ada_rate, clean_reads = 0, 0
        for line in logs[53:]:
            if 'Total written' in line:
                clean = re.findall(r':\s+(.*)\s+bp\s+\((.*)%\)', line.strip())[0]
                clean_reads, ada_rate = int(int(clean[0].replace(',', ''))/100), round(100 - float(clean[1]), 2)
                break
        try:
            base_depth = pd.read_csv(f"{self.sample_path}/{self.name}_base.depth.txt", sep='\t', header=None)
            base_depth.columns = ['chr', 'pos', 'depth']

        except IOError as e:
            logging.error(f"load {self.name}_base.depth.txt file failed!")
            sys.exit(2)
        avg = round(base_depth['depth'].mean(), 2)
        total_base = len(base_depth)
        uniformity = round(len(base_depth[base_depth['depth'] > 0.1 * avg]) / total_base * 100, 2)
        res.extend([raw_data, q30, dup_rate, ada_rate, clean_reads, avg, uniformity])
        map_rate = round(map_reads / clean_reads * 100, 2)
        target_map_rate = round(map_target_reads / map_reads * 100, 2)
        res.extend([map_rate, target_map_rate])
        for i in [1, 4, 10, 30, 100]:
            res.append(round(len(base_depth[base_depth['depth'] >= i]) / total_base * 100, 2))
        if ada_rate >= 10:
            dimer = dimer_evaluate(self.sample_path, self.name, self.fqtype)
            dimer.get_adapter_type(self.soft.blastn, self.prj_path, self.d_th)
        with open(f'{self.sample_path}/summary.csv', 'w') as f:
            f.write('sample_name\traw_reads\tQ30(%)\tdup_rate(%)\tdimer_rate(%)\tclean_reads\tavg_depth\tuniformuty(>0.1x)'
                    '\tmap_rate(%)\tmap_target_rate(%)\tcov_1x(%)\tcov_4x(%)\tcov_10x(%)\tcov_30x(%)\tcov_100x(%)\n')
            f.write('\t'.join([str(_) for _ in res]))

    def _run_fastp(self):

        cmd1 = f'{self.soft.fastp}  -i  {self.fq1} -o {self.sample_path}/{self.name}_1.fastq -I {self.fq2} ' \
               f'-O {self.sample_path}/{self.name}_2.fastq -w {self.threads} -A -j {self.sample_path}/fastp.json ' \
               f'-h {self.sample_path}/{self.name}.fp.html 2>{self.sample_path}/{self.name}.qc.log'
        cmd2 = f'{self.soft.fastp} -i {self.fq1} -o {self.sample_path}/{self.name}.fastq ' \
               f'-w {self.threads} -A -j {self.sample_path}/fastp.json ' \
               f'-h {self.sample_path}/{self.name}.fp.html 2>{self.sample_path}/{self.name}.qc.log'

        if self.fqtype == 'PE':
            run_shell(cmd1, f'{self.name} step1: run fastp')
        else:
            run_shell(cmd2, f'{self.name} step1: run fastp')

    def _run_cutadapt(self):
        adapter1 = 'AAGTCGGAGGCCAAGCGGTCTTAGGAAGACAA'
        adapter2 = 'AAGTCGGATCGTAGCCATGTCGTTC'

        cmd1 = f"{self.soft.cutadapt} -a {adapter1} -A {adapter2} -e 0.12 -j {self.threads} -O 8 -m {self.fqlen} " \
               f"--discard-trimmed --pair-filter=any --too-short-output {self.sample_path}/{self.name}_1.adapt.fq " \
               f"--too-short-paired-output {self.sample_path}/{self.name}_2.adapt.fq " \
               f"-o {self.sample_path}/{self.name}_1.fq -p {self.sample_path}/{self.name}_2.fq " \
               f"{self.sample_path}/{self.name}_1.fastq {self.sample_path}/{self.name}_2.fastq " \
               f">>{self.sample_path}/{self.name}.qc.log"
        cmd2 = f"{self.soft.cutadapt} -a {adapter1} -A {adapter2} -e 0.12 -j {self.threads} -O 8 -m {self.fqlen} " \
               f"--discard-trimmed --too-short-output {self.sample_path}/{self.name}.adapt.fa " \
               f"-o {self.sample_path}/{self.name}.fq  {self.sample_path}/{self.name}.fastq " \
               f">>{self.sample_path}/{self.name}.qc.log"

        if self.fqtype == 'PE':
            run_shell(cmd1, f'{self.name} step2: run cutadapt')
        else:
            run_shell(cmd2, f'{self.name} step2: run cutadapt')

    def _run_bwa_sam(self):
        cmd1 = f'{self.soft.bwa} mem -t {self.threads} {self.ref} ' \
               f'{self.sample_path}/{self.name}_1.fq {self.sample_path}/{self.name}_2.fq  ' \
               f'1>{self.sample_path}/{self.name}.sam'
        cmd2 = f'{self.soft.bwa} mem -t {self.threads} -r 1 {self.ref} {self.sample_path}/{self.name}.fq   ' \
               f'1>{self.sample_path}/{self.name}.sam'

        if self.fqtype == 'PE':
            run_shell(cmd1, f'{self.name} step3: run bwa to generate sam file')
        else:
            run_shell(cmd2, f'{self.name} step3: run bwa to generate sam file')

    def _run_blast(self, tag, thread):
        cmd = f'{self.soft.blastn} -task blastn-short -query {self.sample_path}/cut_read_{tag}.fa -db {self.prj_path}/database/pidx ' \
               f'-num_threads {thread}  -word_size 11 -evalue 0.001 -max_target_seqs 2 -dust no -outfmt "6 qseqid sseqid ' \
               f'pident  length mismatch gapopen qstart qend sstart send" | sort -nrk 4 -|awk \'$7<3&&$9<3\' -| ' \
               f'cut -f1,2 >{self.sample_path}/cut_read_{tag}.blast'
        return cmd

    def _cut_primer(self, cut_flank=5):
        if not os.path.exists(f'{self.sample_path}/sam2primerInfo.csv'):
            f_dic, r_dic, amp_name, primer_dic = self.__build_primer_dict()
            # print(f_dic, r_dic, amp_name, primer_dic)
            if not os.path.exists(f'{self.sample_path}/cut_read_fp.txt'):
                cp.cut_primer(self.sample_path, self.name, f_dic, r_dic, amp_name, primer_dic, cut_flank)
            logging.info(f'{self.name} step4-1: run cut_primers have been done.')
            logging.info(f"{self.name} step5: run sam2bam start")
            # sam2bam = Popen(self._sam2bam(), shell=True)
            blast_f = Popen(self._run_blast('f', 4), shell=True)
            blast_r = Popen(self._run_blast('r', 4), shell=True)
            blast_f.wait()
            blast_r.wait()
            if blast_f.poll():
                logging.error(f"{self.name} run blastn meet some error")
                sys.exit(2)
            logging.info(f"{self.name} step4-2: start to get amplify efficiency")
            fp_aln = self.__merge_primer_aln_info()
        else:
            logging.info(f"{self.name} step4-1: run cut_primer had been done.")
            logging.info(f"{self.name} step5: run sam2bam start")
            # sam2bam = Popen(self._sam2bam(), shell=True)
            logging.info(f"{self.name} step4-2: start to get amplify efficiency")
            f_dic, r_dic, amp_name, primer_dic = self.__build_primer_dict()
            dtypes = {"read_id": str, "f_amp_name": str, "f_other_aln": str, "f_aln_info": str,
                      "r_amp_name": str, "r_other_aln": str, "r_aln_info": str, "f_primer_name": str, "r_primer_name":str}
            fp_aln = pd.read_csv(f'{self.sample_path}/sam2primerInfo.csv', dtype=dtypes)
            fp_aln.fillna(value=False, inplace=True)
        total_read = len(fp_aln) * 2
        unmap_f, unmap_r = len(fp_aln[fp_aln['f_aln_info'] == False]), len(fp_aln[fp_aln['r_aln_info'] == False])
        map_reads = total_read - unmap_f - unmap_r
        map_target_reads = self.__output_primer_efficiency(fp_aln.values, amp_name, primer_dic)
        logging.info(f"{self.name} step4-2: got amplify efficiency successfully!")
        # sam2bam.wait()
        logging.info(f"{self.name} step5:  run sam2bam have been done.")
        logging.info(f"{self.name} step6:  run freebayes start")
        # freebayes = Popen(self._run_freebayes(thread=6), shell=True)
        depth1 = Popen(self._run_bedtools_depth('primers.bed', self.name+'.depth.txt'), shell=True)
        depth2 = Popen(self._run_bedtools_depth('primers_unique_region.bed', self.name+'_uniq.depth.txt'), shell=True)
        base_depth = Popen(self._run_samtools_depth(), shell=True)
        depth1.wait()
        depth2.wait()
        base_depth.wait()
        if base_depth.poll():
            logging.error(f"{self.name} get depth meet error")
            sys.exit(2)
        logging.info(f"{self.name} step7:  start to generate summary report.")
        self.__get_summary_indicator(map_reads, map_target_reads)
        logging.info(f"{self.name} step7:  generate summary report successfully!")
        # freebayes.wait()
        logging.info(f"{self.name} step6:  run freebayes start")
        # if freebayes.poll():
        #     logging.error(f"{self.name} run freebayes meet error")
        #     sys.exit(2)
        logging.info(f"{self.name} step6: run freebayes have been done.")

    def _sam2bam(self):
        cmd = f'{self.soft.samtools} view -bSu {self.sample_path}/{self.name}_cut.sam | {self.soft.samtools} sort ' \
              f'1>{self.sample_path}/{self.name}.bam 2>>{self.sample_path}/bwa.log'
        return  cmd

    def _run_bedtools_depth(self, bed_name, output_name):
        cmd = f'{self.soft.bedtools} coverage -mean -a {self.prj_path}/database/{bed_name} -b ' \
              f'{self.sample_path}/{self.name}.bam >{self.sample_path}/{output_name}'
        return cmd

    def _run_samtools_depth(self):
        cmd = f'{self.soft.samtools} depth -d 100000000 -a -b {self.prj_path}/database/cov_vcf.bed ' \
              f'{self.sample_path}/{self.name}.bam >{self.sample_path}/{self.name}_base.depth.txt'
        return cmd

    def _run_freebayes(self, thread, paras='-p 1 -q 20 --min-coverage 10 -F 0.3'):
        cmd = f'{self.soft.freebayes} -t {self.prj_path}/database/cov_vcf.bed {paras} -f {self.ref} ' \
              f'{self.sample_path}/{self.name}.bam 1>{self.sample_path}/{self.name}.raw.vcf && {self.soft.bcftools} ' \
              f'view --include "QUAL>=100" {self.name}.raw.vcf >{self.name}.vcf'
        return cmd

    def pipeline(self):
        if not os.path.exists(self.sample_path):
            run_shell(f'mkdir -p {self.sample_path}', f'create {self.sample_path} directory')
        else:
            logging.warning(f"{self.sample_path} already exists!")
        # step1: QC.
        if not os.path.exists(f'{self.sample_path}/{self.name}.qc.log'):
            logging.info(f"{self.name} step1: run fastp start")
            self._run_fastp()
        else:
            logging.info(f"{self.name} step1 run fastp had been done.")
        # step2: filter dimer data.
        if not os.path.exists(f'{self.sample_path}/{self.name}_1.adapt.fa') and \
                not os.path.exists(f'{self.sample_path}/{self.name}.adapt.fa'):
            logging.info(f"{self.name} step2: run cutadapt start")
            self._run_cutadapt()
            logging.info(f"{self.name} step2: run cutadapt finish!")
        else:
            logging.info(f"{self.name} step2 run-cutadapt had been done.")
        # step3: alignment.
        if not os.path.exists(f'{self.sample_path}/{self.name}.sam'):
            logging.info(f"{self.name} step3: run bwa start")
            self._run_bwa_sam()
        else:
            logging.info(f"{self.name} step3 run bwa had been done.")
        # step4: cut_primers
        logging.info(f"{self.name} step4-1: run cut_primers start")
        self._cut_primer(self.p_flk)
