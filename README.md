# UE Cheminf

## tasks 25 Feb 2020

- [ ] make cliquer filter isomorphic solutions
- [ ] make cliquer return all mcs solutions which are disconnected

## tasks

- [ ] use openbabel python library
- [ ] make poset generation faster
- [ ] bind mcs-cliquer
- [x] canonicalize: openbabel canonicalization + conformation + chirality
- [x] filter disconnected graphs
- [ ] figure out why mcs-cliquer returns None for "CC" and "CCCC" http://openbabel.org/dev-api/classOpenBabel_1_1OBMol.shtml

## terminology

- modular graph product
- maximum common subgraph (MCS)
- partial order (bin rel: As, R, T), substructure inclusion
- Hasse diagram
- [Bron-Kerbosch alg](http://www.dcs.gla.ac.uk/~pat/jchoco/clique/enumeration/report.pdf)

## resources

### links

- [MCS](https://tripod.nih.gov/?p=189)
- [cliquer](https://users.aalto.fi/~pat/cliquer/cliquer.pdf)
- [publication repo](https://github.com/peter-lind/hasse-manager)
- [indigo](https://github.com/epam/Indigo)
- [SWIG](http://www.swig.org/tutorial.html)
- Flamm presentations: [1](https://www.tbi.univie.ac.at/~xtof/Leere/269019/exercise01.pdf), [2](https://www.tbi.univie.ac.at/~xtof/Leere/270038/ue02.pdf)
- [pybind11](https://pybind11.readthedocs.io/en/stable/basics.html)

### commands

- draw molecule `obabel -:"C12C(CCC1)CCCC2" -o svg > mol.svg`

### observations

- aromatic bonds are considered single or double
- mcs is wrong for CC + ?
- mcs yields disconnected graphs
- one issue is that smiles are not canonicalized stably (one reason is volatile interpretation of aromatic bonds)

### issues

1. getting different outputs for same input (running `python3 hasse/hasse.py -t mcs1`)
   - all three examples are too big, i.e. there are extra molecules being generated
   - inconsistent children (looak at fenoldopam and apomorphine in `small-but-still-too-big` and `too-big1`)
2. missing drawing of molecules, e.g. "CNCCc1ccc(c(c1)O)O" in mcs1

<!-- short and missing last visualization -->
<!-- {'CCNCCc1ccc(c(c1)O)O', 'OC1C=CC2C34C1Oc1c4c(CC2N(CC3)C)ccc1O', 'CN1CCc2c3C1Cc1ccc(c(c1c3ccc2)O)O', 'CNCC(c1ccc(c(c1)O)O)O', 'Oc1ccc(cc1O)CCNCCc1ccccc1', 'Oc1ccc(cc1)C1CNCCc2c1cc(O)c(c2Cl)O', 'CCCCNCCc1ccc(c(c1)O)O', 'CNCCc1ccc(c(c1)O)O', 'CCCCN(C(Cc1ccc(c(c1)O)O)CC=CC)C'} -->

<!-- short not missing vis -->
<!-- {'CNCCc1ccc(c(c1)O)O', 'OC1C=CC2C34C1Oc1c4c(CC2N(CC3)C)ccc1O', 'Oc1ccc(cc1O)CCNCCc1ccccc1', 'CCCCN(C(Cc1ccc(c(c1)O)O)CC=CC)C', 'CN1CCc2c3C1Cc1ccc(c(c1c3ccc2)O)O', 'CCNCCc1ccc(c(c1)O)O', 'CNCC(c1ccc(c(c1)O)O)O', 'CCCCNCCc1ccc(c(c1)O)O', 'Oc1ccc(cc1)C1CNCCc2c1cc(O)c(c2Cl)O'} -->

<!-- long tranclo7 -->
<!-- {'CN1CCc2c3C1Cc1ccc(c(c1c3ccc2)O)O', 'NCCc1ccccc1CC', 'NCCc1ccc(cc1C(CC=CCO)C)O', 'Oc1ccc(cc1)C1CNCCc2c1cc(O)c(c2Cl)O', 'Oc1ccc(cc1O)CCNCCc1ccccc1', 'NCCc1ccccc1', 'CNCCc1ccc(c(c1)O)O', 'CCc1ccccc1', 'CCCCNCCc1ccc(c(c1)O)O', 'CNCC(c1ccc(c(c1)O)O)O', 'CCCCN(C(Cc1ccc(c(c1)O)O)CC=CC)C', 'NCCc1ccc(cc1)O', 'OC1C=CC2C34C1Oc1c4c(CC2N(CC3)C)ccc1O'} -->
