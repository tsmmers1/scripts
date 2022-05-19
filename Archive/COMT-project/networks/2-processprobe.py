#!/usr/bin/python
import os, sys
from collections import Counter

def returntype(name, number):
    if number > 304:
        return "wat"
    elif number == 300 or number == 301 or number == 302:
        return "lig"
    else:
        mc_atoms_dic = {'N': '', 'CA': '', 'C': '', 'O': '', 'H': '', 'HA': '', 'OXT': '', 'HA2': '', 'HA3': '', 'H?': '', 'W': ''}
        if name in mc_atoms_dic.keys():
            return "mc"
        else: return "sc"

if __name__ == '__main__':
    #[wc, cc, so, bo, hb], ...
    res = []
    count = []
    with open("exampleA.probe", "r") as probefile:
        for line in probefile:
            res1 = line[12:15]
            res2 = line[29:32]
            if res1 == "300" or res1 == "301" or res1 == "302":
                restype = returntype(line[38:41].strip(), int(res2))
                if res2 not in res:
                    res.append(res2)
                    count.append([line[6:8]+":"+restype])
                else:
                    count[res.index(res2)].append(line[6:8]+":"+restype)
            if res2 == "300" or res2 == "301" or res2 == "302":
                restype = returntype(line[21:24].strip(), int(res1))
                if res1 not in res:
                    res.append(res1)
                    count.append([line[6:8]+":"+restype])
                else:
                    count[res.index(res1)].append(line[6:8]+":"+restype)
    types = ["wc:mc","wc:sc","wc:wat","cc:mc","cc:sc","cc:wat","hb:mc","hb:sc","hb:wat","so:mc","so:sc","so:wat","bo:mc","bo:sc","bo:wat"]
    print("res wc wc wc cc cc cc hb hb hb so so so bo bo bo")
    print("res mc sc wat mc sc wat mc sc wat mc sc wat mc sc wat")
    for item in res:
        print(item.strip(), end = " ")
        for item2 in types:
            print(Counter(count[res.index(item)])[item2], end=" ")
        print("") 
#        print(item, Counter(count[res.index(item)])['wc'], Counter(count[res.index(item)])['cc'], Counter(count[res.index(item)])['hb'], Counter(count[res.index(item)])['so'], Counter(count[res.index(item)])['bo'])
