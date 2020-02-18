import math
from graphviz import Digraph

get_child_funcs = {
    'gcd': lambda a, b: math.gcd(a, b),
    'subseq': lambda a, b: ''.join([x for x in a if x in b]),
    'substr': lambda a, b: max(
        [
            a[i:j]
            for i in range(len(a))
            for j in range(i, len(a))
            if a[i:j] in b
        ] + [''],
        key=lambda x: len(x)
    )
}


class Hasse:
    def __init__(self, mode, roots, plot_g=True, plot_tc=True):
        self.mode = mode
        self.roots = roots
        self.directory = 'output'

        g = self.get_poset()
        tc = self.get_transitive_closure(g)

        if plot_g:
            self.plot(g, f'{self.mode}-complete')
        if plot_tc:
            self.plot(tc, f'{self.mode}-tc')

    def get_poset(self):
        get_child = get_child_funcs[self.mode]
        stack = self.roots[:]

        g = dict()

        while stack:
            pop = stack.pop()
            g[pop] = set()
            for n in g:
                child = get_child(pop, n)
                if child != n:
                    g[n].add(child)
                if child != pop:
                    g[pop].add(child)

                if child not in g and child not in stack:
                    stack.append(child)

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

        return g

    def plot(self, g, filename):
        graph = Digraph('G')
        for k, v in g.items():
            for n in v:
                graph.edge(str(k), str(n))
        graph.render(filename=filename, format='gv', directory=self.directory)


if __name__ == '__main__':

    Hasse(
        'gcd',
        [80, 40, 20, 50, 12],
    )

    Hasse(
        'subseq',
        ['epinephrine', 'melatonin', 'norepinephrine',
         'triiodothyronine', 'thyroxine', 'dopamine'],
    )

    Hasse(
        'substr',
        ['epinephrine', 'melatonin', 'norepinephrine',
         'triiodothyronine', 'thyroxine', 'dopamine'],
        plot_g=False,
    )
