#!/usr/bin/env python

import os, sys, argparse

#Argparse Setup
parser = argparse.ArgumentParser(description='Analyzes the Combinatoric Residues list against Frequency_Per_Residue file Information and generates a .csv of collated results')
parser.add_argument('-f', dest='freq', type=str, help='Name of the RINRUS-generated Interaction/Frequency File', default='freq_per_res.dat')
parser.add_argument('-c', dest='combi', type=str, help='Name of the combinatoric Interaction/Residue list file', default='fileskey.txt')
parser.add_argument('-s', dest='savefile', type=str, help='Name of the file you wish to save. Default is CumulativeInteractions.csv', default='CumulativeInteractions.csv')
args = parser.parse_args()

#Check existence of desired file(s)
if os.path.exists(args.freq)==False:
    print "File not found: " + args.freq
    sys.exit()
elif os.path.exists(args.combi)==False:
    print "File not found: " + args.combi
    sys.exit()

#Extract Residue and Interaction info from FreqFile
resinter = []
allinters = []
with open(args.freq) as ff:
    for line in ff:
        res = int(line.split()[1])
        inter = [line.split()[x] for x in range(3,len(line.split()))]
        for j, k in enumerate(inter):
            p1 = k[0:3]
            p2 = sorted([k.split(":")[1].split("_")[0], k.split("_")[1]])
            inter[j] = p1 + p2[0] + "_" + p2[1]
        allinters = sorted(list(set(allinters) | set(inter)))
        resinter.append([res, inter])

#Extract Residue List and Name info from Combifile
combires = []
with open(args.combi) as ff:
    for line in ff:
        name = line.split()[0]
        res = line.split("[")[1].split("]")[0]
        res = [int(x) for x in res.split(",")]
        for item in res:
            if item not in [k[0] for k in resinter]:
                print("Error: residue not found in freq-file: " + str(item))
                sys.exit()
        combires.append([name, res])

#Identify interaction information for each set of residues
def resindex(l, elem):
    for row, i in enumerate(l):
        if i[0] == elem:
            return row
    print "Unable to find element: " + str(elem)
    sys.exit()

compdata = []
for item in combires:
    name = item[0]
    reslist = item[1]
    interlist = [0] * len(allinters)
    for residue in reslist:
        for inter in resinter[resindex(resinter,residue)][1]:
            interlist[allinters.index(inter)] +=1
    interlist.append(sum(interlist))
    interlist.insert(0,name)
    compdata.append(interlist)

#Save compiled data to a .csv
with open(args.savefile,"w") as ss:
    ss.write("Name," + ",".join(map(str,allinters)) + ",Total\n")
    for line in compdata:
        ss.write(",".join(map(str,line)) + "\n")














