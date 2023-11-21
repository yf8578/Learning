sample=$1
DataPATH=$2
dir=${DataPATH}/01_quantitative_analyses
cat $sample | while read line
do
id=`echo $line |awk '{print $1}'`
fq1=`echo $line |awk '{print $2}'`
fq2=`echo $line |awk '{print $3}'`


if [ ! -d "$dir/result" ];then
  mkdir $dir/result
fi

if [ ! -d "$dir/result/$id" ];then
  mkdir $dir/result/$id
fi


if [ ! -d "$dir/shell" ];then
  mkdir $dir/shell
fi

if [ ! -d "$dir/featurecount1" ];then
  mkdir $dir/featurecount1
fi

if [ ! -d "$dir/featurecount2" ];then
  mkdir $dir/featurecount2
fi




#####qc

outdir_step1_fastp=$dir/result/$id/step1_fastp

if [ ! -d "$outdir_step1_fastp" ];then
  mkdir $outdir_step1_fastp
fi


outdir_step2_rRNA=$dir/result/$id/step2_rRNA

if [ ! -d "$outdir_step2_rRNA" ];then
  mkdir $outdir_step2_rRNA
fi

outdir_step3_miRNA=$dir/result/$id/step3_miRNA

if [ ! -d "$outdir_step3_miRNA" ];then
  mkdir $outdir_step3_miRNA
fi

outdir_step3_hisat2=$dir/result/$id/step3_hisat2

if [ ! -d "$outdir_step3_hisat2" ];then
  mkdir $outdir_step3_hisat2
fi

outdir_step4_featureCounts_1=$dir/result/$id/step4_featureCounts_1

if [ ! -d "$outdir_step4_featureCounts_1" ];then
  mkdir $outdir_step4_featureCounts_1
fi

outdir_step4_featureCounts_2=$dir/result/$id/step4_featureCounts_2

if [ ! -d "$outdir_step4_featureCounts_2" ];then
  mkdir $outdir_step4_featureCounts_2
fi




outdir_step5_result_summary=$dir/result/$id/step5_result_summary

