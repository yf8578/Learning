"""
@File   : CutPrimer_parallel.py
@Time   : 2022/7/7 17:41
@Author : Tian Chen
@Email  : chentian@genomics.cn
"""
import logging
import re
import os
import sys

from collections import defaultdict, Counter
from multiprocessing import Pool
from subprocess import Popen

import pandas as pd


ambiguous_dna_complement = {
    "a": "t",
    "c": "g",
    "g": "c",
    "t": "a",
    "A": "T",
    "C": "G",
    "G": "C",
    "T": "A",
    "N": "N",
}


def complement(seq):
    """Return the complement sequence"""
    return ''.join([ambiguous_dna_complement[base] for base in seq])


def reverse(seq):
    """Reverses a string given to it."""
    return seq[::-1]


def rev_com(seq):
    """Return the reverse_complement sequence"""
    com = complement(seq)
    rc = reverse(com)
    return rc


def edit_distance(seq1, seq2):
    """
    :param seq1: the head sequence of the read
    :param seq2: the primers
    :return: edit distance
    """
    lens = len(seq2) if len(seq2) < len(seq1) else len(seq1)
    seq1 = seq1[:lens]
    edit = [[i+j for j in range(lens+1)] for i in range(lens+1)]
    for i in range(1, lens+1):
        for j in range(1, lens+1):
            d = 0 if seq2[i-1] == seq1[j-1] else 1
            edit[i][j] = min(edit[i-1][j]+1, edit[i][j-1] + 1, edit[i-1][j-1]+d)
    # print(seq1, seq2, edit[lens][lens])

    return edit[lens][lens]



