#!/usr/bin/env python
import sys, argparse

parser = argparse.ArgumentParser(description="generates mopac .mop input file from xyz coords")
parser.add_argument("f", help="Inputfile .xyz file name")
parser.add_argument("-o", default="model.mop", help="Name of output .mop file (default: model.mop)")
args = parser.parse_args()

def rewrite_atom(a):
    if "EU" in a or "Eu" in a:
        return "Eu"
    elif "N" in a:
        return "N"
    elif "C" in a:
        return "C"
    elif "H" in a:
        return "H"
    elif "O" in a:
        return "O"
    else:
        sys.exit(f"Error interpreting atom type of atom {a}.")


if __name__ == '__main__':

    header = "PM7 SPARKLE CHARGE=0 BFGS GNORM=0.25 XYZ\n"

    with open(args.o, 'w') as savefile:
        savefile.write(header)
        savefile.write(f"{args.f}\n\n")


        with open(args.f, 'r') as xyzfile:
            next(xyzfile)
            next(xyzfile)
            for line in xyzfile:
                atom = rewrite_atom(line.split()[0])
                x = line.split()[1]
                y = line.split()[2]
                z = line.split()[3]
                savefile.write(f"{atom:>3}     {x}   1   {y}   1   {z}   1\n")


 
