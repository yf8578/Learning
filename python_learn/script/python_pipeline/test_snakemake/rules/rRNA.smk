rule rRNA_depletion:
    input:
        fq1="results/{sample}/fastp/{sample}.r1.fq.gz",
        fq2="results/{sample}/fastp/{sample}.r2.fq.gz",
    output:
        sam=temp("results/{sample}/hisat2/{sample}_accepted_rRNA_hits.sam"),
        no_rRNA_1="results/{sample}/hisat2/{sample}_non_rRNA.1",
        no_rRNA_2="results/{sample}/hisat2/{sample}_non_rRNA.2",
        summary="results/{sample}/hisat2/{sample}.summary.txt",
    params:
        path=config["softwares"]["hisat2"]["path"],
        rRNAdatabase=config["softwares"]["hisat2"]["rRNAdatabase"],
        handle="--fr --dta --avoid-pseudogene -k 10 -p 12 --no-unal",
    shell:
        "{params.path} -x {params.rRNAdatabase} -1 {input.fq1} -2 {input.fq2} "
        "-S {output.sam} --summary-file {output.summary} "
        "--un-conc-gz results/{wildcards.sample}/hisat2/{wildcards.sample}_non_rRNA {params.handle}"


rule change_name:
    input:
        fq1="results/{sample}/hisat2/{sample}_non_rRNA.1",
        fq2="results/{sample}/hisat2/{sample}_non_rRNA.2",
    output:
        fastq1="results/{sample}/hisat2/{sample}_non_rRNA.1.fq.gz",
        fastq2="results/{sample}/hisat2/{sample}_non_rRNA.2.fq.gz",
    shell:
        "mv {input.fq1} {output.fastq1} && "
        "mv {input.fq2} {output.fastq2}"


rule alignment:
    input:
        fq1="results/{sample}/hisat2/{sample}_non_rRNA.1.fq.gz",
        fq2="results/{sample}/hisat2/{sample}_non_rRNA.2.fq.gz",
    output:
        sam="results/{sample}/hisat2/{sample}_accepted_hits.sam",
        summary="results/{sample}/hisat2/{sample}_hisat2_result.txt",
        fastq1="results/{sample}/hisat2/{sample}_unmapped.1",
        fastq2="results/{sample}/hisat2/{sample}_unmapped.2",
    params:
        path=config["softwares"]["hisat2"]["path"],
        genome=config["softwares"]["hisat2"]["human_genome"],
        handle="-k 10 -p 12 --no-unal --fr --dta --avoid-pseudogene",
    shell:
        "{params.path} -x {params.genome} -1 {input.fq1} -2 {input.fq2} "
        "-S {output.sam} --summary-file {output.summary} "
        "--un-conc-gz results/{wildcards.sample}/hisat2/{wildcards.sample}_unmapped {params.handle} --novel-splicesite-outfile results/{wildcards.sample}/hisat2/{wildcards.sample}_junctions.bed"


rule samtools:
    input:
        sam="results/{sample}/hisat2/{sample}_accepted_hits.sam",
    output:
        sorted_bam="results/{sample}/hisat2/{sample}_accepted_hits.sorted.bam",
    params:
        path=config["softwares"]["samtools"]["path"],
    shell:
        "{params.path} view -@ 4 -Su {input.sam} | {params.path} sort -@ 4 -o results/{wildcards.sample}/hisat2/{wildcards.sample}_accepted_hits.sorted.sam -O SAM && {params.path} view -@ 4 -bS results/{wildcards.sample}/hisat2/{wildcards.sample}_accepted_hits.sorted.sam > {output.sorted_bam} && {params.path} index {output.sorted_bam} && rm results/{wildcards.sample}/hisat2/{wildcards.sample}_accepted_hits.sam results/{wildcards.sample}/hisat2/{wildcards.sample}_accepted_hits.sorted.sam"
