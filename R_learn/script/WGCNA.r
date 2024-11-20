
library(WGCNA)
library(reshape2)
library(stringr)

yy="A-m-1"

# 
options(stringsAsFactors = FALSE)
# �򿪶��߳�
enableWGCNAThreads()
## Allowing parallel execution with up to 47 working processes.

# ���������log2ת�����
# Deseq2��varianceStabilizingTransformationת��������
# ���������ЧӦ����Ҫ�����Ƴ�����ʹ��removeBatchEffect
# �����ϵͳƫ��(����boxplot�鿴������ֲ��Ƿ�һ��)��
# ��Ҫquantile normalization

#exprMat <- "D:/work/stroke/MG/raw/expression profile/input/mRNA_final.txt"
exprMat <- paste("/home/wyy/SZ/input/",yy,".txt",sep = "");

# �ٷ��Ƽ� "signed" �� "signed hybrid"
# Ϊ��ԭ�ĵ�һ�£���δ�޸� 
type = "unsigned"

# ����Լ���
# �ٷ��Ƽ� biweight mid-correlation & bicor
# corType: pearson or bicor
# Ϊ��ԭ�ĵ�һ�£���δ�޸�
corType = "pearson"

corFnc = ifelse(corType=="pearson", cor, bicor)
# �Զ�Ԫ��������������״��Ϣ���������ʱ��
# ����������������ڼ���״̬ʱ���������������
maxPOutliers = ifelse(corType=="pearson",1,0.05)

# ������Ʒ��״�Ķ�Ԫ����ʱ������
robustY = ifelse(corType=="pearson",T,F)
##��������##
dataExpr <- read.table(exprMat, sep='\t', row.names=1, header=T, 
                       quote="", comment="", check.names=F)

dim(dataExpr)

## [1] 3600  134

#head(dataExpr)[,1:8]

###############################
## ɸѡ��λ����ƫ��ǰ75%�Ļ�������MAD����0.01
## ɸѡ��ή����������Ҳ��ʧȥ������Ϣ
## Ҳ�ɲ���ɸѡ��ʹMAD����0����
m.mad <- apply(dataExpr,1,mad)
dataExprVar <- dataExpr[which(m.mad >max(quantile(m.mad, probs=seq(0, 1, 0.25))[2],0.01)),]

## ת��Ϊ��Ʒ���У��������еľ���
dataExpr <- as.data.frame(t(dataExprVar))

## ���ȱʧֵ
gsg = goodSamplesGenes(dataExpr, verbose = 3)

##  Flagging genes and samples with too many missing values...
##   ..step 1

if (!gsg$allOK){
  # Optionally, print the gene and sample names that were removed:
  if (sum(!gsg$goodGenes)>0) 
    printFlush(paste("Removing genes:", 
                     paste(names(dataExpr)[!gsg$goodGenes], collapse = ",")));
  if (sum(!gsg$goodSamples)>0) 
    printFlush(paste("Removing samples:", 
                     paste(rownames(dataExpr)[!gsg$goodSamples], collapse = ",")));
  # Remove the offending genes and samples from the data:
  dataExpr = dataExpr[gsg$goodSamples, gsg$goodGenes]
}

nGenes = ncol(dataExpr)
nSamples = nrow(dataExpr)

dim(dataExpr)

## [1]  134 2697

head(dataExpr)[,1:8]

#����ֵɸѡ,����ֵ��ɸѡԭ����ʹ����������������ޱ������������
## �鿴�Ƿ�����Ⱥ��Ʒ
sampleTree = hclust(dist(dataExpr), method = "average");
pdf(paste("/home/wyy/SZ/figures/Fig1-",yy,".pdf",sep = ""))
plot(sampleTree, main = "Sample clustering to detect outliers", sub="", xlab="")
dev.off()

powers = c(c(1:10), seq(from = 12, to=30, by=2))
sft = pickSoftThreshold(dataExpr, powerVector=powers, 
                        networkType=type, verbose=5)
pdf(paste("/home/wyy/SZ/figures/Fig2-",yy,".pdf",sep = ""))
par(mfrow = c(1,2))
cex1 = 0.9
# ������Soft threshold (power)���������ޱ�������������������ֵԽ�ߣ�
# ����Խ�����ޱ������ (non-scale)
plot(sft$fitIndices[,1], -sign(sft$fitIndices[,3])*sft$fitIndices[,2],
     xlab="Soft Threshold (power)",
     ylab="Scale Free Topology Model Fit,signed R^2",type="n",
     main = paste("Scale independence"))
text(sft$fitIndices[,1], -sign(sft$fitIndices[,3])*sft$fitIndices[,2],
     labels=powers,cex=cex1,col="red")
# ɸѡ��׼��R-square=0.85
abline(h=0.85,col="red")

# Soft threshold��ƽ����ͨ��
plot(sft$fitIndices[,1], sft$fitIndices[,5],
     xlab="Soft Threshold (power)",ylab="Mean Connectivity", type="n",
     main = paste("Mean connectivity"))
text(sft$fitIndices[,1], sft$fitIndices[,5], labels=powers, 
     cex=cex1, col="red")
dev.off()

power = sft$powerEstimate
power
#########����power (������������powerʱѡ��)
# ����������powerС��15����������powerС��30�ڣ�û��һ��powerֵ����ʹ
# �ޱ������ͼ�׽ṹR^2�ﵽ0.8��ƽ�����ӶȽϸ�����100���ϣ�����������
# ������Ʒ��������Ʒ���̫�������������ЧӦ����Ʒ�����Ի�ʵ��������
# ���Ӱ��̫�����ɡ�����ͨ��������Ʒ����鿴������Ϣ�������쳣��Ʒ��
# �����ȷʵ���������������仯����ģ�Ҳ����ʹ������ľ���powerֵ��
if (is.na(power)){
  power = ifelse(nSamples<20, ifelse(type == "unsigned", 9, 18),
                 ifelse(nSamples<30, ifelse(type == "unsigned", 8, 16),
                        ifelse(nSamples<40, ifelse(type == "unsigned", 7, 14),
                               ifelse(type == "unsigned", 6, 12))       
                 )
  )
}

