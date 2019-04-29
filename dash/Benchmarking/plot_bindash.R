#setwd("MobaXterm/home/Hashing/")
library(SDMTools)

# Using output of quality_vs_coverage_hires.bash
# File has concatenated bindash outputs
file1="bindash_results.txt"
bdash=read.table(file1)

# Or get three vectors instead
# Get coverage
get.cov <- function(line){
	parts = unlist(strsplit(toString(line[1]), "_|.fq"))
	coverage = as.integer(parts[1])
}
# Get quality
get.qual <- function(line){
	parts = unlist(strsplit(toString(line[1]), as.character("_|.fq")))
	quality = as.double(parts[2])
}
# Get Jaccard index (or numerator only)
get.jacc <- function(line){
	parts = unlist(strsplit(line[5], "/"))
	jaccard = as.integer(parts[1])
}
# Populate vectors
vcov = apply(bdash, 1, get.cov)
vqual = apply(bdash, 1, get.qual)
vjacc = apply(bdash, 1, get.jacc)

# For plotting
# Color vector
valcol=vjacc/2048
# Pink scale
pdf(file="bindash_ji.pdf")
plot(vcov, vqual, pch=15, col = rgb(valcol,0,valcol/1.5),
main = "Bindash Jaccard Index", xlab = "Coverage", ylab = "Quality Score Shift")
# For legend
cmap=rgb((0:2048)/2048, 0 , (0:2048)/2048/1.5)
pnts = cbind(x =c(200,210,210,200), y =c(55,55,45,45))
legend.gradient(pnts,cmap,c("0/2048","2048/2048"))
dev.off()
#plot(log(vcov), log(100-vqual), pch=15, col = rgb(valcol,0,0))
