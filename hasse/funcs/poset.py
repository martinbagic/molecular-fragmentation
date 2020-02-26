from . import hack

from collections import defaultdict
import logging


class Poset:
    def __init__(self, genfunc, roots, canonicalizer):
        self.genfunc = genfunc
        self.roots = roots
        self.canonicalizer = canonicalizer

    def __call__(self):

        to_add = self.roots[:]  # set of new nodes to be added to the graph

        P = defaultdict(set)
        C = defaultdict(set)
        S = defaultdict(set)

        added = []

        while to_add:
            logging.debug(f'{len(added):^3} / {len(to_add)+len(added):^3}')

            a = to_add.pop(0)  # new node (a)

            resolve = added[:]  # explore rel with new node

            while resolve:
                b = resolve.pop(0)

                if b in S[a] or b in P[a] or b in C[a]:  # relationship already investigated
                    continue

                x = self.genfunc(a, b)

                if self.canonicalizer:
                    x = self.canonicalizer(x)

                if a == x:  # a = x < b; b is a parent of a
                    C[b].add(a)
                    P[a].add(b)

                    for p in P[b]:  # all parents of b are parents of a
                        P[a].add(p)
                        C[p].add(a)
                        if p in resolve:
                            resolve.remove(p)

                    for c in C[a]:  # all children of a are children of b
                        P[c].add(b)
                        C[b].add(c)
                        if c in resolve:
                            resolve.remove(c)

                elif b == x:  # a > x = b; a is a parent of b
                    C[a].add(b)
                    P[b].add(a)

                    for p in P[a]:  # all parents of a are parents of b
                        P[b].add(p)
                        C[p].add(b)
                        if p in resolve:
                            resolve.remove(p)

                    for c in C[b]:  # all children of b are children of a
                        P[c].add(a)
                        C[a].add(c)
                        if p in resolve:
                            resolve.remove(c)

                else:  # a > x < b; a and b are siblings and x their child
                    S[a].add(b)
                    S[b].add(a)

                    C[a].add(x)
                    C[b].add(x)
                    P[x].add(a)
                    P[x].add(b)

                    if x not in to_add:  # if node is new, add to graph
                        to_add.append(x)
                        print(a,b,x)

            added.append(a)

        return C
