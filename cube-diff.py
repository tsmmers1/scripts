#!/usr/bin/env python
import os, sys
import argparse

parser = argparse.ArgumentParser(description="Calculates the Difference in two cube files (C1 - C2)")
parser.add_argument("-c1", help="First Cube file")
parser.add_argument("-c2", help="Secod Cube file")
parser.add_argument("-o", default="Csub.cube", help="Name used for output cube file, default Csub.cube")
args = parser.parse_args()


if __name__ == '__main__':

    C1 = open(args.c1, 'r').readlines()
    C2 = open(args.c2, 'r').readlines()

    C1atoms = int(C1[2].split()[0])
    C2atoms = int(C2[2].split()[0])

    #Confirm proper origin center
    for i in range(1,4):
        if float(C1[2].split()[i]) != float(C2[2].split()[i]):
            sys.exit("Process terminated: both cube files have different position of origin of volumetric data")

    #Confirm proper grid
    for i in range(3,6):
        C1g = [float(x) for x in C1[i].split()]
        C2g = [float(x) for x in C2[i].split()]
        if C1g != C2g:
            sys.exit("Process terminated: both cube files have different grid parameters")

    with open(args.o, 'w') as savefile:
        #Write header
        for i in range(0,C1atoms+6):
            savefile.write(C1[i])

        #Write new volume data
        for i,j in zip(range(C1atoms+6,len(C1)), range(C2atoms+6,len(C2))):
            s1 = [float(x) for x in C1[i].split()]
            s2 = [float(x) for x in C2[j].split()]
            diff = [x - y for x,y in zip(s1,s2)]  #Take differences in two cubes
            diffstr = [format(x, ".5e").replace("e","E") for x in diff] #Format to certain decimal place
            diffstr = [f'{x: >12}' for x in diffstr]  #Format strings to occupy certain space
            savefile.write(" "+" ".join(diffstr)+"\n")
