# UE Cheminf

## tasks 27 Feb 2020
- [ ] clean up mcs modifications
- [ ] cyclic examples
- [ ] writeup
- [ ] consider fragmenting the disconnected graphs (at least for the root nodes)

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
- run mcs `mcs/mcs s1.smi s2.smi` or `mcs/mcs CNCC(C1=CC(=C(C=C1)O)O)O CN(CCc1ccc(c(c1C)O)O)C`
