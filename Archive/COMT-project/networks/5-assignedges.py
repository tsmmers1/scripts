import sys
import re

combidirs = []
with open("CompiledResults.csv","r") as datafile:
    for line in datafile:
        split = line.split(",")
        if split[7] == "1":
            combidirs.append([split[0], float(split[29]), float(split[31])])

keys = []
with open("fileskey.txt", "r") as keyfile:
    for line in keyfile:
        keys.append([line.split()[0], [int(x) for x in line.split("[")[1].split("]")[0].split(",")]])

edges = []
with open("ArtificialResults.dat","r") as edgefile:
    for line in edgefile:
        edges.append([[int(x) for x in line.split("[")[1].split("]")[0].split(",")], re.findall('\(([^)]+)', line.split(":",1)[1])])

oldkeys = []
with open("oldcombi-fileskey.txt", "r") as oldfile:
    for line in oldfile:
        oldkeys.append([line.split()[0], [int(x) for x in line.split("[")[1].split("]")[0].split(",")]])

edgesets = {}
modname = {}
for item in combidirs:
    if "combi-qcheng" in item[0]:
        name = "qcombi_" + item[0].split("/")[-1].split("-ts")[0] + ".pdb"
        for key in keys:
            if key[0] == name:
                modname[name] = item
                for edge in edges:
                    if edge[0] == key[1]:
                        for inter in edge[1]:
                            edgesets[inter] = key[0]
    else:
        if "model34" in item: name = "res_34-aa.pdb"
        else: name = "res_" + item[0].split("/")[-1].split("-ts")[0] + ".pdb"
        for key in oldkeys:
            if key[0] == name:
                modname[name] = item
                for edge in edges:
                    if edge[0] == key[1]:
                        for inter in edge[1]:
                            edgesets[inter] = key[0]

savefile = open("edgediff.csv","w")
savefile2 = open("edgediff2.csv","w")
savefile2.write("EdgeLength,TSdiff,RXNdiff,Edge\n")
inter = list(edgesets.keys())
for i in range(0,len(inter)):
    for j in range(i+1,len(inter)):
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
            savefile.write(intdiff + "," + str(TSdiff) + "," + str(RXNdiff) + "\n")
            savefile2.write(str(length) + "," + str(TSdiff) + "," + str(RXNdiff) + "," + intdiff + "\n")
savefile.close()
savefile2.close()
