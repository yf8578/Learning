# 输出10以内的奇数
for (i in 1:10) {
    if (i %% 2 == 1) {
        print(i)
    }
}

# install.packages("ggplot2")
library(ggplot2)

# Data with dates and variables. The column 'date' is of class "Date"
df <- economics[economics$date > as.Date("2000-01-01"), ]

ggplot(df, aes(x = date, y = unemploy)) +
    geom_line()

h <- c(1, 2, 3, 4, 5, 6)
M <- c("A", "B", "C", "D", "E", "F")
barplot(h,
    names.arg = M, xlab = "X", ylab = "Y",
    col = "#00cec9", main = "Chart", border = "#fdcb6e"
)

