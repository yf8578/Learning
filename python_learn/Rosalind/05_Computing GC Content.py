"""
Author: zhangyifan1
Date: 2024-06-08 23:46:01
LastEditors: zhangyifan1 zhangyifan1@genomics.cn
LastEditTime: 2024-06-09 18:44:58
FilePath: //Rosalind//05_Computing GC Content.py
Description: 

"""

# calculate the GC content and print the highest GC content and the sequence ID
# For this question, the first step is to parse the fasta format sequence. And I have two ideas to solve this --- traditional dictory to store the sequence or the profesisonal Python packages which is Biopython.

# Biopython
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction


def parse_seq(file_path):
    seq_dic = {}
    for seq_record in SeqIO.parse((file_path), "fasta"):
        print(f"{seq_record.id} done!!!")
        seq_dic[seq_record.id] = gc_fraction(seq_record) * 100
    # print(seq_dic)
    return seq_dic


def get_max_GC(seq_dic):
    max_gc_id = max(seq_dic, key=seq_dic.get)
    return max_gc_id, seq_dic[max_gc_id]


def main():
    file_path = r"D:\000zyf\Learning\python_learn\Rosalind\rosalind_gc.txt"
    id, gc = get_max_GC(parse_seq(file_path))
    print(id, gc)


if __name__ == "__main__":
    main()
