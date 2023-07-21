# Load ggplot2
library(ggplot2)

# create dummy data
data <- data.frame(
  name=letters[1:5],
  value=sample(seq(4,15),5),
  sd=c(1,0.2,3,2,4)
)

# rectangle
ggplot(data) +
  geom_bar( aes(x=name, y=value), stat="identity", fill="skyblue", alpha=0.5) +
  geom_crossbar( aes(x=name, y=value, ymin=value-sd, ymax=value+sd), width=0.4, colour="orange", alpha=0.9, size=1.3)

# line
ggplot(data) +
  geom_bar( aes(x=name, y=value), stat="identity", fill="skyblue", alpha=0.5) +
  geom_linerange( aes(x=name, ymin=value-sd, ymax=value+sd), colour="orange", alpha=0.9, size=1.3)

# line + dot
ggplot(data) +
  geom_bar( aes(x=name, y=value), stat="identity", fill="skyblue", alpha=0.5) +
  geom_pointrange( aes(x=name, y=value, ymin=value-sd, ymax=value+sd), colour="orange", alpha=0.9, size=1.3)

# horizontal
ggplot(data) +
  geom_bar( aes(x=name, y=value), stat="identity", fill="skyblue", alpha=0.5) +
  geom_errorbar( aes(x=name, ymin=value-sd, ymax=value+sd), width=0.4, colour="orange", alpha=0.9, size=1.3) +
  coord_flip()


#Move packages
#在A设备/版本保存名字列表
oldip <- installed.packages()[,1]
save(oldip,file = "installedPacckages.Rdata")
#在B设备/版本上进行安装；
load("installedPacckages.Rdata")
newip <- installed.packages()[,1]
for (i in setdiff(oldip,newip)) {
  install.packages(i)
}


# Load ggplot2
library(ggplot2)
library(hrbrthemes) # for style

# make data
data <- data.frame(
  group=c("A ","B ","C ","D ") , 
  value=c(33,62,56,67) , 
  number_of_obs=c(100,500,459,342)
)

# Calculate the future positions on the x axis of each bar (left border, central position, right border)
data$right <- cumsum(data$number_of_obs) + 30*c(0:(nrow(data)-1))
data$left <- data$right - data$number_of_obs 

# Plot
ggplot(data, aes(ymin = 0)) + 
  geom_rect(aes(xmin = left, xmax = right, ymax = value, colour = group, fill = group)) +
  xlab("number of obs") + 
  ylab("value") +
  theme_ipsum() +
  theme(legend.position="none") 
# Libraries
library(ggplot2)
library(dplyr)
library(hrbrthemes)
library(viridis)

# create a dataset
data <- data.frame(
  name=c( rep("A",500), rep("B",500), rep("B",500), rep("C",20), rep('D', 100)  ),
  value=c( rnorm(500, 10, 5), rnorm(500, 13, 1), rnorm(500, 18, 1), rnorm(20, 25, 4), rnorm(100, 12, 1) )
)

# sample size
sample_size = data %>% group_by(name) %>% summarize(num=n())

# Plot
data %>%
  left_join(sample_size) %>%
  mutate(myaxis = paste0(name, "\n", "n=", num)) %>%
  ggplot( aes(x=myaxis, y=value, fill=name)) +
  geom_violin(width=1.4) +
  geom_boxplot(width=0.1, color="grey", alpha=0.2) +
  scale_fill_viridis(discrete = TRUE) +
  theme_ipsum() +
  theme(
    legend.position="none",
    plot.title = element_text(size=11)
  ) +
  ggtitle("A Violin wrapping a boxplot") +
  xlab("")


# install.packages("ggplot2")
library(ggplot2)

# Data with dates and variables. The column 'date' is of class "Date"
df <- economics[economics$date > as.Date("2000-01-01"), ]

ggplot(df, aes(x = date, y = unemploy)) +
  geom_line() 



#输出10以内的奇数
for (i in 1:10){
  if (i%%2==1){
    print(i)
  }
}
