import os, sys

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
    rmssum = 0
    rmscount = 0
    samsum = 0
    samcount = 0
    catsum = 0
    catcount = 0
    with open(filename, "r") as readfile:
        for line in readfile:
            if line[76:78].strip() == "H": continue
            if line[85:87]=="-1": continue
            if line[17:20].strip()=="WAT" or line[17:20].strip()=="HOH": continue
            if line[17:20].strip() == "SAM":
                name = str(int(line[23:26]))+line[17:20].strip()+line[12:17].strip()
                x = float(line[30:39])
                y = float(line[38:47])
                z = float(line[46:55])
                diff = (x-pdbdata[name][0])**2 + (y-pdbdata[name][1])**2 + (z-pdbdata[name][2])**2
                samsum += diff
                samcount +=1
            elif line[17:20].strip()=="DNC":
                name = str(int(line[23:26]))+line[17:20].strip()+line[12:17].strip()
                x = float(line[30:39])
                y = float(line[38:47])
                z = float(line[46:55])
                diff = (x-pdbdata[name][0])**2 + (y-pdbdata[name][1])**2 + (z-pdbdata[name][2])**2
                catsum += diff
                catcount +=1
            else:
                name = str(int(line[23:26]))+line[17:20].strip()+line[12:17].strip()
                x = float(line[30:39])
                y = float(line[38:47])
                z = float(line[46:55])
                diff = (x-pdbdata[name][0])**2 + (y-pdbdata[name][1])**2 + (z-pdbdata[name][2])**2
                rmssum += diff
                rmscount +=1
    return '%.3f'%((rmssum/rmscount)**0.5), '%.3f'%((samsum/samcount)**0.5), '%.3f'%((catsum/catcount)**0.5)

models = models[1:]
savefile = open("rmsd.csv","w")
savefile.write("Model,Rrmsd,Rsam,Rcat,TSrmsd,TSsam,TScat,Prmsd,Psam,Pcat\n")
for name in models:
    Rname = "./pdbs/"+name+"-R.pdb"
    TSname = "./pdbs/"+name+"-TS.pdb"
    Pname = "./pdbs/"+name+"-P.pdb"
    
    Rrmsd, Rsam, Rcat = calcrmsd(Rname, pdbdata)
    TSrmsd, TSsam, TScat = calcrmsd(TSname, pdbdata)
    Prmsd, Psam, Pcat = calcrmsd(Pname, pdbdata)
    savewrite = [name, Rrmsd, Rsam, Rcat, TSrmsd, TSsam, TScat, Prmsd, Psam, Pcat]
    savefile.write(",".join(savewrite) + "\n")
savefile.close()

