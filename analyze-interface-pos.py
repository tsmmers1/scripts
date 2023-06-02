#!/usr/bin/env python
import sys, argparse, xlsxwriter
from collections import defaultdict

parser = argparse.ArgumentParser(description="Analyzes a .gro MD file, primarily of a pull simulation. Measures proportions of molecules around a given molecule \
        in the Z direction to identify the location of a user-specified atom/molecule with respect to a given interface ")
parser.add_argument("f", help="Inputfile MD .gro file")
parser.add_argument("index", nargs='+', type=int, help="Reference atom index for Z value measurement (from .gro file). If more than one value is provided (e.g. 3 4 5 6), the geometric center of the atoms will be computed \
        for the atoms and used as the point of Z reference")
parser.add_argument("-solvent", nargs='+', default=['WAT','HEX','OCT'], help="3-character resname of solvent molecules to count, default is WAT HEX OCT") 
parser.add_argument("-width", default=0.01, type=float, help="Width (in nm) to permit counting molecules within reference Z direction. Default is 0.01 (i.e. +/- 0.01 nm in +/- Z direction from ref index Z position)") 
parser.add_argument("-o", default="solv_count.xlsx", help="Name used for output .xlsx file, default: solv_count.xlsx")
args = parser.parse_args()


if __name__ == '__main__':

    NAtoms, newline = 0, 1
    mol, ref = defaultdict(list), list()
    solv_count = defaultdict(list)

    with open(args.f, 'r') as readfile:
        for i, line in enumerate(readfile):
            if i == newline: #At beginning of .gro: grab NAtoms and predict end point
                NAtoms = int(line)
                newline += 3+NAtoms
            
            elif i == newline-1: #At title line of .gro
                continue
            
            elif i == newline-2: #At end of .gro: process results
                
                refZ = sum(ref)/len(ref) 

                for s in args.solvent: 
                    solv_count[s].append(0)

                for m in mol:
                    if any([abs(x-refZ) < args.width for x in mol[m]]):
                        solv_count[m[-3:]][-1] +=1

                mol, ref = defaultdict(list), list()
            
            else: #In middle of .gro
                if int(line[15:20]) in args.index:
                    ref.append(float(line[36:44]))
                elif line[5:8] in args.solvent:
                    mol[line[0:8].strip()].append(float(line[36:44]))

    #Save data to worksheet
    workbook = xlsxwriter.Workbook(args.o)
    worksheet = workbook.add_worksheet("SolvCount")

    col = 0
    for s in solv_count:
        if any(solv_count[s]):
            worksheet.write(0,col,s)
            worksheet.write_column(1,col,solv_count[s])
            col +=1
    workbook.close()

    



