#!/usr/bin/env python
import sys, argparse
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("-f", help="Name of .gro trajectory inputfile")
parser.add_argument("-i", nargs = '+', help="Atom indices to serve as point to measure radial distances from")
parser.add_argument("-d", default=3.3, type=float, help="Float of radial distance (Angstroms)")
parser.add_argument("-s", nargs = '+', help="Three-character names of solvent")
parser.add_argument("-o", default="frames", help="Generic name for output .dat file")
args = parser.parse_args()

def distance(x1,y1,z1,x2,y2,z2):
    d = ( ((x2-x1)**2) + ((y2-y1)**2) + ((z2-z1)**2) )**0.5
    return d

if __name__ == '__main__':

    CenterIDs = [int(x) for x in args.i]
    Models = defaultdict(list)

with open(args.f, 'r') as readfile:
    NAtoms = 0
    CenterAtoms = []
    OtherAtoms = []
    Model = set()
    frame=0

    for i, line in enumerate(readfile):
        if i==1:
            NAtoms = int(line)

        #Beginning of frames
        elif i==0 or i==(NAtoms+3)*frame or i==1+((NAtoms+3)*frame): 
            continue

        #End of frames
        elif i==(NAtoms+2)+((NAtoms+3)*frame):
            #Calculate Distances
            for atom1 in CenterAtoms:
                for atom2 in OtherAtoms:
                    Ax = float(atom1.split()[3])
                    Ay = float(atom1.split()[4])
                    Az = float(atom1.split()[5])
                    Bx = float(atom2.split()[3])
                    By = float(atom2.split()[4])
                    Bz = float(atom2.split()[5])
                    dist = distance(Ax, Ay, Az, Bx, By, Bz)
                    
                    if dist <= (args.d/10):
                        Model.add(atom2[:7].strip())
            Model = list(Model)
            solventcounter = 1
            for i in range(0,len(Model)):
                if Model[i][-3:] in args.s:
                    Model[i] = str(solventcounter)+Model[i][-3:]
                    solventcounter +=1
            Model.sort()
            Model = tuple(Model)
            Models[Model].append(frame)

            #Reset Frame Info
            CenterAtoms = []
            OtherAtoms = []
            Model = set()
            frame+=1
            
        elif int(line.split()[2]) in CenterIDs:
            CenterAtoms.append(line.strip())

        else:
            OtherAtoms.append(line.strip())

#Generate Savefiles
ModelTypes = list(Models)
for i in range(0,len(ModelTypes)):
    with open(args.o+str(i)+".ndx", 'w') as savefile:
        savefile.write("[frames]\n")
        for j in list(Models[ModelTypes[i]]):
            savefile.write(str(j)+"\n")

