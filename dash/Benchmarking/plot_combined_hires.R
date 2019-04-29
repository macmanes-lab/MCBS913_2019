#setwd("MobaXterm/home/Hashing/")
library(SDMTools)

# File has concatenated bindash outputs
file1="bindash_results.txt"
bdash=read.table(file1)

# Get three vectors for plotting
# Get coverage
get.cov.b <- function(line){
	parts = unlist(strsplit(toString(line[1]), "_|.fq"))
	coverage = as.integer(parts[1])
}
# Get quality
get.qual.b <- function(line){
	parts = unlist(strsplit(toString(line[1]), as.character("_|.fq")))
	quality = as.double(parts[2])
}
# Get Jaccard index (or numerator only)
get.jacc.b <- function(line){
	parts = unlist(strsplit(line[5], "/"))
	jaccard = as.integer(parts[1])
}
# Populate vectors
vcov_b = apply(bdash, 1, get.cov.b)
vqual_b = apply(bdash, 1, get.qual.b)
vjacc_b = apply(bdash, 1, get.jacc.b)

# For plotting

# Color vector
valcol_b=vjacc_b/2048

X11()

# # Pink scale
# plot(vcov_b, vqual_b, pch=15, col = rgb(valcol_b,0,valcol_b/1.5),
# main = "Bindash Jaccard Index", xlab = "Coverage", ylab = "Quality Score Shift")
# # For legend
# cmap_b =rgb((0:2048)/2048, 0 , (0:2048)/2048/1.5)
# #pnts_b = cbind(x =c(200,210,210,200), y =c(55,55,45,45))
# #pnts_b = cbind(x =c(0,0,0,0), y =c(0,0,0,0))
# #legend.gradient(pnts_b,cmap_b,c("0/2048","2048/2048"))

# Blue version
plot(vcov_b, vqual_b, pch=15, col = rgb(0,0,valcol_b),
main = "Bindash Jaccard Index", xlab = "Coverage", ylab = "Quality Score Shift")
# For legend
cmap_b =rgb(0, 0 , (0:2048)/2048)
pnts_b = cbind(x =c(200,210,210,200), y =c(55,55,45,45))
legend.gradient(pnts_b,cmap_b,c("0/2048","2048/2048"))

# File has dashing distance matrix outputs
file2="dashing_distance_matrix.txt"
dashing=read.table(file2)

# Get coverage
get.cov.d <- function(line){
	filename = unlist(strsplit(toString(line), "/|.fq"))[2]
	coverage = unlist(strsplit(filename, "_"))[1]
}

# Get quality
get.qual.d <- function(line){
	filename = unlist(strsplit(toString(line), "/|.fq"))[2]
	coverage = unlist(strsplit(filename, "_"))[2]
}

# Getting from last column
vcov_d = sapply(dashing[1:(length(dashing)-2),1], get.cov.d)
vqual_d = sapply(dashing[1:(length(dashing)-2),1], get.qual.d)
vjacc_d = dashing[1:(length(dashing)-2),length(dashing)]

# For plotting

X11()

# Color vector
valcol_d = as.numeric(as.character(vjacc_d))

# Pink scale
plot(vcov_d, vqual_d, pch=15, col = rgb(valcol_d,0,valcol_d/1.5),
main = "Dashing Jaccard Index", xlab = "Coverage", ylab = "Quality Score Shift")
# For legend
cmap_d=rgb((0:2048)/2048, 0 , (0:2048)/2048/1.5)
pnts_d = cbind(x =c(200,210,210,200), y =c(55,55,45,45))
legend.gradient(pnts_d,cmap_d,c("0","1"))
# Red version
plot(vcov_d, vqual_d, pch=15, col = rgb(valcol_d,0,0),
main = "Dashing Jaccard Index", xlab = "Coverage", ylab = "Quality Score Shift")
# For legend
cmap_d=rgb((0:2048)/2048, 0 , 0)
pnts_d = cbind(x =c(200,210,210,200), y =c(55,55,45,45))
legend.gradient(pnts_d,cmap_d,c("0","1"))

X11()

# Make new vector to match
# Make array of bindash
covs=1:50
quals=seq(-20,30, by=2)
moew=matrix(nrow=length(covs), ncol=length(quals))
rownames(moew) = covs
colnames(moew) = quals
for (i in 1:length(vjacc_b)){
	moew[as.character(vcov_b[i]),as.character(vqual_b[i])] = vjacc_b[i]
}
vjacc_b2 = c()
# Populate vector of bindash distances to correspond to order of dashing
for (i in 1:length(vjacc_d)){
	vjacc_b2[i] = moew[vcov_d[i], vqual_d[i]]
}
valcol_b2=vjacc_b2/2048

plot(vcov_d, vqual_d, pch=15, col = rgb(valcol_d,0,valcol_b2), cex=1.5,
main = "Combined Jaccard Index", xlab = "Coverage", ylab = "Quality Score Shift")

# Separate for legend
X11()
reds=seq(0,1,0.1)
blues=seq(0,1,0.1)
xs=rep(seq(0,1,0.1),times=11)
ys=as.vector(rbind(reds,reds,reds,reds,reds,reds,reds,reds,reds,reds,reds))
plot(xs, ys, pch=15, col = rgb(xs,0,ys), cex=7.2,
xlab="Dashing JI", ylab="Bindash JI", main="Legend")

# Pink dashing legend only
plot(ys, xs, pch=15, col = rgb(xs,0,xs/1.5), cex=4, ylab="Jaccard Index", xlab = NA, xaxt='n', main="Legend")