if [ ! -d "$
outdir_step5_result_summary" ];then
  mkdir $outdir_step5_result_summary
fi

outdir_step5_qualimap=$dir/result/$id/step5_result_summary/step_result_qualimap

if [ ! -d "$outdir_step5_qualimap" ];then
  mkdir $outdir_step5_qualimap
fi

outdir_step5_kraken2=$dir/result/$id/step_kraken2

if [ ! -d "$outdir_step5_kraken2" ];then
  mkdir $outdir_step5_kraken2
fi


echo "

date1=\`date\`

###step1.1:base correction for PE data   ,   Cut adapter
/jdfssz1/ST_HEALTH/P20Z10200N0041/Lishaogang/software/miniconda3/bin/fastp \\
-i $fq1 -I $fq2  \\
-o $outdir_step1_fastp/N1.r1.fq -O $outdir_step1_fastp/N1.r2.fq  \\
-h $outdir_step1_fastp/cutadapter_fastp.html -j $outdir_step1_fastp/cutadapter_fastp.json \\
--adapter_sequence=AAGTCGGA \\
--adapter_sequence_r2=AAGTCGGA \\
--disable_trim_poly_g \\
--disable_quality_filtering  \\
--disable_length_filtering \\
--dont_eval_duplication \\
--thread=12  -c \\
--failed_out $outdir_step1_fastp/${id}_cutadapter.failed_out.fq.gz &&


###Reverse complement of Read1.fq
/jdfssz1/ST_HEALTH/P20Z10200N0041/Lishaogang/software/seqtk/seqtk seq -r $outdir_step1_fastp/N1.r1.fq > $outdir_step1_fastp/N1.r1_rp.fq
rm $outdir_step1_fastp/N1.r1.fq

#####step1.2:Cut polyA 



/jdfssz1/ST_HEALTH/P20Z10200N0041/Lishaogang/software/miniconda3/bin/fastp \\
-i $outdir_step1_fastp/N1.r1_rp.fq  -I $outdir_step1_fastp/N1.r2.fq \\
-o $outdir_step1_fastp/N2.r1_rp.fq -O $outdir_step1_fastp/N2.r2.fq \\
-h $outdir_step1_fastp/cutpolyA_fastp.html -j $outdir_step1_fastp/cutployA_fastp.json \\
--adapter_fasta /jdfssz1/ST_HEALTH/P20Z10200N0041/Lishaogang/Rscript/cfRNA_pip/adapter_fasta/polyA_10A.fa \\
--thread=12 \\
--disable_trim_poly_g \\
--disable_quality_filtering  \\
--disable_length_filtering \\
--dont_eval_duplication \\
--failed_out $outdir_step1_fastp/${id}_cutpolyA_rp.failed_out.fq.gz

rm $outdir_step1_fastp/N1.r1_rp.fq
rm $outdir_step1_fastp/N1.r2.fq

###Reverse complement of Read1.fq again
/jdfssz1/ST_HEALTH/P20Z10200N0041/Lishaogang/software/seqtk/seqtk seq -r $outdir_step1_fastp/N2.r1_rp.fq > $outdir_step1_fastp/N2.r1.fq

rm $outdir_step1_fastp/N2.r1_rp.fq



###step1.3  quality control 

/jdfssz1/ST_HEALTH/P20Z10200N0041/Lishaogang/software/miniconda3/bin/fastp \\
-i $outdir_step1_fastp/N2.r1.fq -I $outdir_step1_fastp/N2.r2.fq  \\
-o $outdir_step1_fastp/N3.r1.fq -O $outdir_step1_fastp/N3.r2.fq  \\
-h $outdir_step1_fastp/quality_filter.fastp.html -j $outdir_step1_fastp/quality_filter_.fastp.json \\
--disable_adapter_trimming \\
--thread=12 \\
--disable_trim_poly_g \\
--qualified_quality_phred=30 \\
--unqualified_percent_limit=50 \\
--disable_length_filtering \\
--n_base_limit=10 \\
-p  -c \\
--failed_out $outdir_step1_fastp/${id}_quality_failed_out.fq.gz &&

###step1.4  length control

rm $outdir_step1_fastp/N2.r1.fq
rm $outdir_step1_fastp/N2.r2.fq

/jdfssz1/ST_HEALTH/P20Z10200N0041/Lishaogang/software/miniconda3/bin/fastp \\
-i $outdir_step1_fastp/N3.r1.fq -I $outdir_step1_fastp/N3.r2.fq  \\
-o $outdir_step1_fastp/${id}.r1.fq.gz -O $outdir_step1_fastp/${id}.r2.fq.gz  \\
-h $outdir_step1_fastp/${id}_lengthfilter.fastp.html -j $outdir_step1_fastp/${id}_lengthfilter.fastp.json \\
--disable_adapter_trimming \\
--thread=12 \\
--disable_trim_poly_g \\
--length_required=17 \\
--disable_quality_filtering  \\
--dont_eval_duplication \\
-p  -c \\
--failed_out $outdir_step1_fastp/${id}_length_failed_out.fq.gz &&


rm $outdir_step1_fastp/N3.r1.fq
rm $outdir_step1_fastp/N3.r2.fq

date2=\`date\`


###step2 hisat2： rRNA depletion
/share/app/hisat/2.2.1/hisat2 -k 10 -p 12 --no-unal \\
-x /jdfssz1/ST_HEALTH/P20Z10200N0041/Lishaogang/Rscript/cfRNA_pip/rRNA_rmdup/rRNA-new/genome_ss_exon -S $outdir_step2_rRNA/${id}_accepted_hits.sam \\
--fr --dta --avoid-pseudogene \\
--un-conc-gz $outdir_step2_rRNA/${id}_non_rRNA --summary-file $outdir_step2_rRNA/${id}_rRNA_result.txt \\
-1  $outdir_step1_fastp/$id.r1.fq.gz -2 $outdir_step1_fastp/$id.r2.fq.gz &&

rm $outdir_step2_rRNA/${id}_accepted_hits.sam &&
mv $outdir_step2_rRNA/${id}_non_rRNA.1 $outdir_step2_rRNA/${id}_non_rRNA.1.fq.gz &&
mv $outdir_step2_rRNA/${id}_non_rRNA.2 $outdir_step2_rRNA/${id}_non_rRNA.2.fq.gz &&

date3=\`date\`
###step3hisat2  Alignment to genome
/share/app/hisat/2.2.1/hisat2 -k 10 -p 12 --no-unal \\
-x /jdfssz1/ST_HEALTH/P20Z10200N0041/Lishaogang/Rscript/cfRNA_pip/genome/genome_ss_exon/genome_ss_exon  -S $outdir_step3_hisat2/${id}_accepted_hits.sam \\
--novel-splicesite-outfile $outdir_step3_hisat2/${id}_junctions.bed  \\
--fr --dta --avoid-pseudogene \\
--un-conc-gz $outdir_step3_hisat2/${id}_unmapped --summary-file $outdir_step3_hisat2/${id}_hisat2_result.txt \\
-1  $outdir_step2_rRNA/${id}_non_rRNA.1.fq.gz -2 $outdir_step2_rRNA/${id}_non_rRNA.2.fq.gz &&
/share/app/samtools/1.11/bin/samtools view -@ 4 -Su $outdir_step3_hisat2/${id}_accepted_hits.sam | /share/app/samtools/1.11/bin/samtools sort -@ 4 -o $outdir_step3_hisat2/${id}_accepted_hits.sorted.sam -O SAM &&/share/app/samtools/1.11/bin/samtools view -@ 4 -bS $outdir_step3_hisat2/${id}_accepted_hits.sorted.sam > $outdir_step3_hisat2/${id}_accepted_hits.sorted.bam && /share/app/samtools/1.11/bin/samtools index $outdir_step3_hisat2/${id}_accepted_hits.sorted.bam && 

rm $outdir_step3_hisat2/${id}_accepted_hits.sam $outdir_step3_hisat2/${id}_accepted_hits.sorted.sam 

date4=\`date\`


###step4_featureCounts  :Assemble reads into genes


##featureCounts  -O --minOverlap 10
/hwfssz5/ST_HEALTH/P20Z10200N0041/leichanggui/projects/software/subread-2.0.2-Linux-x86_64/bin/featureCounts \
-T 12 -t gene  -g gene_id -B -C  -p   -O --minOverlap 10 \
-a  /jdfssz1/ST_HEALTH/P20Z10200N0041/Wangyingying/cfRNA/cfRNA_reference/NCBI-GTF/GCF_000001405.40_GRCh38.p14_genomic.gtf \
-o ${outdir_step4_featureCounts_1}/$id.featurecounts.txt ${dir}/result/$id/step3_hisat2/${id}_accepted_hits.sorted.bam &&

/hwfssz5/ST_HEALTH/P20Z10200N0041/zhangyifan1/miniconda3/bin/python /jdfssz1/ST_HEALTH/P20Z10200N0041/Wangyingying/cfRNA/cfRNA_code/zhangyifan/gene_type_tpm/gene_summary_20230315.py ${outdir_step4_featureCounts_1}/$id.featurecounts.txt ${outdir_step4_featureCounts_1} ${dir}/featurecount1 &&

##featureCounts 
/hwfssz5/ST_HEALTH/P20Z10200N0041/leichanggui/projects/software/subread-2.0.2-Linux-x86_64/bin/featureCounts \
-T 12 -t gene  -g gene_id -B -C  -p   \
-a /jdfssz1/ST_HEALTH/P20Z10200N0041/Wangyingying/cfRNA/cfRNA_reference/NCBI-GTF/GCF_000001405.40_GRCh38.p14_genomic.gtf \
-o ${outdir_step4_featureCounts_2}/$id.featurecounts.txt ${dir}/result/$id/step3_hisat2/${id}_accepted_hits.sorted.bam &&

/hwfssz5/ST_HEALTH/P20Z10200N0041/zhangyifan1/miniconda3/bin/python /jdfssz1/ST_HEALTH/P20Z10200N0041/Wangyingying/cfRNA/cfRNA_code/zhangyifan/gene_type_tpm/gene_summary_20230315.py ${outdir_step4_featureCounts_2}/$id.featurecounts.txt ${outdir_step4_featureCounts_2} ${dir}/featurecount2 &&

date5=\`date\`

###step5_qualimap

/hwfssz5/ST_HEALTH/P20Z10200N0041/leichanggui/projects/software/miniconda2/envs/aa/bin/qualimap rnaseq \\
-a uniquely-mapped-reads \\
--java-mem-size=10G \\
-bam  $outdir_step3_hisat2/${id}_accepted_hits.sorted.bam  \\
-gtf /jdfssz1/ST_HEALTH/P20Z10200N0041/Wangyingying/cfRNA/cfRNA_reference/NCBI-GTF/NCBI_genecard_final.gtf \\
-outdir $outdir_step5_qualimap/$id

date6=\`date\`

####step6_kraken2
mv $outdir_step3_hisat2/${id}_unmapped.1 $outdir_step3_hisat2/${id}_unmapped.1.fq.gz 
mv $outdir_step3_hisat2/${id}_unmapped.2 $outdir_step3_hisat2/${id}_unmapped.2.fq.gz 

kraken2=/hwfssz5/ST_HEALTH/P20Z10200N0041/leichanggui/projects/software/kraken2/kraken2
database_dir=/hwfssz5/ST_HEALTH/P20Z10200N0041/leichanggui/cfRNA/all_test/kraken2/db/minikraken_8GB_20200312

\$kraken2 --threads 6 --db \$database_dir \\
--use-names --use-mpa-style  --paired \\
--unclassified-out $outdir_step5_kraken2/unclassified.$id#.fastq \\
--report $outdir_step5_kraken2/$id.report \\
--classified-out $outdir_step5_kraken2/classified.$id.#fq \\
--output $outdir_step5_kraken2/$id.output \\
$outdir_step3_hisat2/${id}_unmapped.1.fq.gz \\
$outdir_step3_hisat2/${id}_unmapped.2.fq.gz



date7=\`date\`
 
if [  -e  $outdir_step5_kraken2/$id.report  ] && [  -s $outdir_step5_kraken2/$id.report  ]
then
echo  All steps have done！you can move your files！ >  $dir/result/$id/Endfile.txt
echo -e "\"${id}\\tSucceed\\t\`date\`\""  >> ${DataPATH}/Endreport.txt
else
echo -e "\"${id}\\tfiled\\t\`date\`\""  >> ${DataPATH}/Endreport.txt
fi 

cd $outdir_step3_miRNA
####step7 miRNA
/usr/bin/gunzip  $outdir_step2_rRNA/${id}_non_rRNA.1.fq.gz
source /jdfssz1/ST_HEALTH/P20Z10200N0041/Lishaogang/software/miniconda3/bin/activate

/jdfssz1/ST_HEALTH/P20Z10200N0041/Lishaogang/software/miniconda3/bin/mapper.pl $outdir_step2_rRNA/${id}_non_rRNA.1.fq -e  -p /jdfssz1/ST_HEALTH/P20Z10200N0041/Wangyingying/ref/hg38/bowtie1/hg38_ref.fa -s $outdir_step3_miRNA/${id}_all_collapsed_r1.fa -t $outdir_step3_miRNA/${id}_all_collapsed_r1.arf -h  -m -v -o 10

/jdfssz1/ST_HEALTH/P20Z10200N0041/Lishaogang/software/miniconda3/bin/miRDeep2.pl $outdir_step3_miRNA/${id}_all_collapsed_r1.fa /jdfssz1/ST_HEALTH/P20Z10200N0041/Wangyingying/ref/hg38/genome.fa $outdir_step3_miRNA/${id}_all_collapsed_r1.arf /jdfssz1/ST_HEALTH/P20Z10200N0041/Wangyingying/ref/miRBase/mature_hsa_ref.fa none /jdfssz1/ST_HEALTH/P20Z10200N0041/Wangyingying/ref/miRBase/hairpin_hsa_ref.fa -t Human 2>$outdir_step3_miRNA/${id}_all_collapsed_r1.arf_all_collapsed_r1_report.log

date8=\`date\`

echo reads_clean start at \$date1
echo Remove rRNA start at \$date2
echo Hisat2 aligement start at \$date3
echo featureCounts start at \$date4
echo qualimap start at \$date5
echo kraken2 statrt at \$date6
echo mirDeep start at \$date7
echo mirDeep end at \$date8
" > $dir/shell/$id.step_all.sh
done

