#!/usr/bin/env python
import os, sys
import argparse
import pandas as pd
import numpy as np
from collections import defaultdict


parser = argparse.ArgumentParser(description="Compiles information on FEFF XAFS chi data and generates averaged spectra")
parser.add_argument("-f", help="Input text file containing list of chi.dat files to be compiled")
parser.add_argument("-o", default="compiled_chi.xlsx", help="Optional name used for output .xlsx file, default compiled_chi.xlsx")
args = parser.parse_args()


if __name__ == '__main__':

    #Grab chi file names
    chifiles = [x.strip() for x in open(args.f,'r').readlines()]
    
    #Store each chi.dat info for each chi value into list
    chi = defaultdict(list)

    for chifile in chifiles:
        data = open(chifile, 'r').readlines()
        header = None
        for i,j in enumerate(data):
            if "k          chi" in j:
                header = i
                break

        chi["k_values"].append(chifile)
        if float(data[header+1].split()[0]) != 0:
            chi[0.0].append(None)
        for i in range(header+1,len(data)):
            chi[float(data[i].split()[0])].append(float(data[i].split()[1]))
    
    #Convert dict to dataframe
    df=pd.DataFrame.from_dict(chi,orient='index')
    df.reset_index(inplace=True)
    df.columns = df.iloc[0]
    df = df[1:]
    df['k'] = df['k_values']
    df['AverageChi']=df.iloc[:, 1:len(df.columns)-1].mean(axis=1)
    df['MinChi']=df.iloc[:, 1:len(df.columns)-2].min(axis=1)
    df['MaxChi']=df.iloc[:, 1:len(df.columns)-3].max(axis=1)
    df['kChi']=df['k']*df['AverageChi']
    df['k2Chi']=df['k']*df['k']*df['AverageChi']
    df['k3Chi']=df['k']*df['k']*df['k']*df['AverageChi']
    
    #Save data to spreadsheet
    df.to_excel(args.o, sheet_name='FEFF',index=False)





            

