# -*- coding: utf-8 -*-
import pandas as pd
import sys
import os

inputfeaturecounts_file = sys.argv[1]  # ��ȡ�����ļ���featurecounts������ļ�
output_path = sys.argv[2]  # �������������·��
temppath = sys.argv[3]  # �ϲ��ļ�����ļ���
try:
    ref_name_type = pd.read_csv(
        "/jdfssz1/ST_HEALTH/P20Z10200N0041/Wangyingying/cfRNA/cfRNA_code/zhangyifan/gene_type_tpm/new_genename2type.txt",
        sep="\t",
    )

    # ��inputfeaturecounts_file��/��\\�ָȡ���һ��Ԫ�أ����ļ���
    inputfeaturecounts_file_name = inputfeaturecounts_file.split("/")[-1].split("\\")[
        -1
    ]
    id = inputfeaturecounts_file_name.split(".")[0]

    temp_tpm = temppath + "/" + "temp_tpm"
    temp_counts = temppath + "/" + "temp_counts"
    # �ж��ļ����Ƿ���ڣ�����������򴴽�
    if not os.path.exists(temp_tpm):
        os.makedirs(temp_tpm)
    if not os.path.exists(temp_counts):
        os.makedirs(temp_counts)

    # ��ȡ�����ļ�,�ڶ���Ϊ������
    data = pd.read_csv(inputfeaturecounts_file, sep="\t", header=1)
    # data���һ��������ΪCounts
    data = data.rename(columns={data.columns[-1]: "Counts"})
    # ����TPM
    data["kb"] = data["Length"] / 1000
    data["rpkm"] = data["Counts"] / data["kb"]
    data["TPM"] = (data["rpkm"] / data["rpkm"].sum()) * 1e6
    # ����CPM
    data["CPM"] = (data["Counts"] / data["Counts"].sum()) * 1e6
    # ��ȡGene_ID��tpm�У����浽�µ����ݿ�TPM��
    TPM = data[["Geneid", "TPM"]]
    CPM = data[["Geneid", "CPM"]]
    COUNTS = data[["Geneid", "Counts"]]
    # ����ļ�
    TPM.to_csv(output_path + "/" + id + ".gene_TPM.txt", sep="\t", index=False)
    CPM.to_csv(output_path + "/" + id + ".gene_CPM.txt", sep="\t", index=False)
    COUNTS.to_csv(output_path + "/" + id + ".gene_COUNTS.txt", sep="\t", index=False)
    print(id + " gene TPM CPM COUNTS done!")
    # ����һ���յ�dataframe����ȡref��GeneType������Ϊ����
    df = pd.DataFrame(index=ref_name_type["GeneType"].unique())
    df["TPM>0"] = 0
    df["TPM>1"] = 0
    df["TPM>5"] = 0
    df["TPM>10"] = 0
    # ***********����TPM>0,TPM>1,TPM>5,TPM>10�ĸ���***********
    tpm = pd.read_csv(output_path + "/" + id + ".gene_TPM.txt", sep="\t")
    tpm.columns = ["GeneSymbol", "tpm"]
    tpm_name_type = pd.merge(tpm, ref_name_type, on="GeneSymbol", how="left")
    ##20230407
    tpm_name_type["GeneType"] = tpm_name_type["GeneType"].fillna("other")
    # tpm_name_type��GeneType����Ϊ����
    tpm_name_type = tpm_name_type.set_index("GeneType")
    # ��df������Ϊѭ��������ѭ������tpm_name_type��tpm��
    for type in df.index:
        # �ж�i��tpm_name_type�е�GeneType���Ƿ���ڣ����������ִ���������䣬
        if type in tpm_name_type.index:
            # ��ȡtpm_name_type��
            TPMnum = list(tpm_name_type.loc[type, "tpm"])
            for tpmnum in TPMnum:
                if tpmnum > 10:
                    df.loc[type, "TPM>0"] += 1
                    df.loc[type, "TPM>1"] += 1
                    df.loc[type, "TPM>5"] += 1
                    df.loc[type, "TPM>10"] += 1
                elif tpmnum > 5:
                    df.loc[type, "TPM>0"] += 1
                    df.loc[type, "TPM>1"] += 1
                    df.loc[type, "TPM>5"] += 1
                elif tpmnum > 1:
                    df.loc[type, "TPM>0"] += 1
                    df.loc[type, "TPM>1"] += 1
                elif tpmnum > 0:
                    df.loc[type, "TPM>0"] += 1
            pass
    # ����ļ�
    df.to_csv(output_path + "/" + id + ".TPM_count.txt", sep="\t")
    df.to_csv(temp_tpm + "/" + id + ".TPM_count.txt", sep="\t")
    print(id + ".TPM_count.txt done!")
    # ***********RNAtype counts***********
    counts = pd.read_csv(output_path + "/" + id + ".gene_COUNTS.txt", sep="\t")
    counts.columns = ["GeneSymbol", "counts"]
    counts_name_type = pd.merge(counts, ref_name_type, on="GeneSymbol", how="left")
    ##20230407
    counts_name_type["GeneType"] = counts_name_type["GeneType"].fillna("other")
    # ͳ��GeneType�ж�Ӧ��counts�еĺ�
    RNAtype_counts = counts_name_type.groupby("GeneType")["counts"].sum()
    RNAtype_counts.to_csv(output_path + "/" + id + ".RNA_type.txt")
    RNAtype_counts.to_csv(temp_counts + "/" + id + ".RNA_type.txt")
    print(id + ".RNA_type.txt done!")
except:
    print(id + " gene TPM CPM COUNTS failed!")
    print(id + ".TPM_count.txt failed!")
    print(id + ".RNA_type.txt failed!")
    pass
