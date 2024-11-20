"""
Author: zhangyifan1
Date: 2024-06-06 09:55:31
LastEditors: zhangyifan1 zhangyifan1@genomics.cn
LastEditTime: 2024-06-06 10:42:22
FilePath: //Rosalind//02_Transcribing DNA into RNA.py
Description: 

"""

import time
import random
from Bio.Seq import Seq


# Method 1
def DNA2RNA(Sequence):
    start_time = time.time()
    sequence_RNA = ""
    for base in Sequence:
        if base == "T":
            base = "U"
            sequence_RNA = sequence_RNA + base
        else:
            sequence_RNA += base
    end_time = time.time()
    runtime = end_time - start_time
    return sequence_RNA, runtime


# Method 2
def DNA2RNA_with_Bio(Sequence):
    start_time = time.time()
    dna_seq = Seq(Sequence)
    rna_seq = str(dna_seq.transcribe())
    end_time = time.time()
    runtime = end_time - start_time
    return rna_seq, runtime


# Method 3
def DNA2RNA_with_replace(Sequence):
    start_time = time.time()
    rna_seq = Sequence.replace("T", "U")
    end_time = time.time()
    runtime = end_time - start_time
    return rna_seq, runtime


# Method 4
def DNA2RNA_with_listjoin(Sequence):
    start_time = time.time()
    rna_list = ["U" if base == "T" else base for base in Sequence]
    rna_seq = "".join(rna_list)
    end_time = time.time()
    runtime = end_time - start_time
    return rna_seq, runtime


# Function to generate a random DNA sequence of a given length
def generate_random_dna_sequence(length):
    bases = "ATCG"
    return "".join(random.choice(bases) for _ in range(length))


def main():
    # Test sequence
    Sequence = "GATGGAACTTGACTACGTAAATT"
    # Method 1
    _, runtime1 = DNA2RNA(Sequence)
    # Method 2
    _, runtime2 = DNA2RNA_with_Bio(Sequence)
    # Method 3
    _, runtime3 = DNA2RNA_with_replace(Sequence)
    # Method 4
    _, runtime4 = DNA2RNA_with_listjoin(Sequence)

    print(f"Method 1 Runtime: {runtime1:.10f} seconds")
    print(f"Method 2 Runtime: {runtime2:.10f} seconds")
    print(f"Method 3 Runtime: {runtime3:.10f} seconds")
    print(f"Method 4 Runtime: {runtime4:.10f} seconds")

    # Generate a random DNA sequence for performance testing
    random_sequence_length = (
        1000000  # You can change this length for different tests
    )
    random_dna_sequence = generate_random_dna_sequence(random_sequence_length)

    print(f"\nTesting with a random DNA sequence of length {random_sequence_length}...")

    # Method 1 with random DNA sequence
    _, random_runtime1 = DNA2RNA(random_dna_sequence)

    # Method 2 with random DNA sequence
    _, random_runtime2 = DNA2RNA_with_Bio(random_dna_sequence)

    # Method 3 with random DNA sequence
    _, random_runtime3 = DNA2RNA_with_replace(random_dna_sequence)

    # Method 4 with random DNA sequence
    _, random_runtime4 = DNA2RNA_with_listjoin(random_dna_sequence)

    print(f"Method 1 Random Runtime: {random_runtime1:.10f} seconds")
    print(f"Method 2 Random Runtime: {random_runtime2:.10f} seconds")
    print(f"Method 3 Random Runtime: {random_runtime3:.10f} seconds")
    print(f"Method 4 Random Runtime: {random_runtime4:.10f} seconds")


if __name__ == "__main__":
    main()
