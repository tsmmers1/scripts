with open("GAUresultsExtra4.csv","r") as readfile:
    for line in readfile:
        if "Path" in line.split(",")[0]: continue
        inp = open(line.split(",")[0]+"/1.inp", "r").readlines()
        charge = inp[7].split()[0]
        print(line.split(",")[0], charge)
