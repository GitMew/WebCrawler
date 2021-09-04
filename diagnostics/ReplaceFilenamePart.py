import os

filelist = []
cwd = input("Folder path: ")
old = input("Part to replace: ")
new = input("Replace with: ")
directory = os.fsencode(cwd)
for file in os.listdir(directory):
    os.rename(directory + b"/" + file, directory + b"/" + file.replace(old.encode(),new.encode()))