#!/usr/bin/env python
import sys, argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description="Generates a .csv file reporting user-specified n element type(s) with shortest distance from an atom over an xyz file. NOTE: IN CURRENT CODE DESIGN, CENTER ATOM MUST OCCUR BEFORE ATOMS MEASURING DIST TO.")
parser.add_argument("-f", help="Inputfile .xyz file of MD sim")
parser.add_argument("-c", type=int, help="Index of center atom (beginning at 1)")
parser.add_argument("-a", nargs='+', help="Element types to measure distances to")
parser.add_argument("-n", type=int, help="n number of items to keep the shortest distance of")
parser.add_argument("-o", default="shortest_dist.csv", help="Name of output .csv file")
args = parser.parse_args()

def dist(x1,y1,z1,x2,y2,z2):
    d = ( (x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)**0.5
    return round(d,4)

if __name__ == '__main__':

    frame = 0
    NAtoms = 0
    newline = 0

    center_pos = []
    shortest_dists = []
    shortest_indices = []

    with open(args.o, 'w') as savefile:
        savefile.write("frame,"+",".join(["dist"+str(x) for x in range(0,args.n)])+","+",".join(["id"+str(x) for x in range(0,args.n)])+"\n")
        
        with open(args.f, 'r') as readfile:
            coords = defaultdict(list)
            for i, line in enumerate(readfile):
                if i==newline:
                    NAtoms = int(line)
                    newline += 2+NAtoms
                    shortest_dists = []
                    shortest_indices = []
                elif i in range(newline-NAtoms, newline-1) and (i-1-(frame*(NAtoms+2))) == args.c:
                    center_pos = [float(line.split()[1]), float(line.split()[2]), float(line.split()[3])]
                elif i in range(newline-NAtoms, newline-1) and line.split()[0] in args.a:
                    ax, ay, az = float(line.split()[1]), float(line.split()[2]), float(line.split()[3])
                    d = dist(center_pos[0], center_pos[1], center_pos[2], ax, ay, az)
                    if len(shortest_dists) < args.n:
                        shortest_dists.append(d)
                        shortest_indices.append(i-1-(frame*(NAtoms+2)))
                    elif d < max(shortest_dists):
                        shortest_indices[shortest_dists.index(max(shortest_dists))] = (i-1-(frame*(NAtoms+2)))
                        shortest_dists[shortest_dists.index(max(shortest_dists))] = d
                elif i==newline-1:
                    shortest_dists, shortest_indices = zip(*sorted(zip(shortest_dists, shortest_indices)))
                    data_str = ",".join([str(x) for x in shortest_dists]+[str(x) for x in shortest_indices])
                    savefile.write(str(frame)+","+data_str+"\n")
                    frame +=1


