rule miRNA:
    # input:
    #     fq1="jdfssz1/ST_HEALTH/P20Z10200N0041/zhangyifan1/master/test-snakemake/results/{sample}/hisat2/{sample}_non_rRNA.1.fq.gz",
    output:
        fq2="/jdfssz1/ST_HEALTH/P20Z10200N0041/zhangyifan1/master/test-snakemake/results/{sample}/hisat2/{sample}_non_rRNA.1.fq",
        fa1="/jdfssz1/ST_HEALTH/P20Z10200N0041/zhangyifan1/master/test-snakemake/results/{sample}/miRNA/{sample}_all_collapsed_r1.fa",
        arf1="/jdfssz1/ST_HEALTH/P20Z10200N0041/zhangyifan1/master/test-snakemake/results/{sample}/miRNA/{sample}_all_collapsed_r1.arf",
        report1="/jdfssz1/ST_HEALTH/P20Z10200N0041/zhangyifan1/master/test-snakemake/results/{sample}/miRNA/{sample}_all_collapsed_r1_report.log",
        final_check="/jdfssz1/ST_HEALTH/P20Z10200N0041/zhangyifan1/master/test-snakemake/results/{sample}/miRNA/{sample}.final.txt",
    params:
        mapper="/jdfssz1/ST_HEALTH/P20Z10200N0041/Lishaogang/software/miniconda3/bin/mapper.pl",
        miRDeep2="/jdfssz1/ST_HEALTH/P20Z10200N0041/Lishaogang/software/miniconda3/bin/miRDeep2.pl",
        genome="/jdfssz1/ST_HEALTH/P20Z10200N0041/Wangyingying/ref/hg38/genome.fa",
        miRBase_mature="/jdfssz1/ST_HEALTH/P20Z10200N0041/Wangyingying/ref/miRBase/mature_hsa_ref.fa",
        miRBase_hairpin="/jdfssz1/ST_HEALTH/P20Z10200N0041/Wangyingying/ref/miRBase/hairpin_hsa_ref.fa",
        bowtie1="/jdfssz1/ST_HEALTH/P20Z10200N0041/Wangyingying/ref/hg38/bowtie1/hg38_ref.fa",
    shell:
        """

        cd /jdfssz1/ST_HEALTH/P20Z10200N0041/zhangyifan1/master/test-snakemake/results/{wildcards.sample}/miRNA && 



        /usr/bin/gunzip -c /jdfssz1/ST_HEALTH/P20Z10200N0041/zhangyifan1/master/test-snakemake/results/{wildcards.sample}/hisat2/{wildcards.sample}_non_rRNA.1.fq.gz > {output.fq2} && 



        source /jdfssz1/ST_HEALTH/P20Z10200N0041/Lishaogang/software/miniconda3/bin/activate && 



        {params.mapper} {wildcards.sample}_non_rRNA.1.fq -e -p {params.bowtie1} -s {output.fa1} -t {output.arf1} -h -m -v -o 10 && 



        {params.miRDeep2} {output.fa1} {params.genome} {output.arf1} {params.miRBase_mature} none {params.miRBase_hairpin} -t Human 2> {output.report1} && 



        cd /jdfssz1/ST_HEALTH/P20Z10200N0041/zhangyifan1/master/test-snakemake



        """
        "echo done! > {output.final_check}"
