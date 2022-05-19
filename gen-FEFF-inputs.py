#!/usr/bin/env python
import os, sys
import argparse
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser(description="Generate a series of directories containing FEFF inputfiles of coordinates from specified intervals of MD .xyz sim")
parser.add_argument("-f", help="Inputfile .xyz file of MD sim")
parser.add_argument("-box", type=float, help="Box size of system")
parser.add_argument("-center", type=int, default=1, help="Index of atom to be used for center, default = 1")
parser.add_argument("-atoms", nargs="+", default=['O','N'], help="Element symbol(s) to be analyzed, default is N and O")
parser.add_argument("-dist", type=float, default=8.0, help="Distance (angstroms) from central atom within which to include atoms, default=8.0")
parser.add_argument("-folp", nargs="+", default=None, help="Optional argument to adjust FOLP parameters. Default for elements is 1.15 -- to specify non-default value(s) specify space separated Element Value (Element2 Value2 ...) e.g. N 1.10")
parser.add_argument("-start", default=0, type=int, help="Optional argument specifying frame to begin at, default=0")
parser.add_argument("-end", default=0, type=int, help="Optional argument specifying frame to end at")
parser.add_argument("-skip", default=1, type=int, help="Optional integer specifying frames to optionally skip (default: 1, no-skipping)")
parser.add_argument("-o", default="feff.inp", help="Optional name used for output files, default feff.inp")
args = parser.parse_args()


def write_feff_header(s, title):
    s.write(f"TITLE    Model: {title}\n\n")
    s.write("*        pot xsph fms path genfmt ff2x\n")
    s.write("CONTROL  1   1    1   1    1      1\n")
    s.write("PRINT    0   0    0   1    0      0\n\n")
    s.write("*        r_fms1 [ lfms1 nscmt  ca    nmix]\n")
    s.write("SCF      6.0      1     30     0.05  10\n\n")
    s.write("CRITERIA 0      0\n\n")
    s.write("EXAFS    20\n\n")
    s.write("RPATH    6.5\n")
    s.write("NLEG     8\n\n")
    s.write("EDGE     L3\n")
    s.write("S02      1.0\n\n")

def write_feff_potentials(s, d, cz, ct):
    s.write("POTENTIALS\n")
    s.write("* ipot   Z     tag\n")
    s.write(f"    0    {cz}    {ct}\n")
    sub = d.drop_duplicates(subset=['ipot'], keep='first')
    s.write(sub.to_string(columns=['ipot','aNum','Elem'],header=False,index=False, col_space=5))
    s.write("\n\n")

def write_feff_atoms(s, d, ct):
    s.write("ATOMS\n")
    s.write("* x          y          z      ipot tag distance\n")
    s.write(f"  0.000000   0.000000   0.000000 0 {ct} 0.00000\n")
    s.write(d.to_string(columns=['f1','f2','f3','ipot','Elem','distance'],header=False,index=False))
    s.write("\n\n")

def write_feff_end(s):
    s.write("END\n")

def write_xyz_header(s, a, f):
    s.write(str(a)+"\n")
    s.write(f"Frame {f}\n")

symb_to_num = { "H":"1", "He":"2", "Li":"3", "Be":"4", "B":"5", "C":"6", "N":"7", "O":"8", "F":"9", "Ne":"10", 
"Na":"11", "Mg":"12", "Al":"13", "Si":"14", "P":"15", "S":"16", "Cl":"17", "Ar":"18", "K":"19", "Ca":"20", 
"Sc":"21", "Ti":"22", "V":"23", "Cr":"24", "Mn":"25", "Fe":"26", "Co":"27", "Ni":"28", "Cu":"29", "Zn":"30", 
"Ga":"31", "Ge":"32", "As":"33", "Se":"34", "Br":"35", "Kr":"36", "Rb":"37", "Sr":"38", "Y":"39", "Zr":"40", 
"Nb":"41", "Mo":"42", "Tc":"43", "Ru":"44", "Rh":"45", "Pd":"46", "Ag":"47", "Cd":"48", "In":"49", "Sn":"50", 
"Sb":"51", "Te":"52", "I":"53", "Xe":"54", "Cs":"55", "Ba":"56", "La":"57", "Ce":"58", "Pr":"59", "Nd":"60", 
"Pm":"61", "Sm":"62", "Eu":"63", "Gd":"64", "Tb":"65", "Dy":"66", "Ho":"67", "Er":"68", "Tm":"69", "Yb":"70", 
"Lu":"71", "Hf":"72", "Ta":"73", "W":"74", "Re":"75", "Os":"76", "Ir":"77", "Pt":"78", "Au":"79", "Hg":"80", 
"Tl":"81", "Pb":"82", "Bi":"83", "Po":"84", "At":"85", "Rn":"86", "Fr":"87", "Ra":"88", "Ac":"89", "Th":"90", 
"Pa":"91", "U":"92", "Np":"93", "Pu":"94", "Am":"95", "Cm":"96", "Bk":"97", "Cf":"98", "Es":"99", "Fm":"100", 
"Md":"101", "No":"102", "Lr":"103", "Rf":"104", "Db":"105", "Sg":"106", "Bh":"107", "Hs":"108", "Mt":"109", "Ds":"110", 
"Rg":"111", "Cn":"112", "Nh":"113", "Fl":"114", "Mc":"115", "Lv":"116", "Ts":"117", "Og":"118" }

