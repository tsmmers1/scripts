import os, sys

if __name__ == '__main__':

    myfile = open("GAUresults.csv","r").readlines()
    for line in myfile[1:]:
        directory = line.split(',')[0]
        model = line.split(',')[1]
        natoms = int(line.split(',')[20])

        path = os.getcwd() + '/pdbs/' + model + '-TS.pdb'

        counter = 0
        with open(path,'r') as openfile:
            for line in openfile:
                counter+=1

        if counter!=natoms:
            print("Error: Number of atoms different between PDB and Gaussain file for: ", directory)


