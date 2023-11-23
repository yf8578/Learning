rule change_name_2:
    input:
        "results/{sample}/hisat2/{sample}_unmapped.1",
        "results/{sample}/hisat2/{sample}_unmapped.2",
    output:
        "results/{sample}/hisat2/{sample}_unmapped.1.fq.gz",
        "results/{sample}/hisat2/{sample}_unmapped.2.fq.gz",
    shell:
        "mv {input[0]} {output[0]} && mv {input[1]} {output[1]}"


# rule kraken2:
rule kraken2:
    input:
        fq1="results/{sample}/hisat2/{sample}_unmapped.1.fq.gz",
        fq2="results/{sample}/hisat2/{sample}_unmapped.2.fq.gz",
    output:
        unclassified_out_1="results/{sample}/kraken2/unclassified.{sample}._1fq",
        unclassified_out_2="results/{sample}/kraken2/unclassified.{sample}._2fq",
        report="results/{sample}/kraken2/{sample}.report",
        classified_out_1="results/{sample}/kraken2/classified.{sample}._1fq",
        classified_out_2="results/{sample}/kraken2/classified.{sample}._2fq",
        output="results/{sample}/kraken2/{sample}.output",
        final_check="results/{sample}/kraken2/{sample}.final.txt",
    params:
        path=config["softwares"]["kraken2"]["path"],
        database=config["softwares"]["kraken2"]["database"],
        handle="--threads 6 --use-names --use-mpa-style  --paired",
    shell:
        "{params.path} {params.handle} --db {params.database} --unclassified-out results/{wildcards.sample}/kraken2/unclassified.{wildcards.sample}.#fq --report {output.report} --classified-out results/{wildcards.sample}/kraken2/classified.{wildcards.sample}.#fq --output {output.output} {input.fq1} {input.fq2} && "
        "echo done! > {output.final_check}"
