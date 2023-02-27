#!/usr/bin/env python
import argparse

parser = argparse.ArgumentParser(description="Transforms PDB file to XYZ file where atom names are consistent instead of defaulting to element symbol")
parser.add_argument("f", help="Inputfile .pdb file")
parser.add_argument("-o", type=str, help="(Optional) Name of new outputfile XYZ, default is to use original .pdb name")
args = parser.parse_args()

if __name__ == '__main__':

    #Initialize savefile
    if args.o == None:
        savename = args.f.rsplit(".pdb",1)[0]+".xyz"
    else:
        savename = args.o

    coords = []

    #Extract atoms
    with open(args.f, 'r') as readfile:
        for line in readfile:
            if line[0:6] == "ATOM  " or line[0:6] == "HETATM":
                coords.append(line[13:16]+"     "+line[31:54]+"\n")

    #Write savefile
    with open(savename, 'w') as savefile:
        savefile.write(str(len(coords))+"\n\n")
        for entry in coords:
            savefile.write(entry)


