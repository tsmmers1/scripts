#!/usr/bin/env python
import sys, argparse
from periodictable import Number_To_Symbol 

parser = argparse.ArgumentParser()
parser.add_argument("i", help="Gaussian outputfile name")
parser.add_argument("-o", default="coords.xyz", help="name of XYZ outputfile")
parser.add_argument("-f", type=int, nargs="+", help="Step(s) to extract. -1 will take the last step")
args = parser.parse_args()

if __name__ == '__main__':

    NAtoms = 0
    Steps = []
    
    for position, line in enumerate(open(args.i, 'r')):
        if "NAtoms=" in line and NAtoms == 0:
            NAtoms = int(line.split("NAtoms=")[1].split()[0])
        if "Standard orientation" in line:
            Steps.append(position)

    if args.f == None:
        SelectSteps = Steps
    else:
        Frames = args.f

        for frame in Frames:
            if abs(frame) > len(Steps)-1:
                sys.exit("Error: maximum steps is "+str(len(Steps)-1))
 
        SelectSteps = [Steps[i] for i in Frames]

    SelectCoords = []
    for i in SelectSteps:
        SelectCoords = SelectCoords+list(range(i+5,i+NAtoms+5))
    savefile = open(args.o, 'w')
    for position, line in enumerate(open(args.i, 'r')):
        if position in SelectSteps:
            savefile.write(str(NAtoms)+"\nstep "+str(Steps.index(position))+" of "+str(len(Steps)-1)+"\n")
        elif position in SelectCoords:
            elem = Number_To_Symbol[int(line.split()[1])]
            x = line.split()[3]
            y = line.split()[4]
            z = line.split()[5]
            savefile.write("     ".join([elem,x,y,z])+"\n")
            
    savefile.close()

