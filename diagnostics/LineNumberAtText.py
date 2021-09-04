def numAtLine(filename,linestring):
    with open(filename) as handle:
        for n, line in enumerate(handle, 1):
            if line.strip("\n") == linestring:
                return n
                
print(numAtLine(input("File path: "),input("Text: ")))