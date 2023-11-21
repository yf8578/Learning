import pandas as pd

samples = (
    pd.read_csv(config["samples"], sep=",")
    .set_index("sample_name", drop=False)
    .sort_index()
)
SAMPLES = list(samples["sample_name"])


# fastq1 input function definition
def fq1_from_sample(wildcards):
    return samples.loc[wildcards.sample, "path1"]


# fastq2 input function definition
def fq2_from_sample(wildcards):
    return samples.loc[wildcards.sample, "path2"]
