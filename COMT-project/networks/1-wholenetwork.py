#!/usr/bin/python
import argparse
import os, sys


if __name__ == '__main__':
    """ Usage: python3 network-gen.py -s connectsets-compiled2.sif -o network.png """
    parser = argparse.ArgumentParser(description='Generate Network from probe')
    parser.add_argument('-p', help='probe file')
    parser.add_argument('-s', help='Output Network PNG')
    args = parser.parse_args()

    edgelist = []
    with open(args.p, "r") as probefile:
        for line in probefile:
            res1 = int(line[12:15])
            res2 = int(line[29:32])
            if res1 == res2:
                continue
            if res2 < res1:
                temp = res1
                res1 = res2
                res2 = temp
            if res1 > 303 or res2 > 303:
                inter = "W"
            elif res1 == 300 or res2 == 300 or res1 == 301 or res2 == 301 or res1 == 302 or res2 == 302:
                inter = "S"
            else:
                inter = "R"
            
            def resattribute(number):
                if number < 300:
                    return "RES"
                elif number == 300:
                    return "MG"
                elif number == 301 or number == 302:
                    return "SUB"
                elif number == 303:
                    return "K"
                elif number > 303:
                    return "WAT"
            res1A = resattribute(res1)
            res2A = resattribute(res2)

            if [res1,res1A,inter,res2,res2A] not in edgelist:
                edgelist.append([res1,res1A,inter,res2,res2A])

    with open(args.s, "w") as savefile:
        savefile.write("Res1,Res1A,Int,Res2,Res2A\n")
        for line in edgelist:
            savefile.write(",".join(map(str,line)) + "\n")
