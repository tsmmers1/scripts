#!/usr/bin/env python
import sys, argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description="Generates a .csv file measuring the RMSF of user-specified indices distances over XYZ files")
parser.add_argument("-f", help="Inputfile .xyz file of MD sim")
parser.add_argument("-i", nargs="+", help="Pair(s) of atom indices separated by commas e.g. 1,2 1,3 1,4 2,5")
parser.add_argument("-o", default="RMSF.csv", help="Name of output .csv file")
args = parser.parse_args()

def dist(x1,y1,z1,x2,y2,z2):
    d = ( (x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)**0.5
    return str(round(d,3))

if __name__ == '__main__':

    pairs = [[int(x.split(',')[0]), int(x.split(',')[1])] for x in args.i]
    atoms = set([i for pair in pairs for i in pair])

    frame = 0
    NAtoms = 0
    newline = 0
    with open(args.o, 'w') as savefile:
        savefile.write("Frame,"+",".join(["d"+str(i[0])+"-"+str(i[1]) for i in pairs])+"\n")
        with open(args.f, 'r') as readfile:
            coords = defaultdict(list)
            for i, line in enumerate(readfile):
                if i==newline:
                    NAtoms = int(line)
                    newline += 2+NAtoms
                elif i in range(newline-NAtoms, newline-1) and (i-1-(frame*(NAtoms+2))) in atoms:
                    coords[i-1-(frame*(NAtoms+2))] = [float(line.split()[1]), float(line.split()[2]), float(line.split()[3])]
                elif i==newline-1:
                    results = [str(frame)]
                    for p in pairs:
                        results.append(dist(coords[p[0]][0], coords[p[0]][1], coords[p[0]][2],
                            coords[p[1]][0], coords[p[1]][1], coords[p[1]][2]))
                    savefile.write(",".join(results)+"\n")
                    frame +=1


