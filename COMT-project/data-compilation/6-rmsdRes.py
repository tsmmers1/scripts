import os, sys
from collections import defaultdict

models = []
with open("CompiledResults.csv","r") as readfile:
    for line in readfile:
        if line.split(",")[1].split("-")[0] == "ByHand":
            continue
        else:
            models.append(line.split(",")[1])

pdbdata = {}
with open("3bwm.pdb", "r") as readfile:
    for line in readfile:
        if line[0:6] == "ATOM  " or line[0:6] == "HETATM":
            if line[17:20]=="SAM" and line[13:15]=="CA":
                pdbdata[str(int(line[23:26]))+line[17:20].strip()+"CA'"] = [float(line[30:39]), float(line[38:47]), float(line[46:55])]
            elif line[17:20]=="SAM" and line[13:15]=="CB":
                pdbdata[str(int(line[23:26]))+line[17:20].strip()+"CB'"] = [float(line[30:39]), float(line[38:47]), float(line[46:55])]
            else:
                pdbdata[str(int(line[23:26]))+line[17:20].strip()+line[12:17].strip()] = [float(line[30:39]), float(line[38:47]), float(line[46:55])]

def calcrmsd(filename, pdbdata):
    with open(filename, "r") as readfile:
        res = defaultdict(int)
        rmsdval = defaultdict(float)
        for line in readfile:
            if line[76:78].strip() == "H": continue
            if line[85:87]=="-1": continue
            if line[17:20].strip()=="WAT" or line[17:20].strip()=="HOH": continue
            if line[17:20].strip() != "SAM" and line[17:20].strip() != "DNC":
                name = str(int(line[23:26]))+line[17:20].strip()+line[12:17].strip()
                x = float(line[30:39])
                y = float(line[38:47])
                z = float(line[46:55])
                diff = (x-pdbdata[name][0])**2 + (y-pdbdata[name][1])**2 + (z-pdbdata[name][2])**2
                res[int(line[23:26])] +=1 
                rmsdval[int(line[23:26])] +=diff
    return res, rmsdval

models = models[1:]
savefile = open("rmsdres.csv","w")
writeset = [38,39,40,41,42,46,64,66,67,68,70,71,72,89,90,91,92,95,117,118,119,120,139,141,142,143,144,145,146,169,170,173,174,175,198,199]
savefile.write("model," + ",".join(map(str,writeset)) + "," + ",".join(map(str,writeset)) + "," + ",".join(map(str,writeset)) + "\n")
for name in models:
    Rname = "./pdbs/"+name+"-R.pdb"
    TSname = "./pdbs/"+name+"-TS.pdb"
    Pname = "./pdbs/"+name+"-P.pdb"
    
    Rres, Rrmsd = calcrmsd(Rname, pdbdata)
    TSres, TSrmsd = calcrmsd(TSname, pdbdata)
    Pres, Prmsd = calcrmsd(Pname, pdbdata)

    if Rres != TSres or Pres != TSres:
        print("Error with model: ", name)
        sys.exit()
    
    Rset = ["NA"]*len(writeset)
    TSset = ["NA"]*len(writeset)
    Pset = ["NA"]*len(writeset)
    for i in range(0,len(writeset)):
        if writeset[i] in Rres.keys() and Rres[writeset[i]] >1:
            Rset[i] = "%.3f"% (Rrmsd[writeset[i]]/Rres[writeset[i]])**0.5
            TSset[i] = "%.3f"%(TSrmsd[writeset[i]]/TSres[writeset[i]])**0.5
            Pset[i] = "%.3f"%(Prmsd[writeset[i]]/Pres[writeset[i]])**0.5

    savefile.write(name + "," + ",".join(map(str,Rset)) + "," + ",".join(map(str,TSset)) + "," + ",".join(map(str,Pset)) + "\n")

savefile.close()
