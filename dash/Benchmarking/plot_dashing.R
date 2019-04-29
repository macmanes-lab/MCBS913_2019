#setwd("MobaXterm/home/Hashing/")
library(SDMTools)

# Using output of quality_vs_coverage_hires.bash
# File has dashing distance matrix output
file1="dashing_distance_matrix.txt"
dashing=read.table(file1)

# Get coverage
get.cov <- function(line){
	filename = unlist(strsplit(toString(line), "/|.fq"))[2]
	coverage = unlist(strsplit(filename, "_"))[1]
}

# Get quality
get.qual <- function(line){
	filename = unlist(strsplit(toString(line), "/|.fq"))[2]
	coverage = unlist(strsplit(filename, "_"))[2]
}

vlen=length(dashing)-2
vcov = sapply(dashing[1:vlen,1], get.cov)
vqual = sapply(dashing[1:vlen,1], get.qual)
vjacc = dashing[1:vlen,vlen+2]

# For plotting
# Color vector
valcol=as.numeric(as.character(vjacc))

# Pink scale
pdf(file="dashing_ji.pdf")
plot(vcov, vqual, pch=15, col = rgb(valcol,0,valcol/1.5),
main = "Dashing Jaccard Index", xlab = "Coverage", ylab = "Quality Score Shift")
# For legend
cmap=rgb((0:2048)/2048, 0 , (0:2048)/2048/1.5)
pnts = cbind(x =c(200,210,210,200), y =c(55,55,45,45))
legend.gradient(pnts,cmap,c("0/2048","2048/2048"))
dev.off()