class Read2Primer:
    def __init__(self, prj_path, fprimer_dic, rprimer_dic, amp_name, primer_dic, cut_pri_flank=2):
        self.prj_path = prj_path
        self.f_dic = fprimer_dic
        self.r_dic = rprimer_dic
        self.amp_name = amp_name
        self.primer_dic = primer_dic
        self.cut_flank = cut_pri_flank
        # self.f_dic, self.r_dic, self.amp_name, self.primer_dic = self._build_primer_dict()

    def _gps_primer(self, read_info, is_rev):
        """
        find the alignment read's primer info.
        :param read_info: read alignment info
        :param reads_id: read1 or read2 id.
        :return:
        """
        cut_primer = False
        start, step = int(read_info[3]), 0
        for i in re.findall(r'(\d+)[DM]', read_info[5]):
            step += int(i)
        try:
            pos_lst = re.split(r'[;,]', re.search('XA:Z:(.*)', ' '.join(read_info[15:18])).group(1))
        except:
            pos_lst = []
        if not is_rev:  # sam_flag & 0x10 means is_reverse
            pos, ps_id, primers = start, 1, self.f_dic[str(read_info[2])]
        else:
            pos, ps_id, primers = start + step - 1, 2, self.r_dic[str(read_info[2])]

        other_aln, primer_name = [], ''
        for col in primers:
            primer_pos = col[ps_id]  # if read is reverse mapping, need to compare with Rend.
            #if primer_pos - self.cut_flank <= pos <= primer_pos + self.cut_flank:
            if col[1] - self.cut_flank <= pos <= col[2] + self.cut_flank:
                primer_name = col[0]
                if not is_rev:
                    cut_lens = col[-1] - (pos - primer_pos)
                else:
                    cut_lens = col[-1] + (pos - primer_pos)
                if cut_lens <= 0:
                    continue
                if read_info[0] == 'V350133018L1C001R01001283116':
                    print(read_info[0], col[0], col[-1], cut_lens, is_rev)
                cut_primer = cut_primer_se(read_info, cut_lens, is_rev)
                # cut_primer = cut_primer_se(read_info, col[-1], is_rev)
                break
        # if alignment info can't map to primer, find in second alignment info.
        if not primer_name and len(pos_lst) > 0:
            # other_aln.append(f"{read_info[2]}:{read_info[3]}:{read_info[5]}:{read_info[8]}")
            for i in range(0, len(pos_lst[:-1]), 4):
                start, step = int(pos_lst[i + 1][1:]), 0
                for dm in re.findall(r'(\d+)[DM]', pos_lst[i + 2]):
                    step += int(dm)
                if int(pos_lst[i+1]) < 0:  # reverse mapping
                    pos, ps_id, primers, is_rev = start + step - 1, 2, self.r_dic[pos_lst[i]], True
                else:
                    pos, ps_id, primers, is_rev = start, 1, self.f_dic[pos_lst[i]], False

                for col in primers:
                    primer_pos = col[ps_id]
                    if primer_pos - self.cut_flank <= pos <= primer_pos + self.cut_flank:
                        primer_name = col[0]
                        return [primer_name, other_aln, cut_primer, is_rev]
                other_aln.append(f"{pos_lst[i]}:{pos_lst[i+1]}:{pos_lst[i+2]}")
        else:
            other_aln = [f"{pos_lst[i]}:{pos_lst[i + 1]}:{pos_lst[i + 2]}" for i in range(0, len(pos_lst[:-1]), 4)]
        return [primer_name, other_aln, cut_primer, is_rev]

    def gps_se_primer(self, read_lst):
        idx = os.getpid()  # get the process id.
        fsam = open(self.prj_path+f'/tmp_sam/{idx}.sam', 'a+')
        ff = open(self.prj_path+f'/tmp_fa/{idx}_f.fa', 'a+')
        fr = open(self.prj_path+f'/tmp_fa/{idx}_r.fa', 'a+')
        fp = open(self.prj_path+f'/tmp_fa/{idx}_fp.txt', 'a+')
        rp = open(self.prj_path+f'/tmp_fa/{idx}_rp.txt', 'a+')
        for line in read_lst:
            read = line.strip().split()
            flag = int(read[1])
            if (flag & 0x100) or (flag & 0x800):  # not primary alignment or supplementary alignment
                continue
            if flag & 0x4:
                continue
            rev_flag = True if int(read[1]) & 0x10 else False
            aln_info = f'{read[2]}:{read[3]}:{read[5]}:{read[8]}'
            primer, other_info, cut_read, rev_flag = self._gps_primer(read, rev_flag)
            cut_read = cut_read if cut_read else read
            fsam.write("\t".join(cut_read) + "\n")

            if primer == '':
                #seq = rev_com(read[9])[:35] if int(read[1]) & 0x10 else read[9][:35]
                seq = rev_com(read[9])[:28] if int(read[1]) & 0x10 else read[9][:28]
                r = f'>{read[0]}\n{seq}\n'
                if rev_flag:
                    fr.write(r)
                else:
                    ff.write(r)
            if rev_flag:
                rp.write(f"{read[0]},{primer},{';'.join(other_info)},{aln_info}\n")
            else:
                fp.write(f"{read[0]},{primer},{';'.join(other_info)},{aln_info}\n")

        fsam.close()
        ff.close()
        fr.close()
        fp.close()
        rp.close()

    def _cat_file(self, prefix):
        os.system(f'cat {self.prj_path}/tmp_sam/*.sam >{self.prj_path}/{prefix}_cut.sam')
        os.system(f'cat {self.prj_path}/tmp_fa/*_f.fa >{self.prj_path}/cut_read_f.fa')
        os.system(f'cat {self.prj_path}/tmp_fa/*_r.fa >{self.prj_path}/cut_read_r.fa')
        os.system(f'cat {self.prj_path}/tmp_fa/*_fp.txt >{self.prj_path}/cut_read_fp.txt')
        os.system(f'cat {self.prj_path}/tmp_fa/*_rp.txt >{self.prj_path}/cut_read_rp.txt')
        os.system(f'rm -r {self.prj_path}/tmp_* &')



