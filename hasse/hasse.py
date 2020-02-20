import graphviz
from genfuncs import genfuncs
from hack import make_mol, get_canonical

import pickle

import os
dir_path = os.path.dirname(os.path.realpath(__file__))


smiles_replacement = dict(zip(
    '<>:"/\|?*()',
    'üéâäàåçêëèïîì'
))


def smiles_replace(s):
    for k, v in smiles_replacement.items():
        s = s.replace(k, v)
    return s


def atom_count(s):
    return sum(x.isalpha() for x in s)


class Hasse:
    def __init__(self, mode, roots, plot_g=True, plot_tc=True, plot_images=False):
        # init
        self.mode = mode
        self.roots = roots
        self.directory = 'hasse/output'
        self.canonics = dict()

        self.plot_images = plot_images

        if self.plot_images:
            self.roots = [self.get_canonical(smiles)
                          for smiles in self.roots]

        # calculate
        g = self.get_poset()
        tc = self.get_transitive_closure(g)

        # with open(f'{self.directory}/pickle-{self.mode}', 'rb') as file:
        #     tc = pickle.load(file)

        # plot
        if plot_g:
            self.plot(g, f'ALL-{self.mode}')
        if plot_tc:
            self.plot(tc, f'TRANCLO-{self.mode}')

    def get_canonical(self, smiles):
        get_canonical(smiles, self.canonics)
        return self.canonics[smiles]

    def get_poset(self):
        genfunc = genfuncs[self.mode]
        stack = self.roots[:]

        g = dict()

        while stack:
            pop = stack.pop()
            g[pop] = set()
            for n in g:
                if pop == n:
                    continue
                child = genfunc(pop, n)
                if self.plot_images:
                    child = self.get_canonical(child)
                    if '.' in child:  # FIX THIS
                        print(child)
                        child = max(child.split('.'),
                                    key=lambda x: atom_count(x))
                if child != n:
                    g[n].add(child)
                if child != pop:
                    g[pop].add(child)

                if child not in g and child not in stack:
                    stack.append(child)

            print(len(stack), pop)

        return g

    def get_transitive_closure(self, G):
        nodes = list(G.keys())
        g = {node: [] for node in nodes}

        for start in nodes:
            for end in G[start]:
                flag = False
                for mid in G[start]:
                    if end in G[mid] and end != mid:
                        flag = True
                        break
                if not flag:
                    g[start].append(end)

        with open(f'{self.directory}/pickle-{self.mode}', 'wb') as file:
            pickle.dump(g, file)

        return g

    def plot(self, g, filename):
        graph = graphviz.Digraph()
        graph.format = 'svg'
        graph.edge_attr.update(
            arrowhead='vee',
            arrowsize='0.5',
            splines='curved',
        )

        if self.plot_images:
            for n in g.keys():
                name = smiles_replace(str(n))
                path = f'{self.directory}/{name}.svg'
                if not name:
                    name = 'EMPTY'
                else:
                    make_mol(str(n), path)
                shape = 'rect' if n in self.roots else 'none'
                graph.node(str(n),
                           label='', shape=shape,
                           image=f'{name}.svg',)
        else:
            for root in self.roots:
                graph.node(str(root), str(root),
                           fillcolor='gold', style='filled')

        for k, v in g.items():
            for n in v:
                graph.edge(str(k), str(n))

        graph.render(filename=filename, directory=self.directory)


if __name__ == '__main__':

    # Hasse(
    #     'gcd',
    #     [80, 40, 20, 50, 12, 77, 13, 11, 15, 17],
    # )

    # Hasse(
    #     'common',
    #     ['epinephrine', 'melatonin', 'norepinephrine',
    #      'triiodothyronine', 'thyroxine', 'dopamine',
    #      'morphine', 'methamphetamine', 'progesterone', 'dihydrotestosterone',
    #      'banana', 'kazakhstan', 'lettuce', ],
    # )

    # Hasse(
    #     'substr',
    #     ['epinephrine', 'melatonin', 'norepinephrine',
    #      'triiodothyronine', 'thyroxine', 'dopamine',
    #      'morphine', 'methamphetamine', 'progesterone', 'dihydrotestosterone',
    #      'banana', 'kazakhstan', 'lettuce', ],
    #     plot_g=False,
    # )

    Hasse(
        'mcs',
        [
            "CNCC(C1=CC(=C(C=C1)O)O)O",  # adrenaline
            "CN1CCC2=C3C1CC4=C(C3=CC=C2)C(=C(C=C4)O)O",  # apomorphine
            # "C1CNCC(C2=CC(=C(C(=C21)Cl)O)O)C3=CC=C(C=C3)O",  # fenoldopam
            # "COC1=C(C=C(C=C1)CCN2CCN(CC2)C3=CC=CC=C3Cl)OC",  # mefeclorazine
            "CN1CCC23C4C1CC5=C2C(=C(C=C5)O)OC3C(C=C4)O",  # morphine
            # "C1OC2=C(O1)C=C(C=C2)C(C(=N)N)O",  # olmidine
            "CC12CCC3C(C1CCC2=O)CCC4=C3C=CC(=C4)O",  # estrone
            "CC12CCC(=O)CC1CCC3C2CCC4(C3CCC4O)C",  # dihydrotestosterone
            "CC(=O)C1CCC2C1(CCC3C2CCC4=CC(=O)CCC34C)C",  # progesterone
            "CC(CC1=CC=CC=C1)NC",  # methamphetamine

        ],
        plot_g=False,
        plot_images=True,
    )