#######���繹��
##һ�������繹����One-step network construction and module detection##
# power: ��һ�����������ֵ
# maxBlockSize: ������ܴ�������ģ��Ļ������� (Ĭ��5000)��
#  4G�ڴ���Կɴ���8000-10000����16G�ڴ���Կ��Դ���2�����32G�ڴ���Կ�
#  �Դ���3���
#  ������Դ������������÷���һ��block���档
# corType: pearson or bicor
# numericLabels: �������ֶ�������ɫ��Ϊģ������֣����������ת��Ϊ��ɫ
# saveTOMs����ķ�ʱ��ļ��㣬�洢������������ʹ��
# mergeCutHeight: �ϲ�ģ�����ֵ��Խ��ģ��Խ��
net = blockwiseModules(dataExpr, power = power, maxBlockSize = nGenes,
                       TOMType = type, minModuleSize = 30,
                       reassignThreshold = 0, mergeCutHeight = 0.25,
                       numericLabels = TRUE, pamRespectsDendro = FALSE,
                       saveTOMs=TRUE, corType = corType, 
                       maxPOutliers=maxPOutliers, loadTOMs=TRUE,
                       saveTOMFileBase = paste0(exprMat, ".tom"),
                       verbose = 3)
# ����ģ���л�����Ŀ�Ķ��٣��������У����α��Ϊ `1-���ģ����`��
# **0 (grey)**��ʾ**δ**�����κ�ģ��Ļ��� 
table(net$colors)

#�㼶������չʾ����ģ��
## ��ɫ��Ϊ**δ����**��ģ��Ļ���
# Convert labels to colors for plotting
moduleLabels = net$colors
moduleColors = labels2colors(moduleLabels)
# Plot the dendrogram and the module colors underneath
# ����Խ�������⣬������recutBlockwiseTrees����ʡ����ʱ��
pdf(paste("/home/wyy/SZ/figures/Fig3-",yy,".pdf",sep = ""))
plotDendroAndColors(net$dendrograms[[1]], moduleColors[net$blockGenes[[1]]],
                    "Module colors",
                    dendroLabels = FALSE, hang = 0.03,
                    addGuide = TRUE, guideHang = 0.05)

dev.off()
#����ģ��֮�������ͼ
# module eigengene, ���Ի�����ͼ����Ϊÿ��ģ��Ļ��������Ƶ�չʾ
MEs = net$MEs

### ����Ҫ���¼��㣬���������־ͺ�
### �ٷ��̳������¼���ģ���ʵ���Բ�����ô�鷳
MEs_col = MEs
colnames(MEs_col) = paste0("ME", labels2colors(
  as.numeric(str_replace_all(colnames(MEs),"ME",""))))
MEs_col = orderMEs(MEs_col)

# ���ݻ�����������о������õ��ĸ�ģ���������ͼ
# marDendro/marHeatmap �����¡����ϡ��ҵı߾�
pdf(paste("/home/wyy/SZ/figures/Fig4-",yy,".pdf",sep = ""))
plotEigengeneNetworks(MEs_col, "Eigengene adjacency heatmap", 
                      marDendro = c(3,3,2,4),
                      marHeatmap = c(3,4,2,2), plotDendrograms = T, 
                      xLabelsAngle = 90)
## ����б������ݣ�Ҳ���Ը�ME���ݷ�һ��һ���ͼ
#MEs_colpheno = orderMEs(cbind(MEs_col, traitData))
#plotEigengeneNetworks(MEs_colpheno, "Eigengene adjacency heatmap", 
#                      marDendro = c(3,3,2,4),
#                      marHeatmap = c(3,4,2,2), plotDendrograms = T, 
#                      xLabelsAngle = 90)
dev.off();

#���ӻ��������� (TOM plot)
# ������÷ֲ����㣬�����õ�blocksize>=�ܻ�������ֱ��load����õ�TOM���
# ������Ҫ�ټ���һ�飬�ȽϺķ�ʱ��
# TOM = TOMsimilarityFromExpr(dataExpr, power=power, corType=corType, networkType=type)
load(net$TOMFiles[1], verbose=T)

## Loading objects:
##   TOM

TOM <- as.matrix(TOM)

dissTOM = 1-TOM
# Transform dissTOM with a power to make moderately strong 
# connections more visible in the heatmap
plotTOM = dissTOM^7
# Set diagonal to NA for a nicer plot
diag(plotTOM) = NA
# Call the plot function

pdf(paste("/home/wyy/SZ/figures/Fig5-",yy,".pdf",sep = ""))
# ��һ�����ر��ʱ������ͬʱ���㼶����
TOMplot(plotTOM, net$dendrograms, moduleColors,main = "Network heatmap plot")
dev.off()
#Export the network into edge and node list files Cytoscape can read
#threshold Ĭ��Ϊ0.5, ���Ը����Լ�����Ҫ������Ҳ���Զ���������
#cytoscape���ٵ���
probes = colnames(dataExpr) 
dimnames(TOM) <- list(probes, probes)
cyt = exportNetworkToCytoscape(TOM, edgeFile = paste("/home/wyy/SZ/network/",yy,"-module-edge.txt",sep = ""), nodeFile = paste("/home/wyy/SZ/network/",yy,"-module-node.txt",sep = ""), weighted = TRUE, threshold = 0, nodeNames = probes, nodeAttr = moduleColors)
