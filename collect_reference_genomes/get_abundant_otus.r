otu.tab <- read.table("data/nash_data/td_OTU_tag_mapped_lineage.txt", header=T, sep="\t", row.names=1, comment.char="", check.names=FALSE)

otu.sum <- apply(otu.tab,1,sum)
total.count <- sum(otu.sum)

one.percent <- 0.01 * total.count
abundant.otus <- rownames(otu.tab)[which(otu.sum > one.percent)]

point.one.percent <- 0.001 * total.count
less.abundant.otus <- rownames(otu.tab)[which(otu.sum > point.one.percent)]

abundant.sum <- sum(otu.sum[which(rownames(otu.tab)%in%abundant.otus)])
abundant.sum/total.count
# [1] 0.5860075

less.abundant.sum <- sum(otu.sum[which(rownames(otu.tab)%in%less.abundant.otus)])
less.abundant.sum/total.count
# [1] 0.954467

length(less.abundant.otus)
# [1] 140

exclude.otus <- rownames(otu.tab)[which(!rownames(otu.tab)%in%less.abundant.otus)]

# manually removed exclude OTUs from OTU seed sequence list (OTU_seed_seqs.fa)
