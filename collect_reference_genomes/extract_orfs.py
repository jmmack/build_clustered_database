featureTableFileName = "~/Downloads/test/GCA_000432675.1_MGS50_feature_table.txt"
fnaFilename = "~/Downloads/test/GCA_000432675.1_MGS50_genomic.fna"

def outputCodingSequences(featureTableFilename, fnaFilename, outputFilename):
    fna = open(fnaFilename, 'r')
    sequences = {}
    isId = True
    id = ""
    for line in fna:
        if (isId):
            id = line.split()[0]
            # get rid of the ">" at the beginning of each line
            id = id[1:]
            isId = False
        else:
            sequences[id] = line.strip()
            id = ""
            isId = True
    fna.close()
    featureTable = open(featureTableFilename,'r')
    output = open(outputFilename,'w')
    for line in featureTable:
        if line[:3] == "CDS":
            items = line.split("\t")
            seqid = items[6].strip()
            protid = items[10].strip()
            start = items[7].strip()
            end = items[8].strip()
            sequence = sequences[seqid][(start-1):end].strip()
            output.write(">genomic_accession|"+seqid+"|product_accession|"+protid+"\n")
            output.write(sequence+"\n")
    featureTable.close()
    output.close()