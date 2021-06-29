#!/usr/bin/env python

import sys, itertools, math, argparse

parser = argparse.ArgumentParser(description='Reduces Trang-based combinatoric code into non-directional combinatoric sets')
parser.add_argument('freqfile', type=str, help='Name of the Trang file', default='edges_by_unique_sets.txt')
parser.add_argument('-p','--presort', help='[Optional] Name of file to write all presorted data', default=None)
parser.add_argument('-o','--output', help='Name of outputfile to write containing the sorted data', default='SortedResults.dat')
parser.add_argument('-a','--artificial', help='[Optional] Comma-separated space-less string of numbers you wish to artificially add to all models', default=None)
args = parser.parse_args()

#Identify all interactions
interaction = []
with open(args.freqfile) as readfile:
    for line in readfile:
        splitline = line.split("\'")
        for item in splitline:
            if (":" in item) and (item not in interaction):
                interaction.append(item)

#Isolate individual interactions and the residues corresponding to them
interdic = dict()
with open(args.freqfile) as readfile:
    for line in readfile:
        for item in interaction:
            string = "('" + item + "',)"
            if string in line:
                #Generate a Dictionary of "interaction":[res1,res2,res3...]
                res = [int(x) for x in line.split(")")[0].split("(")[1].split(",")]
                n1 = item.split(":")[0]
                n2 = sorted(item.split(":")[1].split("_"))
                name = n1 + ":" + n2[0] + "_" + n2[1]
                checkremove = ['cnt:ligand_ligand', 'hbond:ligand_ligand', 'ovl:ligand_ligand']
                if (name in interdic.keys()) and (name not in checkremove):
                    interdic[name].extend(res)
                elif (name not in interdic.keys()) and (name not in checkremove):
                    interdic[name] = res

#Remove duplicate residues in dictionary
for item in interdic.keys():
    interdic[item] = sorted(list(set(interdic[item])))

#Compute all combinations of interactions
interlist = []
for i in range(1,len(interdic.keys())+1):
    interlist.extend(list(combi) for combi in itertools.combinations(interdic.keys(), i))

#Translate all combinations of interactions to residue lists
def predres(mylist):
    newlist = []
    for item in mylist:
        newlist.extend(interdic[item])
    newlist = list(set(newlist))
    newlist.sort()
    return newlist

reslist = list(map(predres, interlist))

#Reduce the list by duplicates
shortlist = []
shortlistres = []
shorterlist = []
shorterlistres = []

for i in range(0, len(reslist)):
    if reslist[i] in shortlistres:
        shortlist[shortlistres.index(reslist[i])].append(tuple(interlist[i]))
    else:
        shortlistres.append(reslist[i])
        shortlist.append([tuple(interlist[i])])

    if args.artificial != None:
        artires = [int(x) for x in args.artificial.split(",")]
        artilistres = list(set(reslist[i]) | set(artires))
        artilistres.sort()
        if artilistres in shorterlistres:
            shorterlist[shorterlistres.index(artilistres)].append(tuple(interlist[i]))
        else:
            shorterlistres.append(artilistres)
            shorterlist.append([tuple(interlist[i])])

print("Total undirected interactoins: ", len(interdic.keys()))
print("Total combinatoric structures: ", len(reslist))
print("Total unique combinatoric structures: ", len(shortlist))
if args.artificial != None:
    print("Total unique combinatoric structures after residues artificially added: ", len(shorterlist))

#Write data files
if args.presort != None:
    with open(args.presort, "w") as savefile:
        for i in range(0,len(reslist)):
            savefile.write(str(reslist[i]) + "\t" + str(interlist[i]) + "\n")

with open(args.output, "w") as savefile:
    for i in range(0,len(shortlist)):
        savefile.write(str(shortlistres[i]) + "\t" + str(shortlist[i]) + "\n")

if args.artificial != None:
    with open("ArtificialResults.dat", "w") as savefile:
        for i in range(0,len(shorterlist)):
            savefile.write(str(shorterlistres[i]) + "\t" + str(shorterlist[i]) + "\n")


