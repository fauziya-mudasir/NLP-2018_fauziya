with open("naivebayes.py", "r") as f:
    lines = f.readlines()
    lines = [line.replace("\t", "    ") for line in lines]
    with open("naivebayes2.py", "w") as f2:
        for line in lines:
            f2.write(line)