def cut_primer_se(read, cut_len, is_reverse):
    # read[3]: ref_start, read[5]: cigar, read[7]: mate_ref_start, read[8]:template_length, read[9]: seq, read[10]: qua,
    # read[11]: NM:i:(err_cnt), read[12]: MD:Z:(mapping)
    # is_reverse = int(read[1]) & 0x10
    start, new_seq, new_qua, md = int(read[3]), '', '', read[12].split(':')[-1]
    cigar_lst = re.findall(r'[0-9]+|[MDSI]+', read[5])
    md_lst = re.findall(r'[0-9]+|\^[ATCG]+|[ATCG]', md)
    new_md = rebulidMD(md_lst, is_reverse, cut_len)
    read[12] = "MD:Z:" + new_md
    len_cig = len(cigar_lst)

    if not is_reverse:
        for i in range(0, len_cig, 2):
            if cut_len > 0:
                if cigar_lst[i + 1] == 'M':
                    if int(cigar_lst[i]) >= cut_len:  # there is no mutations on primers
                        cigar_lst[i] = int(cigar_lst[i]) - cut_len
                        new_seq += read[9][cut_len:]
                        new_qua += read[10][cut_len:]
                        start += cut_len
                        cut_len -= cut_len
                        if int(cigar_lst[i]) == 0:
                            cigar_lst[i], cigar_lst[i + 1] = '', ''
                        break
                    else:  # cigar_lst[i] <= cut_len
                        read[9], read[10] = read[9][int(cigar_lst[i]):], read[10][int(cigar_lst[i]):]
                        cut_len -= int(cigar_lst[i])
                        start += int(cigar_lst[i])
                        cigar_lst[i], cigar_lst[i + 1] = '', ''
                        if cut_len == 0:
                            new_seq += read[9]
                            new_qua += read[10]
                            break

                elif cigar_lst[i + 1] == 'S':
                    new_seq, new_qua = new_seq + read[9][:int(cigar_lst[i])], new_qua + read[10][:int(cigar_lst[i])]
                    read[9], read[10] = read[9][int(cigar_lst[i]):], read[10][int(cigar_lst[i]):]
                elif cigar_lst[i + 1] == 'D':  # deletion will be reducing the primer length.
                    if int(cigar_lst[i]) <= cut_len:
                        cut_len -= int(cigar_lst[i])
                        cigar_lst[i], cigar_lst[i + 1] = '', ''
                        if cut_len == 0:
                            new_seq += read[9]
                            new_qua += read[10]
                            break
                    else:
                        cigar_lst[i] = int(cigar_lst[i]) - cut_len
                elif cigar_lst[i + 1] == 'I':  # insertion will be extending the primer length.
                    # cut_len += int(cigar_lst[i])
                    read[9], read[10] = read[9][int(cigar_lst[i]):], read[10][int(cigar_lst[i]):]
                    cigar_lst[i], cigar_lst[i + 1] = '', ''
            else:
                break
        # read[3], read[5], read[9], read[10] = start, ''.join(cigar_lst), new_seq, new_qua
    else:
        for i in range(len_cig - 1, -1, -2):
            if cigar_lst[i] == 'M':
                if int(cigar_lst[i - 1]) >= cut_len:  # there is no mutations on primers
                    cigar_lst[i - 1] = int(cigar_lst[i - 1]) - cut_len
                    #if read[0] == 'alpha7BPE1L1C006R00201944478':
                    #    print(cut_len, new_seq)
                    new_seq = read[9][:-cut_len] + new_seq
                    new_qua = read[10][:-cut_len] + new_qua
                    cut_len -= cut_len
                    if int(cigar_lst[i-1]) == 0:
                        cigar_lst[i - 1], cigar_lst[i] = '', ''
                    #if read[0] == 'alpha7BPE1L1C006R00201944478':
                    #    print(cut_len, new_seq)
                    break
                else:
                    #if read[0] == 'alpha7BPE1L1C006R00201944478':
                    #    print(cut_len, read[9])
                    read[9], read[10] = read[9][:-int(cigar_lst[i - 1])], read[10][:-int(cigar_lst[i - 1])]
                    cut_len -= int(cigar_lst[i - 1])
                    cigar_lst[i - 1], cigar_lst[i] = '', ''
                    #if read[0] == 'alpha7BPE1L1C006R00201944478':
                    #    print(cut_len, read[9])
            elif cigar_lst[i] == 'S':
                new_seq, new_qua = read[9][-int(cigar_lst[i - 1]):] + new_seq, read[10][-int(cigar_lst[i - 1]):] + new_qua
                read[9], read[10] = read[9][:-int(cigar_lst[i - 1])], read[10][:-int(cigar_lst[i - 1])]
            elif cigar_lst[i] == 'D':  # insertion will be reducing the primer length.
                if int(cigar_lst[i - 1]) <= cut_len:
                    cut_len -= int(cigar_lst[i - 1])
                    cigar_lst[i - 1], cigar_lst[i] = '', ''
                    if cut_len == 0:
                        new_seq = read[9] + new_seq
                        new_qua = read[10] + new_qua
                        break
                else:
                    cigar_lst[i - 1] = int(cigar_lst[i - 1]) - cut_len
            elif cigar_lst[i] == 'I':  # insertion will be extending the primer length.
                # cut_len += int(cigar_lst[i - 1])
                read[9], read[10] = read[9][:-int(cigar_lst[i - 1])], read[10][:-int(cigar_lst[i - 1])]
                cigar_lst[i - 1], cigar_lst[i] = '', ''

    read[11] = "NM:i:" + str(len(re.findall(r'[ATCG]+', new_md)))
    read[3], read[5], read[9], read[10] = str(start), ''.join(
        map(lambda x: str(x), cigar_lst)), new_seq, new_qua
    return read


