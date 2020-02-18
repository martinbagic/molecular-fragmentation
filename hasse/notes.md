# UE Cheminf

<!-- ## task
- decompose a collection of molecules using MCS
- partial order is sub-/superstructure -->
## workflow
1. turn inputs to graphs
1. find modular graph product using **?**
1. find maximum clique using **cliquer**
1. insert into poset
 
## terminology
- modular graph product
- maximum common subgraph (MCS)
- partial order (bin rel: As, R, T), substructure inclusion
- Hasse diagram
- [Bron-Kerbosch alg](http://www.dcs.gla.ac.uk/~pat/jchoco/clique/enumeration/report.pdf)

## idea
- maximum common induced subgraph of G and H = maximum clique of modular product of G and H
- use cliquer to find maximum clique

## resources
### links
- [MCS](https://tripod.nih.gov/?p=189) 
- [cliquer](https://users.aalto.fi/~pat/cliquer/cliquer.pdf)
- [publication repo](https://github.com/peter-lind/hasse-manager)
- [indigo](https://github.com/epam/Indigo) 
- [SWIG](http://www.swig.org/tutorial.html) 
- Flamm presentations: [1](https://www.tbi.univie.ac.at/~xtof/Leere/269019/exercise01.pdf), [2](https://www.tbi.univie.ac.at/~xtof/Leere/270038/ue02.pdf)

### commands
- obabel -:"C12C(CCC1)CCCC2" -o svg > mol.svg