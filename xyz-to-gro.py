#!/usr/bin/env python
import sys, argparse


parser = argparse.ArgumentParser(description="Translates .xyz trajectory to .gro and adds velocity info")
parser.add_argument("f", help="Inputfile .xyz file containing coords")
parser.add_argument("v", help="Inputfile .xyz file containing velocities")
parser.add_argument("-resname", default="MOL", help="Up to 5-character name for residue, default MOL")
parser.add_argument("-o", default="converted", help="Name used for output .gro, -pos.xyz, and -vel.xyz, default name: converted")
args = parser.parse_args()

def extract_coords(cline, vline):
    atom1 = cline.split()[0]
    atom2 = vline.split()[0]
    if atom1 != atom2:
        sys.exit("Error: different atoms identified in comparison")

    coords = [float(x)/10 for x in cline.split()[1:]]
    vels = [float(x)*0.0529177249/0.00002418884254 for x in vline.split()[1:]] #Convert bohr/au_time to nm/ps

    return atom1, coords[0], coords[1], coords[2], vels[0], vels[1], vels[2]
    

if __name__ == '__main__':

    coords = open(args.f, 'r').readlines()
    veloc = open(args.v, 'r').readlines()
    if len(coords) != len(veloc):
        sys.exit("Error: different coordinate and velocity file lengths")
    if int(coords[0]) != int(veloc[0]):
        sys.exit("Error: different coordinate and velocity structure sizes")

    NAtoms = int(coords[0])
    Header = 0
    Footer = 1+NAtoms
    Frame = 0
    AtomN = 1

    savefileGro = open(args.o+".gro", 'w')
    savefilePos = open(args.o+"-pos.xyz", 'w')
    savefileVel = open(args.o+"-vel.xyz", 'w')

    for i in range(0,len(coords)):
        if i == Header:
            savefilePos.write(coords[i])
            savefileVel.write(veloc[i])

        elif i == Header+1:
            if "time = " in coords[i]:
                time = float(coords[i].split("time =")[1].split(",")[0])
                savefileGro.write(f"File constructed from xyz-to-gro.py, t= {time}\n{NAtoms}\n")
            else:
                savefileGro.write(f"File constructed from xyz-to-gro.py, frame= {Frame}\n{NAtoms}\n")
            Header += 2+NAtoms
            Frame += 1
            savefilePos.write(coords[i])
            savefileVel.write(veloc[i])

        elif i == Footer:
            #write final coords line
            atom, px, py, pz, vx, vy, vz = extract_coords(coords[i], veloc[i])
            savefileGro.write(f'    1{args.resname : <5}{atom : >5}{AtomN : >5}{px : >8.3f}{py : >8.3f}{pz : >8.3f}{vx : >8.4f}{vy : >8.4f}{vz : >8.4f}\n')
            savefileGro.write("   2.00000   2.00000   2.00000")
            if i < len(coords):
                savefileGro.write("\n")
            Footer += 2+NAtoms
            AtomN = 1
            savefilePos.write(f'{atom : >5}  {px : >20.10}  {py : >20.10}  {pz : >20.10}\n')
            savefileVel.write(f'{atom : >5}  {vx : >20.10}  {vy : >20.10}  {vz : >20.10}\n')
        else:
            atom, px, py, pz, vx, vy, vz = extract_coords(coords[i], veloc[i])
            savefileGro.write(f'    1{args.resname : <5}{atom : >5}{AtomN : >5}{px : >8.3f}{py : >8.3f}{pz : >8.3f}{vx : >8.4f}{vy : >8.4f}{vz : >8.4f}\n')
            AtomN +=1
            savefilePos.write(f'{atom : >5}  {px : >20.10}  {py : >20.10}  {pz : >20.10}\n')
            savefileVel.write(f'{atom : >5}  {vx : >20.10}  {vy : >20.10}  {vz : >20.10}\n')


    savefileGro.close()
    savefilePos.close()
    savefileVel.close()

