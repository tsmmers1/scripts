#!/usr/bin/env python

import os, sys, re

#This script combines the results of the model names, model residue composition, and model interaction lists for analysis

#Extract fileskey information (model names and model residue composition)
keyfile = open("fileskey.txt", "r")
keydata = []

for line in keyfile:
    modelname = line.split(".pdb")[0].split("res_")[1]
    reslist = [int(x) for x in line.split("[")[1].split("]")[0].split(",")]
    reslist.sort()
    keydata.append([modelname,reslist])

keyfile.close()

#Extract edges_by_unique_sets.txt information (model residue composition and corresponding edges)
edgefile = open("edges_by_unique_sets.txt", "r")
edgedata = []

for line in edgefile:
    reslist = [int(x) for x in line.split("|")[0].split("(")[1].split(")")[0].split(",")]
    reslist.sort()
    edgestring = line.split("[")[1].split("]")[0]
    edgestring = re.split('\(|\)', edgestring)
    edgestring = [x.replace('\'','').split(", ") for x in edgestring if ":" in x]
    edgedata.append([reslist, edgestring])

edgefile.close()

#Merge data from keydata and edgedata based on identical reslist information
#Data Format:
#  [0]"Natural",    [1]ModelName,   [2]ResidueList,       [3]Interactions
#  [0]"Absent" ,    [1]ResidueList, [2]Interactions
#  [0]"Artificial", [1]ModelName,   [2]NaturalResidueList [3]ArtificialResidueList [4]Interactions
mergedata = []
for line in edgedata:
    isnatural = False
    for item in keydata:
        if line[0]==item[1]:
            mergedata.append(["natural",item[0],item[1],line[1]])
            isnatural = True
            continue
    if isnatural == False:
        newline = list(set(line[0])|set([300,301,302,141,169,170,411]))
        newline.sort()
        if newline == line[0]:
            mergedata.append(["absent",line[0],line[1]])
            continue
        isartificialpresent = False
        for item in keydata:
            if newline==item[1]:
                mergedata.append(["artificial",item[0],line[0],newline,line[1]])
                isartificialpresent = True
                continue
        if isartificialpresent == False:
            mergedata.append(["absent",line[0],line[1]])

#Set up a system that is able to count interaction-type frequency among one or more files
filenames = sys.argv[1]
filenames = filenames.split(",")

for name in filenames:
    for item in mergedata:
        if item[1]==name:
            for subitem in item[4]:
                print subitem
