rule qualimap:
    input:
        bam="results/{sample}/hisat2/{sample}_accepted_hits.sorted.bam",
        gtf=config["softwares"]["featurecounts"]["human_gtf"],
    output:
        outputdir=directory("results/{sample}/qualimap/"),
        final_check="results/{sample}/qualimap/{sample}.final.txt",
    params:
        path=config["softwares"]["qualimap"]["path"],
        handle="--java-mem-size=10G -a uniquely-mapped-reads",
    shell:
        "{params.path} rnaseq {params.handle} -bam {input.bam} -gtf {input.gtf} -outdir {output.outputdir} && "
        "echo done! > {output.final_check}"
