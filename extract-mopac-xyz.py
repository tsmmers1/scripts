#!/usr/bin/env python
import sys, argparse

parser = argparse.ArgumentParser(description="Extracts XYZ coords from mopac-generated output file")
parser.add_argument("f", help="Inputfile mopac .out file")
parser.add_argument("-o", default="model.xyz", help="Name of output .xyz file (default: model.xyz)")
args = parser.parse_args()

if __name__ == '__main__':

    coords = []

    with open(args.f, 'r') as outputfile:
        begin_writing = False
        skip_line = 0
        for line in outputfile:
            if line == "                             CARTESIAN COORDINATES\n":
                begin_writing = True
                skip_line = 1
            elif begin_writing == True and skip_line == 1:
                skip_line -= 1
            elif begin_writing == True and skip_line == 0:
                if line == "\n":
                    break
                else:
                    coords.append(line.split(None,1)[1])
    
    with open(args.o, 'w') as savefile:
        savefile.write(f"{len(coords)}\n{args.f}\n")
        for atom in coords:
            savefile.write(atom)

