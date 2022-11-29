#!/usr/bin/env python
import os, sys
import argparse
import numpy as np
from collections import defaultdict


parser = argparse.ArgumentParser(description="Compiles information on FEFF XAFS data from xmu.dat files and generates averaged spectra")
parser.add_argument("-f", help="Input text file containing list of xmu.dat files to be compiled")
parser.add_argument("-o", default="compiled_xmu.dat", help="Optional name used for output .xmu file, default compiled_xmu.xlsx")
args = parser.parse_args()


if __name__ == '__main__':

    #Grab xmu file names
    xmufiles = [x.strip() for x in open(args.f,'r').readlines()]
    
    #Store each xmu.dat info for each xmu value into list
    xmu = defaultdict(list)

    for xmufile in xmufiles:
        data = open(xmufile, 'r').readlines()
        header = None
        
        for i,j in enumerate(data):
            if j.startswith("#  omega"):
                header = i
                break
        
        for i in range(header+1,len(data)):
            s = data[i].split()
            xmu[float(s[2])].append([float(s[0]), float(s[1]) , float(s[3]), float(s[4]), float(s[5])])
    
    #Average data for each k
    kOrder = list(xmu.keys())
    kOrder.sort()
    
    with open(args.o, 'w') as savefile:
        savefile.write("#  omega    e    k    mu    mu0     chi     @#\n")

        for k in kOrder:
            avg = np.mean(xmu[k], axis=0)
            omega = f'{avg[0]:.3f}'.rjust(12)
            e = f'{avg[1]:.3f}'.rjust(11)
            k = f'{k:.3f}'.rjust(8)
            mu = f'{avg[2]:.5E}'.rjust(13)
            mu0 = f'{avg[3]:.5E}'.rjust(13)
            chi = f'{avg[4]:.5E}'.rjust(13)
            savefile.write(omega+e+k+mu+mu0+chi+"\n")

