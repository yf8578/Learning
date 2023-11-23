rule featurecount_1:
    input:
        bam="results/{sample}/hisat2/{sample}_accepted_hits.sorted.bam",
    output:
        fea_txt="results/{sample}/featurecount1/{sample}.featurecount.txt",
    params:
        path=config["softwares"]["featurecounts"]["path"],
        handele="-T 12 -t gene  -g gene_id -B -C  -p   -O --minOverlap 10",
        human_gtf=config["softwares"]["featurecounts"]["human_gtf"],
    shell:
        "{params.path} {params.handele} -a {params.human_gtf} -o {output.fea_txt} {input.bam}"


rule featurecount_2:
    input:
        bam="results/{sample}/hisat2/{sample}_accepted_hits.sorted.bam",
    output:
        fea_txt="results/{sample}/featurecount2/{sample}.featurecount.txt",
    params:
        path=config["softwares"]["featurecounts"]["path"],
        handele="-T 12 -t gene  -g gene_id -B -C  -p",
        human_gtf=config["softwares"]["featurecounts"]["human_gtf"],
    shell:
        "{params.path} {params.handele} -a {params.human_gtf} -o {output.fea_txt} {input.bam}"


rule counts:
    input:
        fea_txt1="results/{sample}/featurecount1/{sample}.featurecount.txt",
        fea_txt2="results/{sample}/featurecount2/{sample}.featurecount.txt",
    output:
        feature_out_path1="results/{sample}/featurecount1/",
        feature_out_path2="results/{sample}/featurecount2/",
    params:
        script_py="/jdfssz1/ST_HEALTH/P20Z10200N0041/zhangyifan1/master/test-snakemake/gene_summary_20230315.py",
        conda_py="/hwfssz5/ST_HEALTH/P20Z10200N0041/zhangyifan1/miniconda3/bin/python",
    shell:
        "{params.conda_py} {params.script_py} {input.fea_txt1} {output.feature_out_path1} && "
        "{params.conda_py} {params.script_py} {input.fea_txt2} {output.feature_out_path2}"
