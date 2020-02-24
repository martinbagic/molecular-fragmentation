import os
import subprocess
import helper
import logging


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
        logging.error(f'no MCS for "{smiles1}" and "{smiles}"')
        smiles3 = ''

    os.remove('temp1.smi')
    os.remove('temp2.smi')

    return smiles3


def draw_smiles(smiles, path):
    s = f'obabel -:"{smiles}" -o svg > "{path}"'
    subprocess.run(s, shell=True, stderr=subprocess.DEVNULL)


class Canonicalizer:
    def __init__(self):
        self.pairs = dict()

    def __call__(self, smiles):
        if smiles not in self.pairs:

            s = f'obabel -:"{smiles}" -ocan'
            r = subprocess.run(s, stdout=subprocess.PIPE, shell=True, stderr=subprocess.DEVNULL)
            stdout = r.stdout.decode('ascii')
            canonical_smiles = stdout.strip()
            canonical_smiles = canonical_smiles.replace(
                '/', '').replace('\\', '').replace('@', '')
            
            biggest_smiles = self.biggest(canonical_smiles)

            self.pairs[smiles] = self.biggest(biggest_smiles)

        return self.pairs[smiles]

    def biggest(self, smiles):
        return max(
            smiles.split('.'),
            key=lambda s: sum(c.isalpha() for c in s)
        )
