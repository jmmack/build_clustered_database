# Collect Reference Genomes

This is Ruth's case-specific workflow for finding genomes to create a functional mapping library for a metagenomic study. A list of relevant genomes was created by amalgamating the HMP gut reference genomes with relevant genomes from the NCBI complete and draft bacterial genomes.

## Find out which OTUs are >= 1% abundance

In this experiment, the sequencing depth will only have on average 1x coverage of bacteria that are 1% abundant in a sample. The code for extracting the relevant OTU sequences is in get_abundant_otus.r

The OTU table is read in this line

```R
otu.tab.taxonomy <- read.table("data/nash_data/otus_by_ALL.txt", header=T, sep="\t", row.names=1, comment.char="", check.names=FALSE, stringsAsFactors=FALSE)
```
and the OTU sequences are read in this line

```R
fasta.in <- read.table("data/OTU_seed_seqs.fa", sep="\t",stringsAsFactors=FALSE)
```

The different sections do different things, so cut and paste what you need.

## BLAST OTU seed sequences with Human Microbiome Project data set

The gut HMP reference genomes were downloaded from http://hmpdacc.org/HMRGD/healthy/

To run local BLAST on the

```bash
nohup blastn -db hmp_genomes/all_seqs.fa -query data/OTU_seed_seqs_less_common_removed.fa -out output/blast.out -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen' -evalue 1e-3 -num_alignments 10 -num_threads 4 > blast_nohup.out 2>&1&
```

output list of sequences that don’t have a > 97% identity match using get_otus_not_in_hmp.r

## Find matches in the NCBI complete and draft bacterial genomes for the OTUs that don’t match to the HMP data set

I ran into a bug using the NCBI webtool, and had to search once through the wgs database, and once with Complete Genomes to get both the draft and the complete genomes.

Blast against draft and complete bacterial genomes with NCBI: http://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastSearch&BLAST_SPEC=MicrobialGenomes

I put my BLAST output (Downloaded in CSV format) in data/complete-genomes-Alignment-HitTable.csv and wgs-Alignment-HitTable.csv and data/wgs-Alignment-HitTable.csv and wgs-Alignment-HitTable.csv.

## Retrieve the genome for the matches

This is done in the script extract_taxon_not_in_hmp.py. It requires you to make a folder named genome inside the folder named data, and uses the blast outputs generated in the previous section.

I only wanted genomes that were the best match for each OTU. If there was a match > 99% percent identity, then I wanted a second genome that had a percent identity just over 97%. The script extracts the gi numbers for such matches, and then crawls the NCBI nuccore website to find the taxon ID. The taxon ID is found in ftp://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_genbank.txt and the corresponding FTP link is used to download the genome.

The script can be run on the command line:

```bash
nohup python extract_taxon_not_in_hmp.py > get_taxon_nohup.out 2>&1&
```

The download genomes are compressed. To uncompress, navigate to the folder in terminal and run:
```bash
gunzip *.gz
```

The end result is that all the genomes I need for my functional mapping library are in data/genomes/ and the HMP reference genomes.
