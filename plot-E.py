#!/usr/bin/env python
import sys, argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="Plots the Energy reported within the MD *-pos.xyz file output by CP2K")
parser.add_argument("f", help="Inputfile MD .xyz file")
parser.add_argument("-start", default=None, type=int, help="(Optional) Integer specifying step to begin at")
parser.add_argument("-end", default=None, type=int, help="(Optional) Integer specifying the step to end at") 
parser.add_argument("-step", action="store_true", help="(Optional) If flag is provided, use step values reported in the .xyz file [i.e. the values after 'i = '] rather than beginning at step 0")
args = parser.parse_args()


if __name__ == '__main__':

    step = []
    energy = []

    #Extract data from XYZ file
    with open(args.f, 'r') as readfile:
        for line in readfile:
            if "i = " in line:
                if args.step==True:
                    step.append(int(line.split("i =")[1].split(",")[0]))
                energy.append(float(line.split("E =")[1]))

    if args.step==False:
        step = range(0,len(energy))

    #Trim beginning/ending steps if called for
    if args.start != None:
        s_i = step.index(args.start)
        step = step[s_i:]
        energy = energy[s_i:]
    if args.end != None:
        e_i = step.index(args.end)
        step = step[:e_i+1]
        energy = energy[:e_i+1]

    #Plot the energies
    plt.xlabel("Step")
    plt.ylabel("Energy")
    plt.plot(step, energy, color = "black")
    plt.scatter(step, energy)
    plt.show()