if __name__ == '__main__':

    #Generate directories containing selected XYZ files
    frame = 0
    newframe = args.start
    NAtoms = 0
    newline = 0
    path = str()
    allpaths = []

    with open(args.f, 'r') as readfile:
        for i, line in enumerate(readfile):
            if i==newline:
                NAtoms = int(line)
                newline += 2+NAtoms
                if frame==newframe:
                    path = os.path.join(os.getcwd(), "f"+str(frame))
                    allpaths.append(path)
                    if not os.path.exists(path):
                        os.makedirs(path)
                    savefile = open(path+"/f"+str(frame)+".xyz", "w")
                    write_xyz_header(savefile, NAtoms, frame)
            elif i in range(newline-NAtoms, newline-1) and frame==newframe:
                savefile.write(line)
            elif i==newline-1:
                if frame==newframe:
                    savefile.write(line)
                    savefile.close()
                    newframe += args.skip
                frame +=1
            if args.end != 0 and frame > args.end:
                break
    
    #For each directory's XYZ file, run Richard's FEFF_input0.py code, copied and modified below 
    for p in allpaths:
        #Extract xyz info
        data = np.genfromtxt(p+"/"+p.split("/")[-1]+".xyz", dtype='O, float, float, float', skip_header=2, usecols= (0, 1, 2, 3))
        data = pd.DataFrame(data, columns=['f0', 'f1', 'f2', 'f3'])
        data.insert(0, 'AtomNum', range(1, 1 + len(data)))
        data['Elem'] = [x.decode("utf-8") for x in data['f0']] #Decode the symbols column
        
        #Grab central atom info and original coords
        Ca = data.loc[data['AtomNum']==args.center, 'Elem'].values[0]
        Cx = data.loc[data['AtomNum']==args.center, 'f1'].values[0]
        Cy = data.loc[data['AtomNum']==args.center, 'f2'].values[0]
        Cz = data.loc[data['AtomNum']==args.center, 'f3'].values[0]

        #Isoalte chosen atoms
        data = data.loc[data['Elem'].isin(args.atoms)] 
        data['f1'] -= Cx #Translate the coordinates relative to central atoms origin position
        data['f2'] -= Cy
        data['f3'] -= Cz
        
        #Translate atoms outside box boundaries if needed
        for col in ['f1','f2','f3']:
            data.loc[data[col] <= -(0.5*args.box), col] += args.box
            data.loc[data[col] >= (0.5*args.box), col] -= args.box
        
        #Calculate distances from origin/central atom
        data['distance'] = ( (data['f1']**2) + (data['f2']**2) + (data['f3']**2) )**0.5
        data = data.sort_values('distance') #Sort by distance
        data = data[data.distance <= args.dist]

        #Generate ipot and atomic number info
        data['ipot'] = data.groupby(['Elem'], sort=False).ngroup()
        data['ipot'] += 1 #increment ipot by 1 since center atom will be ipot 0
        data['aNum'] = data['Elem'].map(symb_to_num)

        #Generate .xyz file of modified coords
        with open(p+"/"+p.split("/")[-1]+"-mod.xyz", "w") as savefile:
            write_xyz_header(savefile, len(data)+1, p.split("/")[-1][1:])
            savefile.write(Ca+"\t0.00000\t0.00000\t0.00000\n")
            savefile.write(data.to_string(columns=['Elem','f1','f2','f3'],header=False,index=False))

        #Generate feff.inp file
        with open(p+"/"+args.o, "w") as savefile:
            write_feff_header(savefile, p.split("/")[-1]) 
            write_feff_potentials(savefile, data, symb_to_num[Ca], Ca)
            write_feff_atoms(savefile, data, Ca)
            write_feff_end(savefile)

