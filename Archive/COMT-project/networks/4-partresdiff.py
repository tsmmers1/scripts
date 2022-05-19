#!/usr/bin/python
import os, sys
from collections import defaultdict
import re

if __name__ == '__main__':

    data = []
    energies = []
    datanames = []
    natoms = []
    with open("CompiledResults.csv","r") as readfile:
        for line in readfile:
            split = line.split(",")
            if split[1][0:6] == "ByHand": continue
            data.append([split[k].strip() for k in range(44,87)])
            energies.append([split[k].strip() for k in range(21,25)])
            datanames.append(split[1])
            natoms.append(split[20])

    for i in range(1, len(energies)):
        for j in range(0, len(energies[i])):
            energies[i][j] = float(energies[i][j])

    dataexp = []
    for model in data[1:]:
        expanded = []
        for i in range(0,len(model)):
            if model[i]=="0":
                continue
            else:
                temp = [char + data[0][i] for char in model[i]]
                expanded.extend(temp)
        expanded2 = []
        for item in expanded:
            if item[0] == "C":
                if ("N" + str(int(item[1:])+1)) in expanded:
                    expanded2.extend(["MC"+item[1:]])
                    expanded.remove("N" + str(int(item[1:])+1))
                else:
                    print(item)
                    sys.exit()
            else: expanded2.extend([item])
                
        dataexp.append(set(expanded2))
    natoms = natoms[1:]
    energies = energies[1:]
    datanames = datanames[1:]
    counter = defaultdict(int)
    savefileTS = open("partres.csv","w")
    savefileRXN = open("partres2.csv","w")
    savefileSIF = open("diff.sif", "w")

    for i in range(0,len(dataexp)):
        for j in range(i+1,len(dataexp)):
            if abs(len(dataexp[i]^dataexp[j])) == 1:
                for elem in (dataexp[i]^dataexp[j]):
                    counter[elem]+=1
                    savefileSIF.write(datanames[i] + "\t" + natoms[i] + "\t" + str(energies[i][1]) + "\t" + str(energies[i][3]) + "\t" + list(dataexp[i]^dataexp[j])[0] + "\t" + datanames[j] + "\t" + natoms[j] + "\t" + str(energies[j][1]) + "\t" + str(energies[j][3]) + "\n")
                    if len(dataexp[i]) > len(dataexp[j]):
                        savefileTS.write(elem + "," + str(energies[i][1]-energies[j][1]) + "\n")
                        savefileRNX.write(elem + "," + str(energies[i][3]-energies[j][3]) + "\n")
                    else: 
                        savefileTS.write(elem + "," + str(energies[j][1]-energies[i][1]) + "\n")
                        savefileRXN.write(elem + "," + str(energies[j][3]-energies[i][3]) + "\n")
            elif abs(len(dataexp[i]^dataexp[j])) == 2:
                options = list(dataexp[i]^dataexp[j])
                test1 = int("".join(filter(str.isdigit, options[0])))
                test2 = int("".join(filter(str.isdigit, options[1])))
                if abs(test1-test2) <= 1:
                    newname = "MCR" + str(max([test1, test2]))
                    counter[newname]+=1
                    savefileSIF.write(datanames[i] + "\t" + natoms[i] + "\t" + str(energies[i][1]) + "\t" + str(energies[i][3]) + "\t" + newname + "\t" + datanames[j] + "\t" + natoms[j] + "\t" + str(energies[j][1]) + "\t" + str(energies[j][3]) + "\n")
                    if len(dataexp[i]) > len(dataexp[j]):
                        savefileTS.write(newname + "," + str(energies[i][1]-energies[j][1]) + "\n")
                        savefileRNX.write(newname + "," + str(energies[i][3]-energies[j][3]) + "\n")
                    else:
                        savefileTS.write(newname + "," + str(energies[j][1]-energies[i][1]) + "\n")
                        savefileRXN.write(newname + "," + str(energies[j][3]-energies[i][3]) + "\n")
            elif abs(len(dataexp[i]^dataexp[j])) == 3:
                options = list(dataexp[i]^dataexp[j])
                test1 = int("".join(filter(str.isdigit, options[0])))
                test2 = int("".join(filter(str.isdigit, options[1])))
                test3 = int("".join(filter(str.isdigit, options[2])))
                if (abs(test1-test2)+abs(test2-test3)) in [1,2]:
                    letters = ["".join(l for l in options[0] if l.isalpha()), "".join(l for l in options[1] if l.isalpha()), "".join(l for l in options[2] if l.isalpha())]
                    if letters.count("MC") ==2:
                        newname = "MCRMC" + str(max([test1,test2,test3]))
                        counter[newname] +=1
                        savefileSIF.write(datanames[i] + "\t" + natoms[i] + "\t" + str(energies[i][1]) + "\t" + str(energies[i][3]) + "\t" + newname + "\t" + datanames[j] + "\t" + natoms[j] + "\t" + str(energies[j][1]) + "\t" + str(energies[j][3]) +"\n")
                        if len(dataexp[i]) > len(dataexp[j]):
                            savefileTS.write(newname + "," + str(energies[i][1]-energies[j][1]) + "\n")
                            savefileRNX.write(newname + "," + str(energies[i][3]-energies[j][3]) + "\n")
                        else:
                            savefileTS.write(newname + "," + str(energies[j][1]-energies[i][1]) + "\n")
                            savefileRXN.write(newname + "," + str(energies[j][3]-energies[i][3]) + "\n")
    for item in counter.keys():
        print(item, counter[item])
    savefileTS.close()
    savefileRXN.close()
    savefileSIF.close()
