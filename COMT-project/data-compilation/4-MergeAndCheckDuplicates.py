import os, sys

if __name__ == '__main__':

    myfile1 = open("GAUresults.csv","r").readlines()
    myfile2 = open("MCSC.csv","r").readlines()

    data = []
    compdata = []
    header2 = myfile1[0].strip() + myfile2[0][5:]
    for line1 in myfile1[1:]:
        for line2 in myfile2[1:]:
            if line1.split(",")[1] == line2.split(",")[0]:
                compdata.append([line2.split(",")[0],line2.split(",")[1:]])
                data.append(line1.strip() + "," + ",".join(line2.split(",")[1:]))
                break
    with open("GAUcompiled.csv", "w") as savefile:
        savefile.write(header2)
        for line in data:
            savefile.write(line)

    for i in range(0,len(compdata)):
        for j in range(i+1, len(compdata)):
            if compdata[i][1] == compdata[j][1]:
                check1 = "/home/tsmmers1/src/COMT/data-compilation/pdbs/" + compdata[i][0] + "-TS.pdb"
                check2 = "/home/tsmmers1/src/COMT/data-compilation/pdbs/" + compdata[j][0] + "-TS.pdb"
                if os.path.isfile(check1) == True and os.path.isfile(check2) == True:
                    check1data = []
                    for line in open(check1).readlines():
                        check1data.append(line[17:20] + line[23:26] + line[77])
                    check2data = []
                    for line in open(check2).readlines():
                        check2data.append(line[17:20] + line[23:26] + line[77])
                    check1data.sort()
                    check2data.sort()
                    if check1data == check2data:
                        status = True
                    else: status = False
                else:
                    print("Error in checking files:", check1, check2)
                print(compdata[i][0], compdata[j][0])

