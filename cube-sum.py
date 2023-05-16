#!/usr/bin/env python
import os, sys
import argparse

parser = argparse.ArgumentParser(description="Calculates the sum of the electron density for a cube file")
parser.add_argument("-f", help="name of cube file")
args = parser.parse_args()


if __name__ == '__main__':

    Cube = open(args.f, 'r').readlines()
    Catoms = int(Cube[2].split()[0])

    #Store initial volume data
    Cpos = 0.0
    Cneg = 0.0
    for i in range(Catoms+6, len(Cube)):
        for val in Cube[i].split():
            if float(val) <= 0.0:
                Cneg += float(val)
            elif float(val) >= 0.0:
                Cpos += float(val)

    print(f'Positive: {Cpos}')
    print(f'Negative: {Cneg}')
    print(f'Sum:      {Cpos+Cneg}')
