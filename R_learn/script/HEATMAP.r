#-*-coding:utf-8-*-
# /*
#* @Author: zhangyifan1
#* @Date: 2023-07-12 10:00:10
#* @LastEditors: zhangyifan1 zhangyifan1@genomics.cn
#* @LastEditTime: 2023-07-12 16:44:25
#* @FilePath: \01hilld:\000zyf\work\R_learn\script\HEATMAP.r
#* @Description:
#* /
# usage HEATMAP(CONTROL_tpm, TREATMENT_tpm, GROUP_NAME,diff_expression_gene_slect)
# 热图
HEATMAP <- function(CONTROL_tpm, TREATMENT_tpm, GROUP_NAME, diff_expression_gene_slect) {
    library(ggplot2)
    library(pheatmap)
    # 列注释信息
    heatmap_data <- cbind(CONTROL_tpm, TREATMENT_tpm)
    diff_exp_gene <- rownames(diff_expression_gene_slect)
    heatmap_data <- heatmap_data[rownames(heatmap_data) %in% diff_exp_gene, ]
    heat_map_annotation_col <- data.frame(
        type = c(
            rep("Control", length(names(CONTROL_tpm))),
            rep("Treat", length(names(TREATMENT_tpm)))
        )
    )
    row.names(heat_map_annotation_col) <- colnames(heatmap_data)
    p <- pheatmap(heatmap_data,
        cluster_rows = T, cluster_cols = T, scale = "row",
        show_rownames = F, show_colnames = T,
        color = colorRampPalette(c("#057ce3", "white", "#db2c05"))(100),
        fontsize = 8, border_color = NA,
        main = GROUP_NAME, width = 8, height = 8,
        annotation_col = heat_map_annotation_col,
        annotation_names_col = F,
        cluster_method = "ward.D2", gaps_col = c(10, 20), gaps_row = c(10, 20), legend_labels = NA
    )
    # 保存图片
    ggsave(p, file = paste(GROUP_NAME, "_heatmap.png", sep = ""))
}






#  *                        _oo0oo_
#  *                       o8888888o
#  *                       88" . "88
#  *                       (| -_- |)
#  *                       0\  =  /0
#  *                     ___/`---'\___
#  *                   .' \\|     |// '.
#  *                  / \\|||  :  |||// \
#  *                 / _||||| -:- |||||- \
#  *                |   | \\\  - /// |   |
#  *                | \_|  ''\---/''  |_/ |
#  *                \  .-\__  '-'  ___/-. /
#  *              ___'. .'  /--.--\  `. .'___
#  *           ."" '<  `.___\_<|>_/___.' >' "".
#  *          | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#  *          \  \ `_.   \_ __\ /__ _/   .-` /  /
#  *      =====`-.____`.___ \_____/___.-`___.-'=====
#  *                        `=---='
#  *
#  *
#  *      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
