#!/usr/bin/env python
import sys, argparse
from rdkit import Chem
from rdkit.Chem import rdDistGeom, AllChem, rdMolAlign

#Code adapted from https://iwatobipen.wordpress.com/2021/01/31/generate-conformers-script-with-rdkit-rdkit-chemoinformatics/

parser = argparse.ArgumentParser(description="Generates a series of conformers using RDKit")
parser.add_argument("-f", help="Inputfile .xyz file of MD sim")
parser.add_argument("-o", default="gen_confs.sdf", help="Name used for output")
parser.add_argument("-n", default=100, type=int, help="Number of conformers")
args = parser.parse_args()

if __name__ == '__main__':
    mol = Chem.AddHs(Chem.MolFromMolFile(args.f), addCoords=True)
    refmol = Chem.AddHs(Chem.Mol(mol))
    param = rdDistGeom.ETKDGv2()
    cids = rdDistGeom.EmbedMultipleConfs(mol, args.n)
    mp = AllChem.MMFFGetMoleculeProperties(mol, mmffVariant='MMFF94s')
    AllChem.MMFFOptimizeMoleculeConfs(mol, numThreads=0, mmffVariant='MMFF94s')

    w = Chem.SDWriter(args.o)
    res = []
    for cid in cids:
        ff = AllChem.MMFFGetMoleculeForceField(mol, mp, confId=cid)
        e = ff.CalcEnergy()
        res.append((cid, e))
    sorted_res = sorted(res, key=lambda x:x[1])
    rdMolAlign.AlignMolConformers(mol)
    for cid, e in sorted_res:
        mol.SetProp('CID', str(cid))
        mol.SetProp('Energy', str(e))
        w.write(mol, confId=cid)
    w.close()


