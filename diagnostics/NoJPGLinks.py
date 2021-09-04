file = input("File path: ")
with open("noJPG.txt","w+") as main:
    with open(file,"r+") as handle:
        for line in handle:
            if not(".jpg" in line.lower()):
                main.write(line)