#!/usr/bin/env python
import os, sys
import argparse
from collections import defaultdict
import xlsxwriter

parser = argparse.ArgumentParser(description="Analyzes FEFF chips files in order to isolate the chi(k) components originating from certain atoms")
parser.add_argument("xyz", type=str, help="Inputfile .xyz file to refer coordinates from")
parser.add_argument("box", type=float, help="Box size of system")
parser.add_argument("-include", nargs='+', help="Indices of atoms to include. Indexing begins at 1. Indices can be space separated (e.g. 1 2 3) and given with ranges (e.g. 1-3)")
parser.add_argument("-exclude", nargs='+', help="Indices of atoms to exclude. Indexing begins at 1. Indices can be space separated (e.g. 1 2 3) and given with ranges (e.g. 1-3)")
#parser.add_argument("-feff", default="feff.inp", help="Name of feff inputfile to refer to coords from, default: feff.inp")
parser.add_argument("-path", default="paths.dat", help="Name of FEFF paths file, default: paths.dat")
parser.add_argument("-chips", default=".", help="Path location of chips files, default: current directory")
parser.add_argument("-center", type=int, default=1, help="Index of atom to be used for center, default = 1")
parser.add_argument("-o", default="chi-sel.dat", help="Name of output datafile to export averaged chi(k) selection to, default: chi-sel.dat")
parser.add_argument("-allresults", action='store_true', help="If flag is given, will output .xlsx file (with prefix name of -o flag) containing all chips chi(k) spectra compiled in given selection")
args = parser.parse_args()


def identify_indices(l):
    if l == None: return []
    separated  = []
    for i in l:
        if "-" in i:
            separated.extend(list(range(int(i.split("-")[0]),int(i.split("-")[1])+1)))
        else:
            separated.append(int(i))
    return separated

def correct_coordinates(coords, center, b):
    for i in range(len(coords)):
        coords[i] = [coords[i][0], coords[i][1]-center[1], coords[i][2]-center[2], coords[i][3]-center[3]]
        for j in [1,2,3]:
            if coords[i][j] <= -(0.5*b): coords[i][j] = round(coords[i][j] + b, 3)
            elif coords[i][j] >= (0.5*b): coords[i][j] = round(coords[i][j] - b, 3)
            else: coords[i][j] = round(coords[i][j], 3)
    return coords

def find_paths(f, inc, exc):
    path_pos = []
    pf = open(f, 'r').readlines()
    for i, line in enumerate(pf):
        if "index, nleg, degeneracy" in line:
            index = line.split()[0]
            n_scatter = int(line.split()[1])
            paths = []
            for i in range(i+2, i+2+n_scatter):
                paths.append([pf[i].split("'")[1].strip()]+[round(float(pf[i].split()[j]), 3) for j in [0,1,2]])
            keep_bool = False
            exc_bool = False
            for p in paths:
                if p in exc: exc_bool = True
                elif p in inc: keep_bool = True
            if keep_bool == True and exc_bool == False:
                path_pos.append(index)
    return path_pos

def compile_chik(i_paths, loc):
    chi = defaultdict(list)
    for i in i_paths:
        c_name = f"chip{int(i):04d}.dat"
        data = open(loc+"/"+c_name, 'r').readlines()
        header = None
        for i,j in enumerate(data):
            if "k         chi" in j:
                header = i
                break
        chi["k_values"].append(c_name)
        if float(data[header+1].split()[0]) != 0.0:
            chi[0.0].append(None)
        for i in range(header+1,len(data)):
            chi[float(data[i].split()[0])].append(float(data[i].split()[1]))
    return chi

def calc_avg_chik(chi):
    avg = defaultdict(float)
    for k in chi.keys():
        if k == 'k_values': continue
        if None in chi[k]:
            if len([i for i in chi[k] if i != None]) == 0: continue
            else:
                avg[k] = sum([i for i in chi[k] if i != None]) / len([i for i in chi[k] if i != None])
        else:
            avg[k] = sum(chi[k])/len(chi[k])
    return avg

def save_workbook(name, avg, chi):
    workbook = xlsxwriter.Workbook(name)
    worksheet = workbook.add_worksheet()
    
    #Write average results
    worksheet.write(0,0,"k")
    worksheet.write(0,1,"chi_avg")
    k = list(avg.keys())
    for row in range(0,len(k)):
        worksheet.write(row+1,0, k[row])
        worksheet.write(row+1,1, avg[k[row]])
    
    #Write individual results
    k = list(chi.keys())
    for row in range(0,len(k)):
        worksheet.write(row, 3, k[row])
        entry = chi[k[row]]
        for col in range(0, len(entry)):
            worksheet.write(row, col+4, entry[col])
    workbook.close()

def save_datafile(name, avg):
    with open(name, 'w') as savefile:
        savefile.write("k          chi\n")
        for item in avg:
            savefile.write(f"{item:<10}{chi_avg[item]}\n")

if __name__ == '__main__':

    i_include = identify_indices(args.include)
    i_exclude = identify_indices(args.exclude)

    #Extract relevant coords
    c_center = []
    c_include = []
    c_exclude = []
    with open(args.xyz, 'r') as f:
        for index, line in enumerate(f):
            if index-1 == args.center:
                c_center = [line.split()[0]]+[float(x) for x in line.split()[1:]] #Central atom
            elif index-1 in i_include:
                c_include.append([line.split()[0]]+[float(x) for x in line.split()[1:]]) #Included atoms
            elif index-1 in i_exclude:
                c_exclude.append([line.split()[0]]+[float(x) for x in line.split()[1:]]) #Excluded atoms

    #Center coords and adjust coords outside box dimensions
    c_include = correct_coordinates(c_include, c_center, args.box)
    c_exclude = correct_coordinates(c_exclude, c_center, args.box)

    #Identify indices of appropriate paths in paths datafile
    i_paths = find_paths(args.path, c_include, c_exclude)

    #Compile chi(k) from appropriate chips files
    chi = compile_chik(i_paths, args.chips)

    #Compute average chi(k) spectrum
    chi_avg = calc_avg_chik(chi)

    #Save results
    if args.allresults == True:
        save_workbook(args.o.split(".dat")[0]+".xlsx", chi_avg, chi)
    else:
        save_datafile(args.o, chi_avg)

