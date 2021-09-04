def txtAtLinenum(filename,linenumber):
    with open(filename) as handle:
        for n, line in enumerate(handle, 1):
            if n == linenumber:
                return line.strip("\n")

print(txtAtLinenum(input("File path: "),int(input("Look up text at line n°: "))))