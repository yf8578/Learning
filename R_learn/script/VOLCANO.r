#-*-coding:utf-8-*-
# /*
#* @Author: zhangyifan1
#* @Date: 2023-07-12 10:08:40
#* @LastEditors: zhangyifan1 zhangyifan1@genomics.cn
#* @LastEditTime: 2023-07-12 16:46:24
#* @FilePath: \01hilld:\000zyf\work\R_learn\script\VOLCANO.r
#* @Description:
#*
#* /
# 火山图
VOLCANO <- function(plot_data, GROUP_NAME) {
    library(ggplot2)
    library(ggsci)
    p <- ggplot(
        data = plot_data,
        aes(x = plot_data$log2FoldChange, y = -log10(plot_data$padj), color = plot_data$sig)
    ) +
        geom_point(size = 1) + # 绘制散点图
        scale_color_manual(
            values = c("red", "gray", "green"),
            limits = c("up", "none", "down")
        ) + # 自定义点的颜色
        labs(
            x = "log2 Fold Change", y = "-log10 adjust p-value",
            title = GROUP_NAME, color = ""
        ) + # 坐标轴标题
        theme(
            plot.title = element_text(hjust = 0.5, size = 14),
            panel.grid = element_blank(), # 背景色、网格线、图例等主题修改
            panel.background = element_rect(
                color = "black",
                fill = "transparent"
            ),
            legend.key = element_rect(fill = "transparent")
        ) +
        geom_vline(xintercept = c(-1, 1), lty = 3, color = "black") + # 添加阈值线
        geom_hline(yintercept = -log10(0.05), lty = 3, color = "black")
    # xlim(-12, 12) + ylim(0, 40)  #定义刻度边界

    # 保存图片
    ggsave(p, file = paste(GROUP_NAME, "_volcano.png", sep = ""))
}
