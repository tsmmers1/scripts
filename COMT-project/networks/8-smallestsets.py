import sys
import re

combidirs = []
with open("CompiledResults.csv","r") as datafile:
    for line in datafile:
        split = line.split(",")
        if split[7] == "1":
            combidirs.append([split[0], float(split[29]), float(split[31]), int(split[27])])

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
savefile = open("mininteract.csv","w")
interlist = ["wc:ligand_mc","wc:ligand_sc","wc:ligand_solvent","cc:ligand_mc","cc:ligand_sc","cc:ligand_solvent","so:ligand_mc","so:ligand_sc","so:ligand_solvent","hb:ligand_mc","hb:ligand_sc","hb:ligand_solvent","bo:ligand_sc","bo:ligand_solvent"]
savefile.write("name,"+",".join(interlist)+","+",".join(interlist)+"\n")
for item in combidirs:
    if "combi-qcheng" in item[0]:
        name = "qcombi_" + item[0].split("/")[-1].split("-ts")[0] + ".pdb"
        for key in keys:
            if key[0] == name:
                modname[name] = item
                for edge in edges:
                    if edge[0] == key[1]:
                        minint = []
                        maxint = []
                        for i in range(0,len(edge[1])):
                            maxint.extend(re.findall("'([^']*)'", edge[1][i]))
                            sub = False
                            sup = False
                            for j in range(0,len(edge[1])):
                                if i == j: continue
                                if set(re.findall("'([^']*)'", edge[1][i])).issubset(set(re.findall("'([^']*)'", edge[1][j])))==True: sub = True
                                if set(re.findall("'([^']*)'", edge[1][i])).issuperset(set(re.findall("'([^']*)'", edge[1][j])))==True: sup = True
                            if sub == True and sup == False:
                                minint.extend(re.findall("'([^']*)'", edge[1][i]))
                        str1 = [0]*14
                        str2 = [0]*14
                        for k in range(0,14):
                            if interlist[k] in minint:
                                str1[k] = 1
                            if interlist[k] in maxint:
                                str2[k] = 1
                        savefile.write(name+","+",".join([str(x) for x in str1])+","+",".join([str(x) for x in str2])+"\n")

    else:
        if "model34" in item[0]: name = "res_34-aa.pdb"
        else: name = "res_" + item[0].split("/")[-1].split("-ts")[0] + ".pdb"
        for key in oldkeys:
            if key[0] == name:
                modname[name] = item
                for edge in edges:
                    if edge[0] == key[1]:
                        minint = []
                        maxint = []
                        for i in range(0,len(edge[1])):
                            maxint.extend(re.findall("'([^']*)'", edge[1][i]))
                            sub = False
                            sup = False
                            for j in range(0,len(edge[1])):
                                if i == j: continue
                                if set(re.findall("'([^']*)'", edge[1][i])).issubset(set(re.findall("'([^']*)'", edge[1][j])))==True: sub = True
                                if set(re.findall("'([^']*)'", edge[1][i])).issuperset(set(re.findall("'([^']*)'", edge[1][j])))==True: sup = True
                            if sub == True and sup == False:
                                minint.extend(re.findall("'([^']*)'", edge[1][i]))
                        str1 = [0]*14
                        str2 = [0]*14
                        for k in range(0,14):
                            if interlist[k] in minint:
                                str1[k] = 1
                            if interlist[k] in maxint:
                                str2[k] = 1
                        savefile.write(name+","+",".join([str(x) for x in str1])+","+",".join([str(x) for x in str2])+"\n")

savefile.close()
#savefile = open("edgediff.csv","w")
#savefile2 = open("edgediff2.csv","w")
#savefile2.write("EdgeLength,TSdiff,RXNdiff,Edge,Natoms1,TS1,RXN1,Natoms2,TS2,RXN2\n")
#inter = list(edgesets.keys())
#allinter = set()



"""
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
"""
