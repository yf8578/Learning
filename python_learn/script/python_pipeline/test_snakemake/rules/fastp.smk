rule fastp_Cutadapter:
    input:
        fq1=fq1_from_sample,
        fq2=fq2_from_sample,
    output:
        fastq1=temp("results/{sample}/fastp/{sample}.N1.r1.fq"),
        fastq2=temp("results/{sample}/fastp/{sample}.N1.r2.fq"),
        html="results/{sample}/fastp/{sample}.html",
        json="results/{sample}/fastp/{sample}.json",
        failed_out="results/{sample}/fastp/{sample}_cutadapter.failed_out.fq.gz",
    params:
        fastp_path=config["softwares"]["fastp"]["path"],
        handle="""--adapter_sequence=AAGTCGGA \\
                                                             --adapter_sequence_r2=AAGTCGGA \\
                                                             --disable_trim_poly_g \\
                                                             --disable_quality_filtering  \\
                                                             --disable_length_filtering \\
                                                             --dont_eval_duplication \\
                                                             --thread=12  -c \\""",
    shell:
        "{params.fastp_path} -i {input.fq1} -I {input.fq2} "
        "-o {output.fastq1} -O {output.fastq2} -h {output.html} -j {output.json} --failed_out {output.failed_out} {params.handle}"


rule seqtk_reverse:
    input:
        seq1="results/{sample}/fastp/{sample}.N1.r1.fq",
    output:
        seq1_reverse=temp("results/{sample}/fastp/{sample}.N1.r1_rp.fq"),
    params:
        seqtk_path=config["softwares"]["seqtk"]["path"],
    shell:
        "{params.seqtk_path} seq -r {input.seq1} > {output.seq1_reverse}"


rule fastp_CutpolyA:
    input:
        fq1="results/{sample}/fastp/{sample}.N1.r1_rp.fq",
        fq2="results/{sample}/fastp/{sample}.N1.r2.fq",
    output:
        fastq1=temp("results/{sample}/fastp/{sample}.N2.r1_rp.fq"),
        fastq2=temp("results/{sample}/fastp/{sample}.N2.r2.fq"),
        json="results/{sample}/fastp/{sample}.cutPolyA.json",
        html="results/{sample}/fastp/{sample}.cutPolyA.html",
        failed_out="results/{sample}/fastp/{sample}_cutpolyA.failed_out.fq.gz",
    params:
        fastp_path=config["softwares"]["fastp"]["path"],
        handle="""--adapter_fasta /jdfssz1/ST_HEALTH/P20Z10200N0041/Lishaogang/Rscript/cfRNA_pip/adapter_fasta/polyA_10A.fa \\
                                                         --thread=12 \\
                                                         --disable_trim_poly_g \\
                                                         --disable_quality_filtering  \\
                                                         --disable_length_filtering \\
                                                         --dont_eval_duplication \\""",
    shell:
        "{params.fastp_path} -i {input.fq1} -I {input.fq2} "
        "-o {output.fastq1} -O {output.fastq2} -h {output.html} -j {output.json} --failed_out {output.failed_out} {params.handle}"


rule seqtk_reverse2:
    input:
        seq1="results/{sample}/fastp/{sample}.N2.r1_rp.fq",
    output:
        seq1_reverse=temp("results/{sample}/fastp/{sample}.N2.r1.fq"),
    params:
        seqtk_path=config["softwares"]["seqtk"]["path"],
    shell:
        "{params.seqtk_path} seq -r {input.seq1} > {output.seq1_reverse}"


rule fastp_QC:
    input:
        fq1="results/{sample}/fastp/{sample}.N2.r1.fq",
        fq2="results/{sample}/fastp/{sample}.N2.r2.fq",
    output:
        fastq1=temp("results/{sample}/fastp/{sample}.N3.r1.fq"),
        fastq2=temp("results/{sample}/fastp/{sample}.N3.r2.fq"),
        json="results/{sample}/fastp/{sample}.quality_filter_.fastp.json",
        html="results/{sample}/fastp/{sample}.quality_filter.fastp.html",
        failed_out="results/{sample}/fastp/{sample}_quality_failed_out.fq.gz",
    params:
        fastp_path=config["softwares"]["fastp"]["path"],
        handle="""--disable_adapter_trimming \\
                                                        --thread=12 \\
                                                        --disable_trim_poly_g \\
                                                        --qualified_quality_phred=30 \\
                                                        --unqualified_percent_limit=50 \\
                                                        --disable_length_filtering \\
                                                        --n_base_limit=10 \\
                                                        -p  -c \\""",
    shell:
        "{params.fastp_path} -i {input.fq1} -I {input.fq2} "
        "-o {output.fastq1} -O {output.fastq2} -h {output.html} -j {output.json} --failed_out {output.failed_out} {params.handle}"


rule fastp_LC:
    input:
        fq1="results/{sample}/fastp/{sample}.N3.r1.fq",
        fq2="results/{sample}/fastp/{sample}.N3.r2.fq",
    output:
        fastq1="results/{sample}/fastp/{sample}.r1.fq.gz",
        fastq2="results/{sample}/fastp/{sample}.r2.fq.gz",
        json="results/{sample}/fastp/{sample}.lengthfilter.fastp.json",
        html="results/{sample}/fastp/{sample}.lengthfilter.fastp.html",
        failed_out="results/{sample}/fastp/{sample}_length_failed_out.fq.gz",
    params:
        fastp_path=config["softwares"]["fastp"]["path"],
        handle="""--disable_adapter_trimming \\
                           --thread=12 \\
                           --disable_trim_poly_g \\
                           --length_required=17 \\
                           --disable_quality_filtering  \\
                           --dont_eval_duplication \\
                           -p  -c \\""",
    shell:
        "{params.fastp_path} -i {input.fq1} -I {input.fq2} "
        "-o {output.fastq1} -O {output.fastq2} -h {output.html} -j {output.json} --failed_out {output.failed_out} {params.handle}"
