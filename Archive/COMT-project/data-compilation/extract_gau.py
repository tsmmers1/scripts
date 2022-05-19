import os, sys, argparse, subprocess, math, csv

def check_for_output(path, myfile):
    checkpath = str(path + myfile)
    if os.path.isfile(checkpath) == False:
        print("Error: no ", myfile, " file exists in the directory ", path)
        return 1
    else:
        return 0

def extract_gau_TS_data(filename):
    proc1 = subprocess.check_output(['grep','SCF Done',filename], text=True)
    SCFenergy = proc1.splitlines()[-1].split()[4]

    proc2 = subprocess.check_output(['grep','Sum of e',filename], text=True)
    ZPEenergy = proc2.splitlines()[0].split()[-1]
    INTenergy = proc2.splitlines()[1].split()[-1]
    ENTenergy = proc2.splitlines()[2].split()[-1]
    GIBenergy = proc2.splitlines()[3].split()[-1]

    proc3 = subprocess.check_output(['grep','NBasis=',filename], text=True)
    NBasis = proc3.splitlines()[-1].split()[1]

    proc4 = subprocess.check_output(['grep','NAtoms=',filename], text=True)
    NAtoms = proc4.splitlines()[-1].split()[1]

    proc5 = subprocess.check_output(['grep','Frequencies --',filename], text=True)
    if float(proc5.splitlines()[0].split()[3]) < 0:
        print("Error: More than one Imaginary Frequency", filename)
    Imag = proc5.splitlines()[0].split()[2]

    return SCFenergy, ZPEenergy, INTenergy, ENTenergy, GIBenergy, NBasis, NAtoms, Imag

def extract_gau_IRC_data(filename, basis, atoms):
    proc1 = subprocess.check_output(['grep','SCF Done',filename], text=True)
    SCFenergy = proc1.splitlines()[-1].split()[4]

    proc2 = subprocess.check_output(['grep','Sum of e',filename], text=True)
    ZPEenergy = proc2.splitlines()[0].split()[-1]
    INTenergy = proc2.splitlines()[1].split()[-1]
    ENTenergy = proc2.splitlines()[2].split()[-1]
    GIBenergy = proc2.splitlines()[3].split()[-1]

    proc3 = subprocess.check_output(['grep','NBasis=',filename], text=True)
    NBasis = proc3.splitlines()[-1].split()[1]
    if NBasis != basis:
        print("Error: NBasis not the same for file: ", filename)
    proc4 = subprocess.check_output(['grep','NAtoms=',filename], text=True)
    NAtoms = proc4.splitlines()[-1].split()[1]
    if NAtoms != atoms:
        print("Error: NAtoms not the same for file: ", filename)
    proc5 = subprocess.check_output(['grep','Frequencies --',filename], text=True)
    if float(proc5.splitlines()[0].split()[2]) < 0:
        print("Error: Imaginary frequency found in IRC file: ", filename)

    return SCFenergy, ZPEenergy, INTenergy, ENTenergy, GIBenergy, filename

def extract_OCS_pos(PDBname):
    proc1 = subprocess.check_output(['grep','-n','O2  DNC A 302',PDBname], text=True)
    posO = int(proc1.split(":")[0])

    proc2 = subprocess.check_output(['grep','-n','CE  SAM A 301',PDBname], text=True)
    posC = int(proc2.split(":")[0])

    proc3 = subprocess.check_output(['grep','-n','SD  SAM A 301',PDBname], text=True)
    posS = int(proc3.split(":")[0])
    return posO, posC, posS

def extract_gau_final_coord_pos(filename):
    proc4 = subprocess.check_output(['grep','-n','Coordinates (Angstroms)',filename], text=True)
    pos = int(proc4.splitlines()[-1].split(":")[0])+1
    return pos

def extract_gau_coords(filename, pos):
    posT = pos + extract_gau_final_coord_pos(filename)
    with open(filename) as myfile:
        for i, line in enumerate(myfile):
            if i==posT:
                X = float(line.split()[3])
                Y = float(line.split()[4])
                Z = float(line.split()[5])
    return X, Y, Z

def distance(x1,y1,z1,x2,y2,z2):
    d = math.sqrt(((x2-x1)**2)+((y2-y1)**2)+((z2-z1)**2))
    return d

def compute_OCS_dist(path):
    PDBpath = path + "/template.pdb"
    TSpath = path + "/1.out"
    IRC1path = path + "/irc1/1.out"
    IRC2path = path + "/irc2/1.out"

    posO, posC, posS = extract_OCS_pos(PDBpath)
    Ox, Oy, Oz = extract_gau_coords(TSpath, posO)
    Cx, Cy, Cz = extract_gau_coords(TSpath, posC)
    Sx, Sy, Sz = extract_gau_coords(TSpath, posS)

    Ox1, Oy1, Oz1 = extract_gau_coords(IRC1path, posO)
    Cx1, Cy1, Cz1 = extract_gau_coords(IRC1path, posC)
    Sx1, Sy1, Sz1 = extract_gau_coords(IRC1path, posS)

    Ox2, Oy2, Oz2 = extract_gau_coords(IRC2path, posO)
    Cx2, Cy2, Cz2 = extract_gau_coords(IRC2path, posC)
    Sx2, Sy2, Sz2 = extract_gau_coords(IRC2path, posS)

    COdist = distance(Ox,Oy,Oz,Cx,Cy,Cz)
    CSdist = distance(Cx,Cy,Cz,Sx,Sy,Sz)
    COdist1 = distance(Ox1,Oy1,Oz1,Cx1,Cy1,Cz1)
    CSdist1 = distance(Cx1,Cy1,Cz1,Sx1,Sy1,Sz1)
    COdist2 = distance(Ox2,Oy2,Oz2,Cx2,Cy2,Cz2)
    CSdist2 = distance(Cx2,Cy2,Cz2,Sx2,Sy2,Sz2)
    
    return COdist, COdist1, COdist2, CSdist, CSdist1, CSdist2

