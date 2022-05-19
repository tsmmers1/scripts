import os, sys

if __name__ == '__main__':

    myfile = open("GAUresults.csv","r").readlines()

    allresnum = []
    alldicts = []
    for line in myfile[1:]:
        model = line.split(',')[1]
        path = os.getcwd() + '/pdbs/' + model + '-TS.pdb'
        
        modeldict = {}
        with open(path,'r') as openfile:
            for line in openfile:
                resnum = int(line[22:26])
                atomID = line[12:16].strip()
                resID = line[17:20].strip()

                if resnum not in allresnum:
                    allresnum.append(resnum)
                if resnum not in modeldict:
                    modeldict[resnum] = set()

                if resID == "SAM" or resID == "DNC" or resID == "MG":
                    modeldict[resnum].add("S")
                elif resID == "HOH" or resID == "WAT":
                    modeldict[resnum].add("W")
                elif atomID == "C" or atomID == "O":
                    modeldict[resnum].add("C")
                elif atomID == "N" or atomID == "H":
                    modeldict[resnum].add("N")
                elif resID == "GLY" and atomID == "HA":
                    modeldict[resnum].add("R")
                elif atomID == "CB":
                    modeldict[resnum].add("R")
                else:
                    continue
        alldicts.append(modeldict)

    allresnum.sort()
    with open("MCSC.csv","w") as savefile:
        header = "model," + ",".join(map(str, allresnum)) + "\n"
        savefile.write(header)
        for i in range(1,len(myfile)):
            model = myfile[i].split(',')[1]
            fg = [0] * len(allresnum)
            for j in range(0,len(fg)):
                if allresnum[j] in alldicts[i-1].keys():
                    fg[j] = "".join(alldicts[i-1][allresnum[j]])
            savefile.write(model + "," + ",".join(map(str, fg)) + "\n")


            




