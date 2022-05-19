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
        for i in range(C1atoms+7,C1atoms+8):



        
        

