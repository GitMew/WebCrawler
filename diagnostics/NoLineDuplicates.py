# 2018-02-28
def lookup(filename,str,start,interval):
    with open(filename) as handle:
        contain = False
        for n,line in enumerate(handle,1):
            if n >= start:
                if str in line:
                    contain = True
                if n - start + 1 == interval:
                    break
    return contain
file = input("File path: ")
with open("noduplicates.txt","a+") as main:
    with open(file,"r+") as handle:
        for n,line in enumerate(handle,1):
            print(n)
            if not(lookup(file,line.strip("\n"),n+1,100)):
                main.write(line)