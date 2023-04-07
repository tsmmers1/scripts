#!/usr/bin/env python
import os, sys
import argparse

parser = argparse.ArgumentParser(description="Cleans CP2K output of consecutive MD simulations for further processing by dpdata (deepmd-kit)")
parser.add_argument("f", help="Output file of CP2K MD sim")
parser.add_argument("-o", default="aimd-clean.log", help="Optional name for output file, default aimd-clean.log")
args = parser.parse_args()


if __name__ == '__main__':

    #initial_energy_pattern_v1 = " INITIAL POTENTIAL ENERGY[hartree] "
    #initial_energy_pattern_v2 = " MD_INI| Potential energy [hartree] "

    #energy_pattern_v1 = " POTENTIAL ENERGY[hartree] "
    #energy_pattern_v2 = " MD| Potential energy [hartree] "

    restart_pattern_v1 = " DBCSR| Multiplication driver "
    restart_pattern_v2 = " DBCSR| CPU Multiplication driver "

    end_pattern_v1 = " INITIAL CELL ANGLS[deg]    = "
    end_pattern_v2 = " MD_INI| Cell angles [deg] "

    first_header_found = False
    first_end_found = False

    bool_stop_writing = False

    savefile = open(args.o, 'w')

    with open(args.f, 'r') as readfile:
        for line in readfile:
            if line.startswith(restart_pattern_v1) or line.startswith(restart_pattern_v2):
                if first_header_found == False:
                    first_header_found = True
                else:
                    bool_stop_writing = True

            elif line.startswith(end_pattern_v1) or line.startswith(end_pattern_v2):
                if first_end_found == False:
                    first_end_found = True
                else:
                    bool_stop_writing = False
                    continue

            if bool_stop_writing == False:
                savefile.write(line)
                                    
