#!/usr/bin/env python
import sys, argparse
from decimal import Decimal

parser = argparse.ArgumentParser(description="Generates a series of QChem inputfiles for computing the electron/spin density of a complex from a user-specified .xyz file")
parser.add_argument("-f", help="Inputfile .xyz file")
parser.add_argument("-atoms", default=None, nargs="+", help="(Optional) Integers specifying atoms to construct model fragments of. Atom ranges indicated by dash (0-12). Atoms of separate models are separated by spaces (0-12 13-24). Atoms of the same model but are nonsequential can be indicated by non-space comma-separation (0-12,14,16-24). Default is include all atoms into the model.")
parser.add_argument("-ext", default=10, help="Amount to extend the box by from maximum coords in Bohr. Default is 10 Bohr, recommended to do 7 or greater")
parser.add_argument("-dim", default=100, help="Grid resolution for the dimensions, default is 100")
parser.add_argument("-o", default="model", help="Generic name used for naming inputfile(s), default is model-#.inp")
args = parser.parse_args()

def write_header(s):
    s.write("! UKS M06 cc-PVTZ VeryTightSCF RIJCOSX GRID7 GRIDX7 CPCM(ACETONITRILE) LARGEPRINT\n")
    s.write("%pal\nnprocs 32\nend\n")
    s.write("%scf\nMaxIter 1500\nDIISMaxEq 15\ndirectresetfreq 1\nConvergence VeryTight\nend\n")

def write_metal_basis(s):
    s.write("%basis\n")
    basis = """newgto Dy
S   5
1     78529.74300                0.000138
2     11854.69900                0.001033
3      2719.98070                0.004861
4       772.40360                0.014340
5       242.03200                0.021620
S   1
1        48.35620                1.0
S   1
1        31.88060                1.0
S   1
1        16.86090                1.0
S   1
1         4.21550                1.0
S   1
1         2.12870                1.0
S   1
1         0.78890                1.0
S   1
1         0.33830                1.0
S   1
1         0.05810                1.0
S   1
1         0.02380                1.0
P   6
1      4069.16260                0.000119
2       962.25980                0.000987
3       308.60090                0.004608
4       112.40990                0.013362
5        32.27070                0.076444
6        22.83780               -0.039861
P   1
1        16.30880                1.0
P   1
1         5.88070                1.0
P   1
1         2.92130                1.0
P   1
1         1.25850                1.0
P   1
1         0.59260                1.0
P   1
1         0.25690                1.0
P   1
1         0.08000                1.0
D   6
1       409.80320                0.001046
2       123.71040                0.008448
3        47.09760                0.033945
4        20.12020                0.063313
5         8.15710                0.310542
6         4.14740                0.443276
D   1
1         2.08250                1.0
D   1
1         0.99980                1.0
D   1
1         0.32020                1.0
D   1
1         0.09130                1.0
F   5
1       129.62740                0.005252
2        47.17270                0.048490
3        21.15860                0.154752
4         9.63810                0.281170
5         4.39530                0.353828
F   1
1         1.94260                1.0
F   1
1         0.79800                1.0
F   1
1         0.28660                1.0
G   4
1        21.15860                0.040920
2         9.63810                0.125497
3         4.39530                0.268397
4         1.94260                0.451595
G   1
1         0.79800                1.0
G   1
1         0.28660                1.0
END
NewECP DY
  N_core 28
  lmax h
  s 1
   1     26.429586000  705.671221000 2
  p 1
   1     17.317034000  254.866989000 2
  d 1
   1     12.913599000   95.045187000 2
  f 1
   1     24.907878000  -54.574093000 2
  g 1
   1     24.148753000  -29.828277000 2
  h 1
   1      1.000000000    0.000000000 2
end
END
"""
    s.write(basis)

def write_plots(s, dim, mol_min, mol_max, name):
    s.write("%plots\n")
    s.write(f"dim1 {dim}\ndim2 {dim}\ndim3 {dim}\n")
    s.write(f"min1 {mol_min[0]}\nmax1 {mol_max[0]}\n")
    s.write(f"min2 {mol_min[1]}\nmax2 {mol_max[1]}\n")
    s.write(f"min3 {mol_min[2]}\nmax3 {mol_max[2]}\n")
    s.write("Format Gaussian_cube\n")
    s.write(f'SpinDens("{name}-sdens.cube");\n')
    s.write(f'ElDens("{name}-edens.cube");\n')
    s.write("end\n")

def write_coords(s, c):
    s.write("*xyz 0 0\n")
    for line in c:
        s.write(line)
    s.write("*\n")

def write_footer(s):
    s.write("\n")

if __name__ == '__main__':

    xyz = open(args.f, 'r').readlines()
    bohr = 1.8897259886
    xyz_max = [float(xyz[2].split()[1])*bohr, float(xyz[2].split()[2])*bohr, float(xyz[2].split()[3])*bohr]
    xyz_min = [float(xyz[2].split()[1])*bohr, float(xyz[2].split()[2])*bohr, float(xyz[2].split()[3])*bohr]
    
    #Find min/max xyz coords in Bohrs
    for atom in xyz[2:]:
        for i in range(0,3):
            xyz_max[i] = max(xyz_max[i], float(atom.split()[i+1])*bohr)
            xyz_min[i] = min(xyz_min[i], float(atom.split()[i+1])*bohr)

    #Identify suitable box dimensions
    diff = [a-b for a,b in zip(xyz_max, xyz_min)]
    maxdim = int(max(diff)+args.ext)
    abc_max = [0,0,0]
    abc_min = [0,0,0]
    for i in range(0,3):
        abc_max[i] = int(xyz_max[i]+((maxdim-diff[i])/2))
        abc_min[i] = abc_max[i]-maxdim

    #Default write all coords to file
    if args.atoms == None:
        fname = args.o+"-0"
        savefile = open(fname+".inp", "w")

        write_header(savefile)
        write_metal_basis(savefile)
        write_plots(savefile, args.dim, abc_min, abc_max, fname)
        write_coords(savefile, xyz[2:])
        write_footer(savefile)
        savefile.close()
    else:
        fint = 0
        for model in args.atoms:
            #Identify atom indices to make models of
            n = []
            for i in model.split(","):
                if "-" in i:
                    n.extend(list(range(int(i.split("-")[0]), int(i.split("-")[1])+1)))
                else:
                    n.append(int(i))
            #Grb selected coords
            modcoords = [xyz[i+2] for i in n]
            
            #Generate model file
            fname = args.o+"-"+str(fint)
            savefile = open(fname+".inp", "w")

            write_header(savefile)
            write_metal_basis(savefile)
            write_plots(savefile, args.dim, abc_min, abc_max, fname)
            write_coords(savefile, modcoords)
            write_footer(savefile)
            savefile.close()

            fint +=1
 
