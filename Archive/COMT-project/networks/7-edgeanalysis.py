import sys
import re

edges = []
with open("ArtificialResults.dat","r") as edgefile:
    for line in edgefile:
        edges.append([[int(x) for x in line.split("[")[1].split("]")[0].split(",")], re.findall('\(([^)]+)', line.split(":",1)[1])])

optmods = []
with open("optimizedmodels.txt","r") as modfile:
    for line in modfile:
        optmods.append([line.split(":")[0], [int(x) for x in line.split("[")[1].split("]")[0].split(",")]])

for data in edges:
    for model in optmods:
        if data[0] == model[1]:
            total = len(data[1])
            smallest = len(data[1][0].split(","))
            sset = []
            largest = len(data[1][0].split(","))
            for elem in data[1]:
                elemA = elem.split(",")
                if len(elemA) < smallest: smallest = len(elemA)
                if len(elemA) > largest: largest = len(elemA)
            for i in range(0,len(data[1])):
                sub = False
                sup = False
                for j in range(0,len(data[1])):
                    if i == j: continue
                    if set(re.findall("'([^']*)'", data[1][i])).issubset(set(re.findall("'([^']*)'", data[1][j])))==True: sub = True
                    if set(re.findall("'([^']*)'", data[1][i])).issuperset(set(re.findall("'([^']*)'", data[1][j])))==True: sup = True
                if sub == True and sup == False:
                    print(re.findall("'([^']*)'", data[1][i]))

            print(model[0], model[1], total, smallest, largest)
sys.exit()

allinter = set()
for i in range(0,len(inter)):
    for j in range(i+1,len(inter)):
        allinter = allinter | set(re.findall("'([^']*)'", inter[i]))
        if len(set(re.findall("'([^']*)'", inter[i]))^set(re.findall("'([^']*)'", inter[j])))==1:
            intdiff = list(set(re.findall("'([^']*)'", inter[i]))^set(re.findall("'([^']*)'", inter[j])))[0]
            if len(re.findall("'([^']*)'", inter[i])) < len(re.findall("'([^']*)'", inter[j])):
                TSdiff = modname[edgesets[inter[j]]][1] - modname[edgesets[inter[i]]][1]
                RXNdiff = modname[edgesets[inter[j]]][2] - modname[edgesets[inter[i]]][2]
                length = len(re.findall("'([^']*)'", inter[i]))
            else:
                TSdiff = modname[edgesets[inter[i]]][1] - modname[edgesets[inter[j]]][1]
                RXNdiff = modname[edgesets[inter[i]]][2] - modname[edgesets[inter[j]]][2]
                length = len(re.findall("'([^']*)'", inter[j]))
            natoms1 = modname[edgesets[inter[i]]][3]
            TSenergy1 = modname[edgesets[inter[i]]][1]
            RXNenergy1 = modname[edgesets[inter[i]]][2]
            natoms2 = modname[edgesets[inter[j]]][3]
            TSenergy2 = modname[edgesets[inter[j]]][1]
            RXNenergy2 = modname[edgesets[inter[j]]][2]
            savefile.write(intdiff + "," + str(TSdiff) + "," + str(RXNdiff) + "\n")
            savefile2format = [str(length), str(TSdiff), str(RXNdiff), intdiff, str(natoms1), str(TSenergy1), str(RXNenergy1), str(natoms2), str(TSenergy2), str(RXNenergy2)]
            savefile2.write(",".join(savefile2format) + "\n")
savefile.close()
savefile2.close()

allinter = list(allinter)
allinter.sort()
edgescomp = {}
for entry in inter:
    if edgesets[entry] not in edgescomp:
        fg = [0] * len(allinter)
        for i in range(0, len(fg)):
            if allinter[i] in re.findall("'([^']*)'", entry): fg[i]+=1
        fg.extend([modname[edgesets[entry]][1], modname[edgesets[entry]][2]])
        edgescomp[edgesets[entry]] = fg
    else:
        for i in range(0, len(allinter)):
            if allinter[i] in re.findall("'([^']*)'", entry): edgescomp[edgesets[entry]][i] +=1

savefile3 = open("edgescomp.csv","w")
savefile3.write("Model," + ",".join(allinter) + ",TS,RXN\n")
for item in edgescomp:
    savefile3.write(item + "," + ",".join(map(str, edgescomp[item])) + "\n")
savefile3.close()


