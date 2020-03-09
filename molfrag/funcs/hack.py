import os
import subprocess
import helper
import logging


def get_mcs(smiles1, smiles2):
    """ Run mcs-cliquer over cmd. """

    args = [helper.MCS_PATH, smiles1, smiles2]
    r = subprocess.run(args, stdout=subprocess.PIPE)

    stdout = r.stdout.decode("utf8")

    smiles3 = []
    for line in stdout.split("\n"):
        if line.startswith("rEsUlT"):
            mol = line.split()[1].strip()
            if mol not in smiles3:
                smiles3.append(mol)

    return smiles3


def draw_smiles(smiles, path):
    s = f'obabel -:"{smiles}" -O "{path}"'
    subprocess.run(s, shell=True, stderr=subprocess.DEVNULL)


class Canonicalizer:
    def __init__(self):
        self.pairs = dict()
        self.do_split = True
        self.min_length = 7

    def __call__(self, smiles):
        if smiles not in self.pairs:

            s = f'obabel -:"{smiles}" -ocan'
            r = subprocess.run(
                s, stdout=subprocess.PIPE, shell=True, stderr=subprocess.DEVNULL
            )
            stdout = r.stdout.decode("ascii")
            canonical_smiles = stdout.strip()
            canonical_smiles = (
                canonical_smiles.replace("/", "").replace("\\", "").replace("@", "")
            )

            self.pairs[smiles] = canonical_smiles

        return self.pairs[smiles]

    def split(self, smiles_list, from_roots):
        """
        If all are disconnected, split all and return biggest fragment.
        If some are disconnected, return all connected.
        If none are disconnected, return all connected.
        """

        char_count = lambda s: sum(char.isalpha() for char in s)

        all_disconnected = all("." in smiles for smiles in smiles_list)

        if all_disconnected:
            if not from_roots:
                return []
            frags = {
                frag
                for smiles in smiles_list
                for frag in smiles.split(".")
                if char_count(frag) >= self.min_length
            }
            if not frags:
                return []
            return [max(frags, key=char_count)]

        else:

            all_connected = all("." not in smiles for smiles in smiles_list)
            if all_connected:
                return [
                    smiles
                    for smiles in smiles_list
                    if char_count(smiles) >= self.min_length
                ]

            else:
                return [
                    smiles
                    for smiles in smiles_list
                    if "." not in smiles and char_count(smiles) >= self.min_length
                ]
