import os, sys, argparse, subprocess
from string import ascii_lowercase
import extract_gau

def check_for_output(path, myfile):
    checkpath = str(path + myfile)
    if os.path.isfile(checkpath) == False:
        print("Error: no ", myfile, " file exists in the directory ", path)
        return 1
    else:
        return 0

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Compiles COMT project data into a file for analysis.')
    parser.add_argument('-dirs', dest='dirs', default="DirList", help='list_of_Gaussian_TS_directories')
    parser.add_argument('-save', dest='save', default="GAUresults.csv", help='CSV_savefile')
    parser.add_argument('-pdbs', dest='pdbs', default="/pdbs/", help='save_pdbs_directory')
    args = parser.parse_args()

    #Check if listed TS/IRC1/IRC2 directories exist and are duplicate in existing savefile
    alldirs = [x.strip() for x in open(args.dirs).readlines()]
    if os.path.isfile(args.save):
        sdirs = [x.split(',')[0] for x in open(args.save).readlines()]
        sdirs = sdirs[1:]
        sIDs = [x.split(',')[1] for x in open(args.save).readlines()]
        sIDs = sIDs[1:]
    else:
        sdirs = []
        sIDs = []
        with open(args.save, "w") as savefile:
            savefile.write("Path, ID, " +
                    "TS_SCFenergy, TS_ZPEenergy, TS_INTenergy, TS_ENTenergy, TS_GIBenergy, " +
                    "R_Path, R_SCFenergy, R_ZPEenergy, R_INTenergy, R_ENTenergy, R_GIBenergy, " +
                    "P_Path, P_SCFenergy, P_ZPEenergy, P_INTenergy, P_ENTenergy, P_GIBenergy, " +
                    "NBasis, NAtoms, TS_deltaE, TS_deltaG, RXN_deltaE, RXN_deltaG, Imag, " +
                    "R_COdist, TS_COdist, P_COdist, R_CSdist, TS_CSdist, P_CSdist, " +
                    "R_MgO1dist, TS_MgO1dist, P_MgO1dist, R_MgO2dist, TS_MgO2dist, P_MgO2dist, " +
                    "R_EHdist, TS_EHdist, P_EHdist, R_OHdist, TS_OHdist, P_OHdist\n")
    wdirs = []
    check = 0
    #Tpath variable made here and below to change where template.pdb location is
    for path in alldirs:
        if path not in sdirs:
            wdirs.append(path)
            check += check_for_output(path, "/1.out")
            check += check_for_output(path, "/irc1/1.out")
            check += check_for_output(path, "/irc2/1.out")
            check += check_for_output(path, "/template.pdb")
    if check != 0:
        sys.exit()

    #Check pdb save location
    savepdbpath = os.getcwd() + args.pdbs
    if os.path.isdir(savepdbpath) == False:
        print("Error: unable to locate path ", savepdbpath)
        sys.exit()

    with open(args.save, "a") as savefile:
        for path in wdirs:
            #Extract Information of TS and IRCs
            COdist, COdist1, COdist2, CSdist, CSdist1, CSdist2 = extract_gau.compute_OCS_dist(path)
            MgO1dist, MgO2dist, MgO1dist1, MgO2dist1, MgO1dist2, MgO2dist2 = extract_gau.compute_MgO_dist(path)
            EHdist, OHdist, EHdist1, OHdist1, EHdist2, OHdist2 = extract_gau.compute_EHO_dist(path)

            SCFenergy, ZPEenergy, INTenergy, ENTenergy, GIBenergy, NBasis, NAtoms, Imag = extract_gau.extract_gau_TS_data(str(path+"/1.out"))
            if CSdist1 < CSdist2:
                SCFenergyR, ZPEenergyR, INTenergyR, ENTenergyR, GIBenergyR, DirR = extract_gau.extract_gau_IRC_data(str(path+"/irc1/1.out"), NBasis, NAtoms)
                SCFenergyP, ZPEenergyP, INTenergyP, ENTenergyP, GIBenergyP, DirP = extract_gau.extract_gau_IRC_data(str(path+"/irc2/1.out"), NBasis, NAtoms)
                COdistR, COdistP, CSdistR, CSdistP = COdist1, COdist2, CSdist1, CSdist2
                MgO1distR, MgO1distP, MgO2distR, MgO2distP = MgO1dist1, MgO1dist2, MgO2dist1, MgO2dist2
                EHdistR, EHdistP, OHdistR, OHdistP = EHdist1, EHdist2, OHdist1, OHdist2
            else:
                SCFenergyR, ZPEenergyR, INTenergyR, ENTenergyR, GIBenergyR, DirR = extract_gau.extract_gau_IRC_data(str(path+"/irc2/1.out"), NBasis, NAtoms)
                SCFenergyP, ZPEenergyP, INTenergyP, ENTenergyP, GIBenergyP, DirP = extract_gau.extract_gau_IRC_data(str(path+"/irc1/1.out"), NBasis, NAtoms)
                COdistR, COdistP, CSdistR, CSdistP = COdist2, COdist1, CSdist2, CSdist1
                MgO1distR, MgO1distP, MgO2distR, MgO2distP = MgO1dist2, MgO1dist1, MgO2dist2, MgO2dist1
                EHdistR, EHdistP, OHdistR, OHdistP = EHdist2, EHdist1, OHdist2, OHdist1

            TSdE = (float(SCFenergy) - float(SCFenergyR))*627.51
            TSdG = (float(GIBenergy) - float(GIBenergyR))*627.51
            RXNdE = (float(SCFenergyP) - float(SCFenergyR))*627.51
            RXNdG = (float(GIBenergyP) - float(GIBenergyR))*627.51

            #Generate ID for model
            ID = str()
            for let1 in ascii_lowercase:
                mybool = False
                for let2 in ascii_lowercase:
                    tryname = "Model-" + str(NAtoms) + "-" + let1 + let2
                    if tryname not in sIDs:
                        ID = tryname
                        sIDs.append(tryname)
                        mybool = True
                        break
                if mybool == True:
                    break

            #Write information to CSV
            savelist = [path, ID,
                    SCFenergy, ZPEenergy, INTenergy, ENTenergy, GIBenergy,
                    DirR.strip(), SCFenergyR, ZPEenergyR, INTenergyR, ENTenergyR, GIBenergyR,
                    DirP.strip(), SCFenergyP, ZPEenergyP, INTenergyP, ENTenergyP, GIBenergyP,
                    NBasis, NAtoms, TSdE, TSdG, RXNdE, RXNdG, Imag,
                    COdistR, COdist, COdistP, CSdistR, CSdist, CSdistP,
                    MgO1distR, MgO1dist, MgO1distP, MgO2distR, MgO2dist, MgO2distP,
                    EHdistR, EHdist, EHdistP, OHdistR, OHdist, OHdistP]
            savefile.write(",".join(map(str, savelist)) + "\n")
            
            #Generate PDBs of model ID
            Tpath = path.rsplit("/ts",1)[0]
            subproc = subprocess.Popen(["python3","/home/tsmmers1/git/RINRUS/bin/gopt_to_pdb.py","-f","-1","-o",path+"/1.out","-p",path+"/template.pdb"],cwd=savepdbpath)
            subproc.wait()
            subproc = subprocess.Popen(["mv", "final.pdb", ID+"-TS.pdb"], cwd=savepdbpath)
            subproc.wait()
            subproc = subprocess.Popen(["python3","/home/tsmmers1/git/RINRUS/bin/gopt_to_pdb.py","-f","-1","-o",DirR.strip(),"-p",path+"/template.pdb"],cwd=savepdbpath)
            subproc.wait()
            subproc = subprocess.Popen(["mv", "final.pdb", ID+"-R.pdb"], cwd=savepdbpath)
            subproc.wait()
            subproc = subprocess.Popen(["python3","/home/tsmmers1/git/RINRUS/bin/gopt_to_pdb.py","-f","-1","-o",DirP.strip(),"-p",path+"/template.pdb"],cwd=savepdbpath)
            subproc.wait()
            subproc = subprocess.Popen(["mv", "final.pdb", ID+"-P.pdb"], cwd=savepdbpath)
            subproc.wait()