def extract_MgO_pos(PDBname):
    proc1 = subprocess.check_output(['grep','-n','MG    MG A 300',PDBname], text=True)
    posMg = int(proc1.split(":")[0])

    proc2 = subprocess.check_output(['grep','-n','O1  DNC A 302',PDBname], text=True)
    posO1 = int(proc2.split(":")[0])

    proc3 = subprocess.check_output(['grep','-n','O2  DNC A 302',PDBname], text=True)
    posO2 = int(proc3.split(":")[0])

    return posMg, posO1, posO2

    
def compute_MgO_dist(path):
    PDBpath = path + "/template.pdb"
    TSpath = path + "/1.out"
    IRC1path = path + "/irc1/1.out"
    IRC2path = path + "/irc2/1.out"

    posMg, posO1, posO2 = extract_MgO_pos(PDBpath)
    MGx, MGy, MGz = extract_gau_coords(TSpath, posMg)
    O1x, O1y, O1z = extract_gau_coords(TSpath, posO1)
    O2x, O2y, O2z = extract_gau_coords(TSpath, posO2)

    MGx1, MGy1, MGz1 = extract_gau_coords(IRC1path, posMg)
    O1x1, O1y1, O1z1 = extract_gau_coords(IRC1path, posO1)
    O2x1, O2y1, O2z1 = extract_gau_coords(IRC1path, posO2)

    MGx2, MGy2, MGz2 = extract_gau_coords(IRC2path, posMg)
    O1x2, O1y2, O1z2 = extract_gau_coords(IRC2path, posO1)
    O2x2, O2y2, O2z2 = extract_gau_coords(IRC2path, posO2)

    MgO1dist = distance(MGx,MGy,MGz,O1x,O1y,O1z)
    MgO2dist = distance(MGx,MGy,MGz,O2x,O2y,O2z)
    MgO1dist1 = distance(MGx1,MGy1,MGz1,O1x1,O1y1,O1z1)
    MgO2dist1 = distance(MGx1,MGy1,MGz1,O2x1,O2y1,O2z1)
    MgO1dist2 = distance(MGx2,MGy2,MGz2,O1x2,O1y2,O1z2)
    MgO2dist2 = distance(MGx2,MGy2,MGz2,O2x2,O2y2,O2z2)

    return MgO1dist, MgO2dist, MgO1dist1, MgO2dist1, MgO1dist2, MgO2dist2 

def extract_EHO_pos(PDBname):
    with open(PDBname) as ff:
        posE = None
        for i, line in enumerate(ff):
            if "OE2 GLU A 199" in line: posE = i+1
            if "H04 DNC A 302" in line: posH = i+1
            if "O1  DNC A 302" in line: posO = i+1
    return posE, posH, posO

def compute_EHO_dist(path):
    PDBpath = path + "/template.pdb"
    TSpath = path + "/1.out"
    IRC1path = path + "/irc1/1.out"
    IRC2path = path + "/irc2/1.out"

    posE, posH, posO = extract_EHO_pos(PDBpath)
    Hx, Hy, Hz = extract_gau_coords(TSpath, posH)
    Ox, Oy, Oz = extract_gau_coords(TSpath, posO)

    Hx1, Hy1, Hz1 = extract_gau_coords(IRC1path, posH)
    Ox1, Oy1, Oz1 = extract_gau_coords(IRC1path, posO)

    Hx2, Hy2, Hz2 = extract_gau_coords(IRC2path, posH)
    Ox2, Oy2, Oz2 = extract_gau_coords(IRC2path, posO)
    
    OHdist = distance(Hx,Hy,Hz,Ox,Oy,Oz)
    OHdist1 = distance(Hx1,Hy1,Hz1,Ox1,Oy1,Oz1)
    OHdist2 = distance(Hx2,Hy2,Hz2,Ox2,Oy2,Oz2)

    if posE != None:
        Ex, Ey, Ez = extract_gau_coords(TSpath, posE)
        Ex1, Ey1, Ez1 = extract_gau_coords(IRC1path, posE)
        Ex2, Ey2, Ez2 = extract_gau_coords(IRC2path, posE)

        EHdist = distance(Ex,Ey,Ez,Hx,Hy,Hz)
        EHdist1 = distance(Ex1,Ey1,Ez1,Hx1,Hy1,Hz1)
        EHdist2 = distance(Ex2,Ey2,Ez2,Hx2,Hy2,Hz2)
    else:
        EHdist = EHdist1 = EHdist2 = None
    
    return EHdist, OHdist, EHdist1, OHdist1, EHdist2, OHdist2
