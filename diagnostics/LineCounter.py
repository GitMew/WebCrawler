file = input("File path: ")
i = 0
with open(file,"r") as handle:
    for line in handle:
        i += 1
print(file + " contains %s lines" % i)