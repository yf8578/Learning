"""
Author: zhangyifan1
Date: 2024-06-06 10:44:22
LastEditors: zhangyifan1 zhangyifan1@genomics.cn
LastEditTime: 2024-06-06 10:46:50
FilePath: //Rosalind//test.py
Description: 

"""

import time
import random
import matplotlib.pyplot as plt
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


# Function to measure runtimes for different methods and sequence lengths
def measure_runtimes(sequence_lengths):
    runtimes = {
        "Method 1": [],
        "Method 2": [],
        "Method 3": [],
        "Method 4": [],
    }

    for length in sequence_lengths:
        seq = generate_random_dna_sequence(length)
        _, runtime1 = DNA2RNA(seq)
        _, runtime2 = DNA2RNA_with_Bio(seq)
        _, runtime3 = DNA2RNA_with_replace(seq)
        _, runtime4 = DNA2RNA_with_listjoin(seq)

        runtimes["Method 1"].append(runtime1)
        runtimes["Method 2"].append(runtime2)
        runtimes["Method 3"].append(runtime3)
        runtimes["Method 4"].append(runtime4)

    return runtimes


# Plot the runtimes
def plot_runtimes(sequence_lengths, runtimes):
    plt.figure(figsize=(10, 6))

    for method, times in runtimes.items():
        plt.plot(sequence_lengths, times, label=method)

    plt.xlabel("Sequence Length")
    plt.ylabel("Runtime (seconds)")
    plt.title("Runtime of Different Methods for Transcribing DNA to RNA")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    sequence_lengths = [10, 100, 1000, 5000, 10000, 50000, 100000, 500000, 1000000,5000000]
    runtimes = measure_runtimes(sequence_lengths)
    plot_runtimes(sequence_lengths, runtimes)


if __name__ == "__main__":
    main()
