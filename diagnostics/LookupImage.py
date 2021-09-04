import os

img = input("Path of image to match: ")
cwd = input("Path of folder to search through: ")
directory = os.fsencode(cwd)
filelist = []
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        filelist.append(os.path.join(cwd, filename))

m = 0        
for i in range(len(filelist)):
    if open(img,"rb").read() == open(filelist[i],"rb").read():
        print("Found a match! The name of the match is " + filelist[i] + ".")
        m += 1
    if i % 1000 == 0:
        print("Checked " + str(i+1) + " ...")
        
print("Total matches: " + str(m))