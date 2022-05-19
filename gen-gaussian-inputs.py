#!/usr/bin/env python
import sys, argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description="Generate a series of Gaussian inputfiles containing structures from specified intervals of MD .xyz sim")
parser.add_argument("-f", help="Inputfile .xyz file of MD sim")
parser.add_argument("-s", default=1, type=int, help="Integer specifying frames to optionally skip (default: 1, no-skipping)")
parser.add_argument("-o", default="geom", help="Generic name used output name-#.inp files")
args = parser.parse_args()

def write_header(s):
    s.write("%nprocshared=32\n")
    s.write("%mem=112GB\n")
    s.write("#P b3lyp/6-311++G(d,p) freq scrf(cpcm,solvent=carbontetrachloride)\n\n")
    s.write("TPY-NO2\n\n")
    s.write("0 1\n")

def write_footer(s):
    s.write("\n")

if __name__ == '__main__':

    frame = 0
    newframe = 0
    NAtoms = 0
    newline = 0
    with open(args.f, 'r') as readfile:
        for i, line in enumerate(readfile):
            if i==newline:
                NAtoms = int(line)
                newline += 2+NAtoms
                if frame==newframe:
                    savefile = open(args.o+"-"+str(frame)+".inp", "w")
                    write_header(savefile)
            elif i in range(newline-NAtoms, newline-1) and frame==newframe:
                savefile.write(line)
            elif i==newline-1:
                if frame==newframe:
                    savefile.write(line)
                    write_footer(savefile)
                    savefile.close()
                    newframe += args.s
                frame +=1





