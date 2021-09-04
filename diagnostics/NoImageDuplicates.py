import os
import math
def lookup(filename,str):
    bytes = str.replace("\r","").replace("\t","").replace("\n","").replace("\v","").encode()
    with open(filename, "rb") as handle:
        for line in handle:
            if bytes == line.replace(b"\r",b"").replace(b"\t",b"").replace(b"\n",b"").replace(b"\v",b""):
                return True

filelist = []
cwd = input("Folder path: ")
directory = os.fsencode(cwd)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        filelist.append(os.path.join(cwd, filename))

open("dellist.txt","a+")
l = len(filelist)
b = 1 + math.floor(l/1000)
for k in range(b):
    for i in range(1,1000):
        print("Batch " + str(k+1) + ", image " + str(i))
        for j in range(i+1,1001):
            if open(filelist[1000*k+i-1],"rb").read() == open(filelist[1000*k+j-1],"rb").read():
                input(filelist[1000*k+i-1] + " seems to be matching " + filelist[1000*k+j-1] + ". Please check to see if the program is working correctly.")
                with open("dellist.txt","a+") as handle:
                    if not(lookup("dellist.txt",filelist[1000*k+j-1])):
                        handle.write(filelist[1000*k+j-1]+"\n")
            if 1000*k+j-1 == l-1:
                break
        if 1000*k+i-1 == l-2:
            break

print("Deletion currently disabled.")
#with open("dellist.txt","r+") as handle:
#    for path in handle:
#        p = path.strip("\n")
#        os.remove(p)
#        print("Deleting " + p + ".")
#
#os.remove("dellist.txt")