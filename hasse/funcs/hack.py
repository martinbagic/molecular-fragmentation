import os
import subprocess
import helper


def get_mcs(smiles1, smiles2):
    ''' Run mcs-cliquer over cmd. '''

    with open('temp1.smi', 'w') as f:
        f.write(smiles1)

    with open('temp2.smi', 'w') as f:
        f.write(smiles2)

    args = [helper.MCS_PATH, 'temp1.smi', 'temp2.smi']
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


def draw_smiles(smiles, path):
    s = f'obabel -:"{smiles}" -o svg > "{path}"'
    subprocess.run(s, shell=True)


def get_canonical(smiles, canonics):

    if smiles not in canonics:
        s = f'obabel -:"{smiles}" -ocan'
        r = subprocess.run(s, stdout=subprocess.PIPE, shell=True)
        stdout = r.stdout.decode('utf8')
        canonical_smiles = stdout.strip()
        canonical_smiles = canonical_smiles.replace('/', '').replace('\\', '')
        canonics[smiles] = canonical_smiles
