"""
Author: zhangyifan1
Date: 2024-06-10 21:23:02
LastEditors: zhangyifan1 zhangyifan1@genomics.cn
LastEditTime: 2024-06-16 14:49:15
FilePath: //Rosalind//07_Mendel's First Law.py
Description: 

"""


def dominant_phenotype_probability(k, m, n):
    # 总个体数
    total = k + m + n
    # 各种配对产生显性表型的概率
    prob_AA_AA = (k / total) * ((k - 1) / (total - 1))
    prob_AA_Aa = 2 * (k / total) * (m / (total - 1))
    prob_AA_aa = 2 * (k / total) * (n / (total - 1))
    prob_Aa_Aa = (m / total) * ((m - 1) / (total - 1))
    prob_Aa_aa = 2 * (m / total) * (n / (total - 1))
    prob_aa_aa = (n / total) * ((n - 1) / (total - 1))

    # 显性表型的总概率
    probability = (
        prob_AA_AA * 1
        + prob_AA_Aa * 1
        + prob_AA_aa * 1
        + prob_Aa_Aa * 0.75
        + prob_Aa_aa * 0.5
        + prob_aa_aa * 0
    )
    return probability


def main():
    # 从输入读取数据
    k = int(input("请输入显性纯合体（AA）的个体数: "))
    m = int(input("请输入杂合体（Aa）的个体数: "))
    n = int(input("请输入隐性纯合体（aa）的个体数: "))

    # 计算并打印概率
    result = dominant_phenotype_probability(k, m, n)
    print(f"产生显性表型后代的概率: {result:.5f}")


if __name__ == "__main__":
    main()