def rebulidMD(md, is_reverse, cut_len):
    # md = ['5', '^', 'C', '46', 'T', '48']
    # md = ['4', 'C', '5', 'T', '84', '^', 'C', '5']
    if not is_reverse:
        for idx in range(len(md)):
            if md[idx] in 'ATCGN':
                if cut_len > 0:
                    md[idx] = ''
                    cut_len -= 1
            elif '^' in md[idx]:
                md[idx], md[idx + 1] = '', ''
            elif int(md[idx]) > cut_len:
                md[idx] = str(int(md[idx]) - cut_len)
                cut_len -= cut_len
                break
            elif int(md[idx]) < cut_len:
                cut_len -= int(md[idx])
                md[idx] = ''
    else:
        for idx in range(len(md) - 1, -1, -1):
            if md[idx] in 'ATCGN':
                if cut_len > 0:
                    md[idx] = ''
                    cut_len -= 1
            elif '^' in md[idx]:
                md[idx], md[idx + 1] = '', ''
            elif int(md[idx]) > cut_len:
                md[idx] = str(int(md[idx]) - cut_len)
                cut_len -= cut_len
                break
            elif int(md[idx]) < cut_len:
                cut_len -= int(md[idx])
                md[idx] = ''
    # print("".join(md))
    return "".join(md)


def load_sam_file(path, sam_hd, batch_size=100000):
    cnt, res = 1, []
    try:
        with open(path+'/tmp_sam/0_0.sam', 'w+') as f:
            data = sam_hd.readline()
            while data[0] == "@":
                f.write(data)
                data = sam_hd.readline()
        while data:
            if cnt > batch_size:
                # print(f"cnt: {cnt}")
                yield res
                cnt, res = 1, []
            res.append(data)
            data = sam_hd.readline()
            cnt += 1
        print(f"cnt: {cnt}")
        yield res
    except IOError:
        print("No found sam file")
        sys.exit(2)
    except:
        print("load sam file meet error")
        sys.exit(2)


def cut_primer(prj_path, sample_name, f_dic, r_dic, amp_name, primer_dict, cut_flank=5):
    if not os.path.exists(prj_path+'/tmp_sam'):
        os.system(f'mkdir -p {prj_path}/tmp_sam')
    else:
        os.system(f'rm -rf {prj_path}/tmp_sam && mkdir -p {prj_path}/tmp_sam')

    if not os.path.exists(prj_path+'/tmp_fa'):
        os.system(f'mkdir -p {prj_path}/tmp_fa')
    else:
        os.system(f'rm -rf {prj_path}/tmp_fa && mkdir -p {prj_path}/tmp_fa')
    sam_f = open(prj_path+f'/'+sample_name+'.sam', 'r', 1000000)
    rp = Read2Primer(prj_path, f_dic, r_dic, amp_name, primer_dict, cut_flank)
    # for reads in load_sam_file(prj_path, sam_f):
    #     rp.gps_se_primer(reads)
    #     break

    pool = Pool(8)
    for reads in load_sam_file(prj_path, sam_f):
        pool.apply_async(func=rp.gps_se_primer, args=(reads,))
    pool.close()
    pool.join()
    rp._cat_file(sample_name)

def test():
    read = "alpha7BPE1L1C006R00201944478    147     NM_019063.5     1917    46      76S20M4S        =       1678    -259    GCCAAAGACAGATAGATAATTCTGTGGGATCATCATCTCATTGGCTAAAGAGACATCATGGTTCCGGTTCGGTTTAGCACAATCAGAGCTGTAGCAAGTG    H33CD>?4=?1@8D/8CDCD2EC<FG9@D@G4F0C@HF2;=F<022;C:C6@C9=E0:1FH4EAG/C</H/57/F/FE=?CC<77HB;8D>B;A?CDHFF    NM:i:0  MD:Z:20 AS:i:20 XS:i:0"
    print(read)
    new_read = cut_primer_se(read.split(), 21, True)
    print(new_read)


if __name__ == '__main__':
    # script_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
    # gl.init(script_dir)
    filename, primer = 'test.sam', 'primers_info.txt'
    prj_path = '/hwfssz8/MGI_BIOINFO/USER/chentian/projects/Multi-PCR_Analysis/MultiPcrAnalysisV1.1/EML4-ALK/'
    test()
    # cut_primer(primer, prj_path, sam_f)
    # rp = Read2Primer(primerfile=primer, sample_name='test', prj_path=prj_path)
    # rp.output_primer_efficiency()
