#!/usr/bin/env python
import os, sys
import argparse, xlsxwriter
from itertools import islice

parser = argparse.ArgumentParser(description="Compiles energy data from NWPEsSE output files")
parser.add_argument("f", help="Input text file containing list of NWPEsSE output files to process")
parser.add_argument("-top", default=50, help="When analyzing the energies among multiple outputs, compile a list of the top # lowest energy structures, default=50") 
parser.add_argument("-o", default="compiled_energies.xlsx", help="Optional name used for output .xlsx file, default compiled_energies.xlsx")
args = parser.parse_args()


if __name__ == '__main__':
    fnames = [x.strip() for x in open(args.f, 'r').readlines()]

    top_names = []
    top_energies = []
    max_top_energies = None

    workbook = xlsxwriter.Workbook(args.o)

    for name in fnames:
        energies = []
        sname = name.split("/")[-2]
        
        with open(name, 'r') as efile:
            counter_write = 4
            for line in iter(efile):
                if counter_write == 0:
                    if line == "===============================================================\n" : #encountered end, write output to sheet
                        if len(sname) >31: #Abbreviate sheet name to be less than 31 characters
                            wname = sname[-31:]
                        else:
                            wname = sname

                        worksheet = workbook.add_worksheet(sname)
                        row = 0
                        for pair in energies:
                            worksheet.write(row, 0, pair[0])
                            worksheet.write(row, 1, pair[1])
                            row+=1
                        break 

                    energies.append([line.split()[0], line.split()[1]]) #Store data for worksheet

                    if len(top_energies) < args.top: #Fill up top energies if less than top
                        top_names.append(sname+"_"+line.split()[0])
                        top_energies.append(float(line.split()[1]))
                        max_top_energies = max(top_energies) #Store highest energy in top energies so it doesn't have to be re-found for each comparison
                    elif float(line.split()[1]) < max_top_energies:
                        top_names[top_energies.index(max_top_energies)] = sname+"_"+line.split()[0] #Replace name of max_energy with better value
                        top_energies[top_energies.index(max_top_energies)] = float(line.split()[1]) #Replace energy of max_energy with better value
                        max_top_energies = max(top_energies) #Update max_top when list gets updated

                elif line == "Reordered from low to high energy:\n":
                    counter_write -=1
                elif counter_write != 4:
                    counter_write -=1

    #Write top 50 energy info
    sorted_names = [x for _, x in sorted(zip(top_energies, top_names))]
    top_energies.sort()
    worksheet = workbook.add_worksheet("Top")
    worksheet.write_column(0, 0, sorted_names)
    worksheet.write_column(0, 1, top_energies)
    

    workbook.close()



    
