#!/usr/bin/env python
import sys, argparse
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("-f", help="Name of Gaussian outputfile containing frequency info from Freq keyword")
parser.add_argument("-s", default=1.0, type=float, help="(Optional) Scaling factor")
parser.add_argument("-o", default="spectrum.csv", help="Name for output .csv file")
args = parser.parse_args()

if __name__ == '__main__':

    with open(args.o, 'w') as savefile:
        savefile.write("Frequency (cm-1),Intensity,Intensity Scaled (s="+str(args.s)+")\n")
        with open(args.f, 'r') as readfile:
            freq = []
            inten = []
            sinten = []
            for line in readfile:
                if "Frequencies --" in line:
                    freq = line.split("--")[1].split()
                elif "IR Inten    --" in line:
                    inten = [float(x) for x in line.split("--")[1].split()]
                    sinten = [(args.s*x) for x in inten]
                    
                    for i in range(0,len(freq)):
                        savefile.write(",".join([freq[i],str(inten[i]),str(sinten[i])+"\n"]))
                    freq = []
                    inten = []
                    sinten = []
