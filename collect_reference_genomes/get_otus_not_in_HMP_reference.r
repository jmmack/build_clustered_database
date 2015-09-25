data <- read.table("output/blast.out",header=TRUE)
otus.in.hmp <- data[which(data$pident >= 97),]
otus.not.in.hmp <- unique(data$qseqid[which(!as.character(data$qseqid)%in%as.character(otus.in.hmp$qseqid))])
