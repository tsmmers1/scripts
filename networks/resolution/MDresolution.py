#! /usr/bin/env python
import os, sys
import argparse, re
from collections import defaultdict

parser = argparse.ArgumentParser(description='Analyzes Arpeggio data of MD snapshots for resolution')
parser.add_argument('-data', help='file containing MD arpeggio frame information')
parser.add_argument('-intervals', nargs='+', default=[2,3,4,5], help='integers for the selection of alternating frames i.e. 1 2 3 4 5')
parser.add_argument('-save', default='MDresolution.csv', help='name of savefile')
args = parser.parse_args()

#Assign each interval an index for storing in the dictionary's list. Format Index : [Interval, Interval_total_count]
intindex = {1:[1,0]}
for i in range(2, len(args.intervals)+2):
    intindex[i] = [int(args.intervals[i-2]), 0]

#Read in data
edges = {}
with open(args.data, "r") as readfile:
    for line in readfile:
        sline = line.split(",")
        
        if sline[0] == "Frame": #Identify edges
            for i in range(1,len(sline)):
                #Ignore Waters for now
                if "".join(re.findall("[a-zA-Z]+", sline[i].strip().split(".")[1])) != "W":
                    edges[i] = [sline[i].strip()] +  ([0]*(len(intindex.keys())+1))

        else:
            #Add divisible frames to total count
            frame = int(sline[0])
            for i in intindex:
                if frame % intindex[i][0] == 0:
                    intindex[i][1] +=1

            for i in edges:
                if int(sline[i]) != 0:
                    for j in intindex:
                        if frame % intindex[j][0] == 0:
                            edges[i][j] +=1

#Write the data to a file
savefile = open(args.save, "w")

for i in intindex:
    savefile.write("Frames in Alt%s:,%s\n"%(intindex[i][0],intindex[i][1]))

header1 = ['Interaction,'] + [',Alt%s,,'%intindex[i][0] for i in intindex]
header2 = [',Freq,RelFreq,Diff']*len(intindex)
savefile.write("".join(header1)+"\n")
savefile.write("".join(header2)+"\n")

for i in edges:
    datapoint = [edges[i][0]] + [',%s,%s,%s'%(edges[i][j], (edges[i][j]/intindex[j][1]), ((edges[i][j]/intindex[j][1])-(edges[i][1]/intindex[1][1]))) for j in intindex]
    savefile.write("".join(datapoint)+"\n")
savefile.close()
