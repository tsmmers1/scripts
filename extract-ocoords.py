#!/usr/bin/env python
import sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument("i", help="Orca outputfile name")
parser.add_argument("-o", default="coords.xyz", help="name of XYZ outputfile")
args = parser.parse_args()

if __name__ == '__main__':

    NAtoms = 0

    with open(args.i, 'r') as readfile:
        savefile = open(args.o, 'w')
        writecoords = 0
        step = 0
        for line in readfile:
            if "Number of atoms" in line:
                NAtoms = int(line.split()[-1])
            if writecoords == NAtoms+1:
                savefile.write("STEP "+str(step)+"\n")
                step += 1
                writecoords -= 1 
            elif writecoords != 0:
                savefile.write(line)
                writecoords -= 1
            elif "CARTESIAN COORDINATES (ANGSTROEM)" in line:
                writecoords = NAtoms+1
                savefile.write(str(NAtoms)+"\n")
        savefile.close()
            
        
