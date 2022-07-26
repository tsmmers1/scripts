#!/usr/bin/env python
import os, sys
import argparse

parser = argparse.ArgumentParser(description="Calculates the Difference in two or more cube files (C1 - C2)")
parser.add_argument("-c1", help="First Cube file")
parser.add_argument("-c2", nargs = '+', help="Second Cube file(s). Multiple files are indicated by space separation")
parser.add_argument("-o", default="Csub.cube", help="Name used for output cube file, default Csub.cube")
args = parser.parse_args()


if __name__ == '__main__':

    C1 = open(args.c1, 'r').readlines()
    C1atoms = int(C1[2].split()[0])

    #Store initial volume data
    Cdiff = [] 
    for i in range(C1atoms+6, len(C1)):
        Cdiff.append([float(x) for x in C1[i].split()])

    for cfile in args.c2:
        C2 = open(cfile, 'r').readlines()
        C2atoms = int(C2[2].split()[0])

        #Confirm proper origin center
        for i in range(1,4):
            if float(C1[2].split()[i]) != float(C2[2].split()[i]):
                sys.exit("Process terminated: cube files have different position of origin of volumetric data")

        #Confirm proper grid
        for i in range(3,6):
            C1g = [float(x) for x in C1[i].split()]
            C2g = [float(x) for x in C2[i].split()]
            if C1g != C2g:
                sys.exit("Process terminated: cube files have different grid parameters")

        #Take difference in volume data
        for i,j in zip(range(0,len(Cdiff)), range(C2atoms+6, len(C2))):
            v2 = [float(x) for x in C2[j].split()]
            Cdiff[i] = [x - y for x,y in zip(Cdiff[i], v2)]

    #Save the difference
    with open(args.o, 'w') as savefile:
        #Write header
        for i in range(0,C1atoms+6):
            savefile.write(C1[i])

        #Write new volume data
        for i in Cdiff:
            diffstr = [format(x, ".5e").replace("e","E") for x in i] #Format to certain decimal place
            diffstr = [f'{x: >12}' for x in diffstr]  #Format strings to occupy certain space
            savefile.write(" "+" ".join(diffstr)+"\n")

