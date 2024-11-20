"""
Author: zhangyifan1
Date: 2024-06-05 18:53:52
LastEditors: zhangyifan1 zhangyifan1@genomics.cn
LastEditTime: 2024-06-05 20:00:40
FilePath: //undefinedd://000zyf//Learning//python_learn//Rosalind//01_Counting_DNA_Nucleotides.py
Description: Counting DNA Nucleotides

"""

import time

Sequence = "ACTTCGGGABCTTCGGGTGCAAACTTCGGGTGCAAACTTCGGGTGCAAACTTCGGGTGCAATGCAA"
# Method 1
start_time = time.time()
count_A = 0
count_C = 0
count_T = 0
count_G = 0
for base in Sequence:
    if base == "A":
        count_A += 1
    elif base == "T":
        count_T += 1
    elif base == "C":
        count_C += 1
    elif base == "G":
        count_G += 1
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Method1 Runtime: {elapsed_time} seconds")
print(f"A:{count_A} C:{count_C} T:{count_T} G:{count_G}")
# Method2
start_time = time.time()
base_dic = {}
for base in Sequence:
    if base not in base_dic:
        base_dic[base] = 1
    else:
        base_dic[base] += 1
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Method2 Runtime: {elapsed_time} seconds")
print(base_dic)
# 方法3：使用 collections.Counter
from collections import Counter

start_time = time.time()
base_counter = Counter(Sequence)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Method3 Runtime: {elapsed_time} seconds")
print(base_counter)

# 方法4：使用字符串的 count 方法
start_time = time.time()
count_A = Sequence.count("A")
count_C = Sequence.count("C")
count_T = Sequence.count("T")
count_G = Sequence.count("G")
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Method4 Runtime: {elapsed_time} seconds")
print(f"A:{count_A} C:{count_C} T:{count_T} G:{count_G}")

# Method 5 Biopython
from Bio.Seq import Seq

sequence = Seq(Sequence)
# 计数碱基
start_time = time.time()
count_A = sequence.count("A")
count_C = sequence.count("C")
count_T = sequence.count("T")
count_G = sequence.count("G")
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Method5 Runtime: {elapsed_time} seconds")
print(f"A:{count_A} C:{count_C} T:{count_T} G:{count_G}")
