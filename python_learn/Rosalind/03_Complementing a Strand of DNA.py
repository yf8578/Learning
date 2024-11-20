"""
Author: zhangyifan1
Date: 2024-06-07 00:58:48
LastEditors: zhangyifan1 zhangyifan1@genomics.cn
LastEditTime: 2024-06-07 01:26:48
FilePath: //Rosalind//03_Complementing a Strand of DNA.py
Description: 

"""


# method 1
def replace_reverse(Sequence):
    reverse_seq = ""
    for base in Sequence:
        if base == "A":
            base = "T"
            reverse_seq += base
        elif base == "T":
            base = "A"
            reverse_seq += base
        elif base == "C":
            base = "G"
            reverse_seq += base
        elif base == "G":
            base = "C"
            reverse_seq += base
    print(reverse_seq)
    print("".join(reversed(reverse_seq)))#join() 是一个字符串方法，用于将一个可迭代对象（例如列表、元组或反向迭代器）中的元素连接成一个新的字符串。


# method 2
from Bio.Seq import Seq

def biopy_reverse(Sequence):
    seq = Seq(Sequence)
    reverse_complement = seq.reverse_complement()
    # print("Original Sequence: ", Sequence)
    print("Reverse Complement: ", str(reverse_complement))

def main():
    Sequence = "GGTTTCCCATGGTTGACATGATACAGAATTCGGCAGCCCGAAAGTACATGCTGTATGT"
    replace_reverse(Sequence)
    biopy_reverse(Sequence)


if __name__ == "__main__":
    main()
