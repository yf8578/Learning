# 数据来自list列表

UpSet_plot <- function(Data) {
    # 判断是否存在upsetR包，如果不存在则安装
    if (!require(UpSetR)) {
        install.packages("UpSetR")
        library(UpSetR)
    }

    upset_plot <- upset(fromList(Data),
        keep.order = T, matrix.color = "#676565", main.bar.color = "#676565",
        sets.bar.color = "#676565", shade.color = "#918f8f",
        mb.ratio = c(0.65, 0.35), point.size = 5, line.size = 3,
        sets = rev(colnames(fromList(Data))), # order.by = "freq",
        nsets = dim(fromList(Data))[2], text.scale = 5,
        mainbar.y.label = "Name", set_size.show = TRUE,
        set_size.angles = 70, # set_size.numbers_size = 8,
        queries = list(list(query = intersects, params = list("group_a", "group_b", "group_c", "group_d", "group_e"), active = T, color = "#f34d06"))
        # queries = list(list(query = intersects, params = list(colnames(fromList(upgene))), active = T))
    )

    return(upset_plot)
}

a <- list("apple", "banana", "pear", "oranges", "liulian")
b <- list("apple", "banana", "pear", "oranges", "liulian", "watermelon")
c <- list("apple", "oranges", "liulian", "watermelon", "mango")
d <- list("pear", "oranges", "liulian", "watermelon", "mango", "pineapple")
e <- list("apple", "banana", "pear", "oranges", "liulian", "watermelon", "mango", "pineapple", "strawberry")
Data <- list(group_a = a, group_b = b, group_c = c, group_d = d, group_e = e)

UpSet_plot(Data)
