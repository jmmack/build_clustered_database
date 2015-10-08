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
             