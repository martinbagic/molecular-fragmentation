# run from cheminf

import os
import subprocess


def get_mcs(smiles1, smiles2):
    mcs = "./mcs-cliquer-1.0.0/mcs/mcs"

    with open('temp1.smi', 'w') as f:
        f.write(smiles1)

    with open('temp2.smi', 'w') as f:
        f.write(smiles2)

    args = [mcs, 'temp1.smi', 'temp2.smi']
    r = subprocess.run(args, stdout=subprocess.PIPE)

    stdout = r.stdout.decode('utf8')
    try:
        smiles3 = stdout.split()[-2]
    except:
        print('no mcs', smiles1, smiles2)
        smiles3 = ''

    os.remove('temp1.smi')
    os.remove('temp2.smi')

    return smiles3

# if __name__ == '__main__':
#     mol1 = "O1[C@@H]2[C@]34[C@H]([C@H](N(CC3)C)Cc3c4c1c(O)cc3)C=C[C@@H]2O"
#     mol2 = "O[C@H](c1cc(O)c(O)cc1)CNC"
#     get_mcs(mol1,mol2)


# - obabel -:"C12C(CCC1)CCCC2" -o svg > mol.svg

def make_mol(smiles, path):
    # print(smiles)
    s = f'obabel -:"{smiles}" -o svg > {path}'
    # args = s.split()
    subprocess.run(s, shell=True)


def get_canonical(smiles, canonics):

    if smiles not in canonics:
        s = f'obabel -:"{smiles}" -ocan'
        r = subprocess.run(s, stdout=subprocess.PIPE, shell=True)
        stdout = r.stdout.decode('utf8')
        canonical_smiles = stdout.strip()
        canonical_smiles = canonical_smiles.replace('/','').replace('\\','')
        canonics[smiles] = canonical_smiles

