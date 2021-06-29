#!/usr/bin/python
import os, sys
from collections import defaultdict

if __name__ == '__main__':

    data = []
    energies = []
    datanames = []
    natoms = []
    with open("CompiledResults.csv","r") as readfile:
        for line in readfile:
            split = line.split(",")
            if split[1][0:6] == "ByHand": continue
            data.append([split[k].strip() for k in range(44,84)])
            energies.append([split[k].strip() for k in range(21,25)])
            datanames.append(split[1])
            natoms.append(split[20])

    for i in range(1,len(data)):
        for j in range(0,len(data[i])):
            if data[i][j] != "0":
                data[i][j] = 1
            else: data[i][j] = 0

    for i in range(1, len(energies)):
        for j in range(0, len(energies[i])):
            energies[i][j] = float(energies[i][j])

    savefile = open("wholeres.csv","w")
    savefile.write("x1,y1,x2,y2\n")

    counter = defaultdict(int)
    for i in range(1,len(data)):
        for j in range(i+1,len(data)):
            diff = 0
            for k in range(0,len(data[i])):
                if data[i][k] != data[j][k]:
                    diff +=1
            if diff==1:
                for k in range(0, len(data[i])):
                    if data[i][k] != data[j][k]:
                        counter[data[0][k]] +=1
                savefile.write(",".join(map(str,[natoms[i], energies[i][1], natoms[j], energies[j][1]])) + "\n")

    savefile.close()

    for item in counter:
        print(item, counter[item])
