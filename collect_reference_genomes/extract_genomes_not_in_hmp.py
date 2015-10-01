#############################################################################
# These functions allow one to retrieve NCBI taxon ID using the GI number,
#  and then download the corresponding full bacterial genome.
# The input is a csv BLAST output file, downloaded from the NCBI BLAST webtool.
# Ruth Grace Wong
# ruthgracewong@gmail.com
# October 1, 2015
#############################################################################

import urllib2
import re
from bs4 import BeautifulSoup
from ftplib import FTP

# Extracts taxon ID using GI number, using information found on NCBI website.
def getTaxon(giNumber):
    page = urllib2.urlopen('http://www.ncbi.nlm.nih.gov/nuccore/' + giNumber).read()
    soup = BeautifulSoup(page,"html.parser")
    divText = soup.find(submit_url=re.compile("ORGANISM"))
    search = re.search('ORGANISM=([0-9]*)',str(divText))
    if (search):
        return search.group(1)
    return ""

# Extracts GI numbers from BLAST output.
# In this case I wanted the best match, and one additional match just over
#  97% percent identity if the first match was > 99%.
def getGI(gi,filename):
    otu = {}
    genome2 = {}
    blastResults = open(filename,'r')
    for line in blastResults:
        line = line.strip()
        items = line.split(",")
        if len(items) == 12:
            # if you just want to get all the GI numbers, you would replace the
            #  rest of this for loop with:
            # newGI = items[1].split("|")[1]
            # if newGI not in gi:
            #     gi.add(newGI)
            newOTU = items[0]
            pident = float(items[2])
            if newOTU not in otu:
                otu[newOTU] = pident
                newGI = items[1].split("|")[1]
                if newGI not in gi:
                    gi.add(newGI)
            elif otu[newOTU] > 99:
                if pident > 97:
                    genome2[newOTU] = items[1].split("|")[1]
                else:
                    if newOTU in genome2:
                        newGI = genome2[newOTU]
                        otu[newOTU] = otu[newOTU]*(-1)
                        if newGI not in gi:
                            gi.add(newGI)
    blastResults.close()
    return gi

# Extracts all the taxon ID for all the GI numbers
def getAllTaxon(gi,filename):
    taxon = set()
    taxonOutput = open(filename,'w')
    for i in gi:
        newTaxon = getTaxon(i)
        print("gi "+i+" taxon "+newTaxon)
        if newTaxon not in taxon and newTaxon!="":
            taxon.add(newTaxon)
            taxonOutput.write(newTaxon+"\n")
    taxonOutput.close()
    return taxon

# Downloads all genomes associated with the taxon into the specified folder
def getAllGenomes(taxon, foldername):
    # This file was downloaded from ftp://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_genbank.txt
    genbank = open('data/assembly_summary_genbank.txt','r')
    ftp = FTP('ftp.ncbi.nlm.nih.gov')     # connect to host, default port
    ftp.login()
    for line in genbank:
        if line[0]!='#':
            items = line.split("\t")
            if len(items) == 20:
                currentTaxon  = items[5]
                if currentTaxon in taxon:
                    # Get the FTP link to the genome for the taxa
                    genomeFolder = items[19].strip()
                    if genomeFolder!="":
                        # removing ftp://ftp.ncbi.nlm.nih.gov from beginning of genome folder path
                        genomeFolder = genomeFolder[26:]
                        filename = genomeFolder.split("/")[-1].strip()
                        if filename!="":
                            print("attempting to retrieve " + filename + "_genomic.fna.gz" + " from " + genomeFolder + " for taxon " + currentTaxon)
                            ftp.cwd(genomeFolder)
                            localGenome = open(foldername + filename + "_genomic.fna.gz", 'wb')
                            ftp.retrbinary('RETR %s' % filename + "_genomic.fna.gz", localGenome.write)
                            localGenome.close()
    genbank.close()

### Calling the functions
gi = set()
# A bug in NCBI BLAST made it necessary for me to search the wgs database for
#  bacterial draft genomes separately from the complete genomes
getGI(gi,'./output/wgs-Alignment-HitTable.csv')
print("Extracted " + str(len(gi)) + " gi numbers from wgs output")
getGI(gi,'./output/complete-genomes-Alignment-HitTable.csv')
print("Extracted " + str(len(gi)) + " gi numbers from wgs and complete genome output")
taxon = getAllTaxon(gi,'./data/taxon_not_in_hmp.txt')
print("Output all taxon")
getAllGenomes(taxon,'data/genomes/')
print("Complete")
