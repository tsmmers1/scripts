#!/usr/bin/env python
import sys, argparse, numpy, xlsxwriter
from collections import defaultdict
import calculate_rmsd

parser = argparse.ArgumentParser(description="Constructs RMSD matrices for conformers of given sizes")
parser.add_argument("f", help="Inputfile list of .xyz files to construct RMSD matrices of")
parser.add_argument("-t", default=1.0, type=float, help="Threshold RMSD below which structures will be classified as near-identical, default: 1.0")
parser.add_argument("-o", default="rmsd_matrices.xlsx", help="Name used for output .xlsx file, default: rmsd_matrices.xlsx")
args = parser.parse_args()

def group_common_NAtoms(names_list):
    grouped_names = defaultdict(list)
    for name in names_list:
        with open(name, 'r') as f:
            #Group files with common NAtoms (first line of XYZ file)
            grouped_names[int(f.readline())].append(name)
    return grouped_names

def identify_uniques_and_similars(structures, threshold):
    unique = []
    similar = []

    for i in range(0, len(structures)):
        if any(structures[i] == x[0] for x in similar): continue

        for j in range(i+1, len(structures)):
            if any(structures[j] == x[0] for x in similar): continue
            rmsd = calculate_rmsd.main([structures[i], structures[j], '-urks', '--reorder'])
            if float(rmsd) <= threshold:
                similar.append([structures[j],structures[i],str(rmsd)])

        unique.append(structures[i])
    return unique, similar

def generate_rmsd_matrix(structs):
    mat = numpy.zeros(shape=(len(structs), len(structs)))
    for i in range(0, len(structs)):
        for j in range(i+1, len(structs)):
            rmsd = calculate_rmsd.main([structs[i], structs[j], '-urks', '--reorder'])
            mat[i][j] = rmsd
            mat[j][i] = rmsd
    return mat


if __name__ == '__main__':

    #Extract file names
    names = [x.strip() for x in open(args.f, 'r').readlines()]

    #Identify NAtoms in XYZ files and group common sizes
    grouped_names = group_common_NAtoms(names)
    grouped_names_sort = list(grouped_names.keys())
    grouped_names_sort.sort()

    #Initialize results excel file
    workbook = xlsxwriter.Workbook(args.o)

    #Save Distribution data
    worksheet = workbook.add_worksheet("Distribution")
    worksheet.write_row(0,0,['NAtoms','Count','Freq'])
    for pos, group in enumerate(grouped_names_sort):
        if len(grouped_names[group]) == 1:
            worksheet.write_row(pos+1,0,[str(group), str(len(grouped_names[group])), str(len(grouped_names[group])/len(names)), grouped_names[group][0]])
        else:
            worksheet.write_row(pos+1,0,[str(group), str(len(grouped_names[group])), str(len(grouped_names[group])/len(names))])

    #For each grouping with more than one structure, construct RMSD matrix
    for group in grouped_names_sort:

        if len(grouped_names[group]) <= 1: continue

        #Identify Unique/Similar Structures
        unique, similar = identify_uniques_and_similars(grouped_names[group], args.t)

        #Construct RMSD matrix of all unique structures
        if len(unique) > 1:
            rmsd_mat = generate_rmsd_matrix(unique)
        
        #Save similarity data to sheet
        worksheet = workbook.add_worksheet("NAtoms"+str(group))
        worksheet.write_row(0,0,['Unique','','Similar','SimilarToUnique','RMSD'])
        for pos, data in enumerate(unique):
            worksheet.write(pos+1, 0, data)
        for pos, data in enumerate(similar):
            worksheet.write_row(pos+1, 2, data)

        #Save RMSD matrix data to sheet
        if len(unique) > 1:
            worksheet = workbook.add_worksheet("RMSD"+str(group))
            worksheet.write_row(0,1,unique)
            worksheet.write_column(1,0,unique)
            for pos, data in enumerate(rmsd_mat):
                worksheet.write_row(pos+1, 1, data)
    
    workbook.close()

