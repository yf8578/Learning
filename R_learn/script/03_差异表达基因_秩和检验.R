#BiocManager::install("clusterProfiler") 

library(ggplot2)


deg_cal<-function(tit,detail_output,threshold){
  #data_matrix=read.csv("D:/work/PE/02_protein/02_QC/01_protein/3_proteomics_colmedian_union_final_Normalized/combined_matrix_final_imputed.csv",
   #                  header = T,row.names = 1)
  data_matrix=na.omit(read.csv(tit,header = T,row.names = 1))

  # 列名中以P开头的为一组，以C开头的为另一组
p_columns <- grep("^P", colnames(data_matrix))
c_columns <- grep("^C", colnames(data_matrix))

# 初始化结果矩阵
results <- data.frame(feature=rownames(data_matrix), p_value=NA, fold_change=NA)

# 对每一行（特征）进行Wilcoxon秩和检验
for (i in 1:nrow(data_matrix)) {
  p_group <- as.numeric(data_matrix[i, p_columns])
  c_group <- as.numeric(data_matrix[i, c_columns])
  
  # 计算fold change (mean ratio)
  fold_change <- mean(p_group, na.rm = TRUE) /mean(c_group, na.rm = TRUE)
  
  # 进行Wilcoxon秩和检验
  test_result <- wilcox.test(p_group, c_group)
  
  # 填充结果
  results[i, "p_value"] <- test_result$p.value
  results[i, "fold_change"] <- fold_change
}

# 应用FDR校正
results$fdr <- p.adjust(results$p_value, method = "fdr")
write.csv(results,paste(detail_output,"/all_deg_results.csv",sep = ""),row.names = F)
# 差异表达基因的筛选
de_genes <- results[(results$p_value <= 0.05),1]
de_exp<-na.omit(results[(results$p_value <= 0.05),])

write.csv(de_exp,paste(detail_output,"/dep_results_under_","05",".csv",sep = ""),row.names = F)
# 使用org.Hs.eg.db包中的函数将UniProt ID转换为Entrez ID
return(results)

}
deg_results=results
logFC_t=1
pvalue_t=0.05
fdr_threshold=0.05

dra_vol<-function(deg_results,logFC_t,pvalue_t,fdr_threshold)
{
# 火山图
# 计算-log10(p-value)和log2(fold_change)
deg_results$log2_fold_change <- log2(deg_results$fold_change)
deg_results$neg_log10_p_value <- -log10(deg_results$p_value)

#logFC_t=1
#pvalue_t=0.05
k1=(deg_results$p_value < pvalue_t)&(deg_results$fold_change < -logFC_t);
#table(k1)
k2=(deg_results$p_value < pvalue_t)&(deg_results$fold_change > logFC_t);
#table(k2)
deg_results$change=ifelse(k1,"DOWN",ifelse(k2,"UP","NOT"))
#table(deg_results$change)

# 绘制火山图
vol_plot<-ggplot(deg_results, aes(x = fold_change, y = neg_log10_p_value),color=change) +
  geom_point(aes(color = p_value < 0.05)) +
  scale_color_manual(values = c("black", "red")) +
  theme_minimal() +
  labs(x = "Log Fold Change", y = "-Log10 P-value", title = "Volcano Plot") +
  geom_vline(xintercept = 0, linetype = "dashed") +
  geom_hline(yintercept = -log10(0.05), linetype = "dashed")

ggsave(paste("Volcano_Plot_DEG_",fdr_threshold,".pdf"), plot = vol_plot, width = 10, height = 6)
ggsave(paste("Volcano_Plot_DEG_",fdr_threshold,".tiff"), plot = vol_plot, width = 10, height = 6, dpi = 300)

}

input_folder=c("D:/work/PE/05_RNA/clean_data/all//")
output_folder=c("D:/work/PE/05_RNA/01_DE/")
file_list=list.files(input_folder,full.names = T)
for (i in 1:length(file_list))
{
  tit=file_list[i]
  setwd(output_folder);
  deg_results=deg_cal(tit,output_folder,0.05);
  dra_vol(deg_results,1,0.05,0.05);
}
detail_output=output_folder

