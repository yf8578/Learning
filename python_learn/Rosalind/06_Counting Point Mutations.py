
def mutation(seq1,seq2):
    mutation=0
    for base1,base2 in zip(seq1,seq2):
        if base1!=base2:
            mutation+=1
    return mutation

def main():
    seq1='GTGCCTATCGGTCAACCCAGGGGGTATACTCACTATCGTTTTTAGGGCGAACCCCCTATTACGTAAACTTCGACGGTCGAGCTACTACTACTT'
    seq2='GTGCCTATCGGTCAACCCAGGGGGTATACTCACTATCGAATTTAGGGCGAACCCCCTATTACGTAAACTTCGACGGTCGAGCTACTACTACTT'
    print(mutation(seq1,seq2))
    
    
    
if __name__=='__main__':
    main()
        