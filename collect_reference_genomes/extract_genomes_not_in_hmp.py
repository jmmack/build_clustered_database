import urllib2
import re
from bs4 import BeautifulSoup

def getTaxon(giNumber):
    page = urllib2.urlopen('http://www.ncbi.nlm.nih.gov/nuccore/' + giNumber).read()
    soup = BeautifulSoup(page,"html.parser")
    divText = soup.find(submit_url=re.compile("ORGANISM"))
    search = re.search('ORGANISM=([0-9]*)',str(divText))
    if (search):
        return search.group(1)
    return ""

def getGI(gi,filename):
    otu = {}
    genome2 = {}
    blastResults = open(filename,'r')
    for line in blastResults:
        line = line.strip()
        items = line.split(",")
        if len(items) == 12:
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


gi = set()
getGI(gi,'./output/wgs-Alignment-HitTable.csv')
print("Extracted " + str(len(gi)) + " gi numbers from wgs output")
getGI(gi,'./output/complete-genomes-Alignment-HitTable.csv')
print("Extracted " + str(len(gi)) + " gi numbers from wgs and complete genome output")
getAllTaxon(gi,'./output/taxon_not_in_hmp.txt')
print("Complete")
