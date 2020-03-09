# Molecular Fragmentation by MCS

In chemistry, molecular structure dictates molecular function. Thus, recognizing structural similarities between molecules as well as recognizing the presence and distinctiveness of structural motifs is of particular interest.

This project attempts to generate molecular fragments by decomposing an initial set of molecules using the [maximum common subgraph](#definitions) (MCS). Subsequently, it organizes the resulting fragments in a hierarchy determined by the implicit partial order.

> Maximum common subgraph is the [maximum clique](#definitions) of a [modular graph product](#definitions).

<!-- ## Flowchart -->

## Get started (Linux)
To get started, run the following commands:
```
. get_started.sh
```

This bash script will install a Python virtual environment `.env`, activate it, and install the necessary Python libraries (`PyYAML` and `graphviz`).

## Usage example

The project provides numerous instances for different partial orders:

- greatest common divisor `gcd1` `gcd2`
- longest substring `substr1`
- inclusion of letters `common1`
- maximum common subgraph `mcs1` `mcs2` `mcs3` `mcs4` `mcs5`


To run the first example and plot the results, simply run:

```
python3 molfrag/molfrag.py -t gcd1
```

If you wish to use the precalculated data for the provided examples, simply include the -r flag:
```
python3 molfrag/molfrag.py -rt gcd1
```

To run custom examples, add data to the `molfrag/input.yaml`:
1. Specify the root nodes in the _definitions_ section.
2. Specify instance attributes in the _instances_ section.
   - _mode_ = partial order
   - _roots_ = link to root nodes list
   - _canonicalize_ = bool flag, whether to canonicalize (set to _true_ only for _mcs_)

## Limitations and issues

### _Cliquer_ considers **disconnected** subgraphs.

Disconnected subgraphs are not relevant in this context (we are not interested in matching separated molecular fragments). In order to tackle this problem, `mcs` was modified to return all (well, <a id="a1">[not _all_ but many](#all-solutions)</a>) solutions, not just one. This increases our chance of finding connected subgraphs, but we will still need to handle the disconnected subgraphs. There are three different scenarios:

1. **_Cliquer_ returns only connected subgraphs.** In this case, we do not have to do anything.
2. **_Cliquer_ returns both connected and disconnected subgraphs.** In this case, we simply remove the disconnected subgraphs.
3. **_Cliquer_ returns only disconnected subgraphs.** This is _the problematic_ case. There are essentially two fundamentally different handling approaches:
   1. **Discard all the subgraphs.**
      > &minus; losing a big part of the lattice; however; this may be offset by having another molecule happen to be a child of both, thus replacing the empty subgraph<br> > &plus; not inserting non-maximum common subgraphs into the lattice
   2. **Extract fragments from subgraphs.** This is done by splitting the subgraphs at the dot sign (`.`), counting cardinality of all fragments, finding greatest cardinality, and finally choosing the fragments with that cardinality.
      > &plus; not losing a big part of the lattice<br> > &minus; inserting non-maximum common subgraphs into the lattice; this is obviously an issue because it is contrary to the task definition itself, but also because it becomes order-dependent, i.e. `mcs(A,mcs(B,C))` &ne; `mcs(mcs(A,B),C)`, and this can cause the lattice to explode

The first two scenarios are not problematic and handled as described. The third scenario is problematic and is handled in a hybrid way:

1. If both `A` and `B` in `mcs(A,B)` are root molecules (the one specified in the input) then we use the 2nd approach and extract one randomly chosen maximum fragment.
2. Otherwise, we will discard all subgraphs.

The choice is such because running `mcs` on two big molecules tends to return only disconnected graphs (because there is a lot of room for micro&#8209;optimization, i.e. finding small fragments). This means that we should count with not finding connected graphs high up in the lattice. Thus, I am taking a fragment to salvage the lattice. However, once either or both of the molecules is not a root molecule, the importance of salvaging the resulting part of the lattice is lower but also because the molecules are smaller, we expect fewer instances of only getting disconnected graphs.

<h3 id="all-solutions">

`mcs` does not return all the solutions.

</h3>

Currently, the maximum number of returned solutions is 1024, as is specified in the `mcs.cpp` in the line 
```
int max_cliques = 1024
```

This limit is important for tractability reasons.

As long as at least one solution is a connected subgraph, this limit is benign and will simply result in a smaller output lattice. However, if there are many disconnected subgraph solutions, it could happen that no connected subgraph solution is returned, which further causes the issues described above.

<sub>
<sup>

Note that an additional condition (`i < max_cliques`) has been added to `mcs.cpp` for-loop in line 249.
This is because it is possible that `n` is greater than `max_cliques`, but letting `i` grow bigger than `max_cliques` leads to a _Segmentation fault (core dumped)_ error.

</sup>
</sub>

## Potential improvements

1. **Implement C++/Python binding.**
   Relevant technologies are [indigo](https://github.com/epam/Indigo), [SWIG](http://www.swig.org/tutorial.html), and [pybind11](https://pybind11.readthedocs.io/en/stable/basics.html).
2. **Exclude disconnected subgraphs from _cliquer_**.
3. **Lift clique limit in _cliquer_**.
   Currently, the issue lies in the fact that before calling the `clique_unweighted_find_all()`, we need to define the clique list and its max number:
   <br>`int max_cliques = 1024`,
   <br>`set_t s[max_cliques]`, and <br>`clique_default_options->clique_list_length = max_cliques`.
   <br> In order to lift the limit, we should dive deeper in the _cliquer_ code &ndash; probably starting with the function `store_clique()` in `cliquer.c`.
4. **Call _obabel_ directly from Python.**

## Design choices

- Fragments with less than 7 atoms are ignored (defined in `Canonicalizer.min_length = 7`)

## Definitions

- [**maximum common induced subgraph**](https://en.wikipedia.org/wiki/Maximum_common_subgraph) &ndash; a graph that is an induced subgraph of two given graphs and has as many vertices as possible
- [**maximum common edge subgraph**](https://en.wikipedia.org/wiki/Maximum_common_edge_subgraph) &ndash; a graph that is a subgraph of two given graphs and has as many edges as possible
- [**isomorphic graphs**](https://en.wikipedia.org/wiki/Graph_isomorphism) &ndash; graphs for which there is a mapping of vertices that preserves adjacency
- [**connected graph** (undirected)](<https://en.wikipedia.org/wiki/Connectivity_(graph_theory)#Connected_graph>) &ndash; graph with at least one vertex and with a path between any pair of vertices
- [**disconnected graph** (undirected)](<https://en.wikipedia.org/wiki/Connectivity_(graph_theory)#Connected_graph>) &ndash; graph that is not connected
- [**modular product of graphs** A and B](https://en.wikipedia.org/wiki/Modular_product_of_graphs) &ndash; graph whose vertex set is the cartesian product of vertex sets of A and B and edge set contains all vertex pairs of vertices that are either adjacent in both A and B or not adjacent in neither A nor B
- [**clique**](<https://en.wikipedia.org/wiki/Clique_(graph_theory)>) &ndash; a subset of vertices of an undirected graph such that every two distinct vertices in the clique are adjacent

## Resources

- [Christoph Flamm](https://ufind.univie.ac.at/en/person.html?id=17324)'s presentations: [1](https://www.tbi.univie.ac.at/~xtof/Leere/269019/exercise01.pdf), [2](https://www.tbi.univie.ac.at/~xtof/Leere/270038/ue02.pdf)
- maximum common subgraph algorithm ([mcs](https://tripod.nih.gov/?p=189))
- maximum clique algorithm ([cliquer](https://users.aalto.fi/~pat/cliquer/cliquer.pdf))
- Peter Lind's [publication](https://www.ncbi.nlm.nih.gov/pubmed/24437465) "Construction and use of fragment-augmented molecular Hasse diagrams" and [publication repo](https://github.com/peter-lind/hasse-manager)

## Meta

Martin Bagic &ndash; https://github.com/martinbagic<br>
This project was done in the domain of a [university course](https://ufind.univie.ac.at/en/course.html?lv=270086&semester=2019W) led by [Christoph Flamm](https://ufind.univie.ac.at/en/person.html?id=17324).
