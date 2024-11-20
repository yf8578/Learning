# 绘制基因表达的箱线图函数
# Compare_list<-list(c("T1", "T2"), c("T1", "T3"), c("T1", "T4"), c("T1", "T5"), c("T2", "T3"), c("T2", "T4"), c("T2", "T5"), c("T3", "T4"), c("T3", "T5"), c("T4", "T5"))
# 好像还需要ggpubr？
#这个是登山数据代码，大致就是这样
Gene_boxplot <- function(Gene_data, Gene_name, Compare_list) {
    p <- Gene_data %>%
        ggplot(aes(x = Time, y = expre, fill = Time)) +
        # 绘制误差棒
        stat_boxplot(geom = "errorbar", width = 0.6, aes(x = Time, y = expre, group = Time)) +
        # 绘制box
        geom_boxplot() +
        # scale_fill_viridis(discrete = TRUE, alpha = 0.6) +
        # 绘制数据点分布位置
        # geom_jitter(color = "#000000", size = 0.4, alpha = 0.9) +
        # 白色背景，但是存在字体问题
        # theme_ipsum() +
        # 变成深色背景
        # theme_ft_rc()+
        theme(
            legend.position = "right",
            plot.title = element_text(size = 11)
        ) +
        ggtitle(Gene_name) +
        xlab("") +
        geom_signif(comparisons = Compare_list, step_increase = 0.1, map_signif_level = T) +
        stat_compare_means(label.y = max(Gene_data$expre) * 2)
    return(p)
}
