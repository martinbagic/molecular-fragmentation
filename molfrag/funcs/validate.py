from collections import defaultdict
import logging


def validate_tranclo(tc):

    # check if all children converge
    assert sum(len(v) == 0 for v in tc.values()
               ) == 1, "There is no ultimate child."

    # check that each has 0 or 2+ parents
    P = defaultdict(set)
    for p, cs in tc.items():
        for c in cs:
            P[c].add(p)

    assert all(len(ps) != 1 for ps in P.values()
               ), "There are children with one parent only."

    logging.info('Validation successful.')
