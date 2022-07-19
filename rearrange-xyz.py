#!/usr/bin/env python
import sys, argparse

parser = argparse.ArgumentParser(description="Rearranges the atom ordering of an XYZ file to a user-specified ordering")
parser.add_argument("-f", help="Inputfile .xyz file")
parser.add_argument("-order", default=1, help="New atom ordering. Index begins at 1. Atom ordering separated by commas [e.g. 2,5,10...] and sequential atoms can be indicated by a dash separating first and last atoms [e.g. 2,5,10,12-15,17-21]")
parser.add_argument("-o", default="reordered", help="Prefix name of new outputfile XYZ. Default: reordered")
args = parser.parse_args()

if __name__ == '__main__':

    #Obtain atom order
    order = []
    for item in args.order.split(","):
        if "-" in item:
            order.extend(range(int(item.split("-")[0]), int(item.split("-")[1])+1))
        else:
            order.append(int(item))

    #Write re-arranged file
    with open(args.o+".xyz", 'w') as savefile:
        origxyz = open(args.f, 'r').readlines()
        savefile.write(origxyz[0])
        savefile.write(origxyz[1])

        for index in order:
            savefile.write(origxyz[index+1])





