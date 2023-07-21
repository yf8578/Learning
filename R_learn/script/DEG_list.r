# /*
#* @Author: zhangyifan1
#* @Date: 2023-07-12 10:03:18
#* @LastEditors: zhangyifan1 zhangyifan1@genomics.cn
#* @LastEditTime: 2023-07-12 16:45:21
#* @FilePath: \01hilld:\000zyf\work\R_learn\script\DEG_list.r
#* @Description:

# 差异分析
DEG <- function(CONTROL_counts, TREATMENT_counts, GROUP_NAME) {
    # 差异分析两组数据
    conditions <- factor(
        c(
            rep("Control", length(names(CONTROL_counts))),
            rep("Treat", length(names(TREATMENT_counts)))
        ),
        levels = c("Control", "Treat")
    )
    Data_frame <- cbind(CONTROL_counts, TREATMENT_counts)
    # 过滤表达量不超过10的基因
    Data_frame <- Data_frame[rowSums(Data_frame) >= 10, ]
    #########################################################################################################################################################
    colData <- data.frame(
        row.names = colnames(Data_frame),
        conditions = conditions
    )
    # 差异分析
    # library(DESeq2) # nolint
    suppressPackageStartupMessages(library(DESeq2)) # 防止输出DESeq2包的版本信息
    dds <- DESeqDataSetFromMatrix(countData = Data_frame, colData = colData, design = ~conditions)
    dds <- DESeq(dds)
    res <- results(dds)
    # 如果你想保存所有结果，也可以不过滤,
    write.table(res, paste(GROUP_NAME, "_all_diff_exp_gene.txt", sep = ""),
        sep = "\t", row.names = T, quote = F
    )
    # 过滤标准: padj < 0.05, log2 fold change >= 1
    # 筛选差异表达基因
    res1 <- data.frame(res, stringsAsFactors = FALSE, check.names = FALSE)
    # 去除NA值
    res1 <- na.omit(res1)
    ######################################################################################################################
    # 按 padj 值升序排序，相同 padj 值下继续按 log2FC 降序排序
    res1 <- res1[order(res1$padj, res1$log2FoldChange,
        decreasing = c(FALSE, TRUE)
    ), ]

    # log2FC≥1 & padj<0.05 标识 up，代表显著上调的基因
    # log2FC≤-1 & padj<0.05 标识 down，代表显著下调的基因
    # 其余标识 none，代表非差异的基因
    res1[which(res1$log2FoldChange >= 1 & res1$padj < 0.05), "sig"] <- "up"
    res1[which(res1$log2FoldChange <= -1 & res1$padj < 0.05), "sig"] <- "down"
    res1[which(abs(res1$log2FoldChange) <= 1 | res1$padj >= 0.05), "sig"] <- "none"

    # 输出上调下调基因
    res1_select <- subset(res1, res1$sig %in% c("up", "down"))
    write.table(res1_select,
        paste(GROUP_NAME, "_diff_exp_gene_up_and_down.txt", sep = ""),
        sep = "\t", row.names = T, quote = F
    )
    return(res1)
}
