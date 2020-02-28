import os
import subprocess
import helper
import logging


def get_mcs(smiles1, smiles2):
    ''' Run mcs-cliquer over cmd. '''

    args = [helper.MCS_PATH, smiles1, smiles2]
    r = subprocess.run(args, stdout=subprocess.PIPE)

    stdout = r.stdout.decode('utf8')

    smiles3 = []
    for line in stdout.split('\n'):
        if line.startswith('rEsUlT'):
            mol = line.split()[1].strip()
            if mol not in smiles3:
                smiles3.append(mol)

    return smiles3


def draw_smiles(smiles, path):
    s = f'obabel -:"{smiles}" -o svg > "{path}"'
    subprocess.run(s, shell=True, stderr=subprocess.DEVNULL)


class Canonicalizer:
    def __init__(self):
        self.pairs = dict()
        self.splittings = dict()
        self.do_split = True

    def __call__(self, smiles):
        if smiles not in self.pairs:

            s = f'obabel -:"{smiles}" -ocan'
            r = subprocess.run(s, stdout=subprocess.PIPE,
                               shell=True, stderr=subprocess.DEVNULL)
            stdout = r.stdout.decode('ascii')
            canonical_smiles = stdout.strip()
            canonical_smiles = canonical_smiles.replace(
                '/', '').replace('\\', '').replace('@', '')

            if self.do_split:
                canonical_smiles = self.biggest(canonical_smiles)

            self.pairs[smiles] = canonical_smiles

        return self.pairs[smiles]

    def biggest(self, smiles):
        if smiles not in self.splittings:
            self.splittings[smiles] = max(
                smiles.split('.'),
                key=lambda s: sum(c.isalpha() for c in s)
            )
        return self.splittings[smiles]
