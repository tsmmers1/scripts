#!/usr/bin/env python
import sys, argparse, xlsxwriter
from collections import defaultdict

parser = argparse.ArgumentParser(description="Analyzes a .gro MD file, primarily of a pull simulation. Measures proportions of molecules around a given molecule \
        in the Z direction to identify the location of a user-specified atom/molecule with respect to a given interface ")
parser.add_argument("f", help="Inputfile MD .gro file")
parser.add_argument("index", nargs='+', help="Reference atom index/indices for distance measurement (from .gro file).")
parser.add_argument("-solvent", nargs='+', default=['WAT','HEX','OCT'], help="3-character resname of solvent molecules to count, default is WAT HEX OCT") 
parser.add_argument("-dist", default=0.3, type=float, help="Distance (in nm) within to count all solvent atoms, default is 0.3")
parser.add_argument("-maxdist", default=3.0, type=float, help="Distance (in nm) that if an any solvent-index is greater than, then the solvent atom distances \
        are skipped to accelerate computation time, default is 3.0")
parser.add_argument("-o", default="solv_count_dist.xlsx", help="Name used for output .xlsx file, default: solv_count_dist.xlsx")
args = parser.parse_args()


if __name__ == '__main__':

    NAtoms, newline = 0, 1
    mol, ref = defaultdict(list), list()
    solv_count = defaultdict(list)

    index = []
    for item in args.index:
        if "-" in item:
            index.extend(range(int(item.split("-")[0]), int(item.split("-")[1])+1))
        else:
            index.append(int(item))
    
    with open(args.f, 'r') as readfile:
        for i, line in enumerate(readfile):
            if i == newline: #At beginning of .gro: grab NAtoms and predict end point
                NAtoms = int(line)
                newline += 3+NAtoms
            
            elif i == newline-1: #At title line of .gro
                continue
            
            elif i == newline-2: #At end of .gro: process results
                
                for s in args.solvent: 
                    solv_count[s].append(0)

                for m in mol:
                    b = False
                    for mi in mol[m]:
                        if b == True: continue
                        for r in ref:
                            d = ( (r[0]-mi[0])**2 + (r[1]-mi[1])**2 + (r[2]-mi[2])**2 )**0.5
                            if d <= args.dist:
                                solv_count[m[-3:]][-1] +=1
                                b = True
                                break
                            elif d >= args.maxdist:
                                b = True
                                break
                        
                    #if any([abs(x-refZ) < args.width for x in mol[m]]):
                        
                    #    solv_count[m[-3:]][-1] +=1
                mol, ref = defaultdict(list), list()
            
            else: #In middle of .gro
                if int(line[15:20]) in index:
                    ref.append([float(line[20:28]), float(line[28:36]), float(line[36:44])])
                elif line[5:8] in args.solvent:
                    mol[line[0:8].strip()].append([float(line[20:28]), float(line[28:36]), float(line[36:44])])

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

    



