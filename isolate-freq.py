#!/usr/bin/env python
import sys, argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description="Used to parse through .csv file containing -NO2 freq information")
parser.add_argument("-f", help="Inputfile .csv file of MD sim -NO2 Freq info")
parser.add_argument("-o", default="freq-comp.csv", help="Output .csv name")
args = parser.parse_args()

if __name__ == '__main__':

    freqinfo = defaultdict(list)

    with open(args.f, 'r') as readfile:
        next(readfile)
        for line in readfile:
            data = line.split(",")
            if data[-1].strip() not in freqinfo and float(data[0])<1000: continue
            elif data[-1].strip() not in freqinfo and float(data[0]) >1000:
                freqinfo[data[-1].strip()] = [data[0],data[1],data[2],max([abs(float(x)) for x in data[3:12]])]
            elif max([abs(float(x)) for x in data[3:12]]) > freqinfo[data[-1].strip()][3]:
                freqinfo[data[-1].strip()] = [data[0],data[1],data[2],max([abs(float(x)) for x in data[3:12]])]

    with open(args.o, 'w') as savefile:
        for item in freqinfo:
            savefile.write(",".join([item.split("-")[1].split(".")[0]]+[str(x) for x in freqinfo[item]]+["\n"]))


