---
layout: page
published: false
title: scikit-tda
description: Open-source maintainer of scikit-tda, a scikit-learn–compatible suite of TDA libraries.
img: assets/img/scikit_tda.png
importance: 4
category: tda
related_publications: false
---

[scikit-tda](https://scikit-tda.org) is an open-source ecosystem of Python libraries for
topological data analysis, designed to be interoperable with the scikit-learn ecosystem.
I contribute as a maintainer of the project, which spans several packages covering
different parts of the TDA pipeline.

## Packages

scikit-tda includes a variety of packages. Here are some of which I contribute to.

### [Ripser.py](https://ripser.scikit-tda.org)

A Python wrapper around the highly optimized [Ripser](https://github.com/Ripser/ripser)
C++ library for computing Vietoris–Rips persistent homology. Ripser.py is one of the
fastest persistent homology implementations available in Python. It supports
$$\mathbb{Z}/p$$ coefficients, sparse distance matrices, and computing homology in
arbitrary dimensions. The interface is simple — pass in a point cloud or distance matrix,
get back a list of persistence diagrams.

### [Persim](https://persim.scikit-tda.org)

A library for computing distances and similarities between persistence diagrams, and for
converting them into vector representations suitable for machine learning pipelines.
Persim implements the bottleneck distance, Wasserstein distance, and several
vectorization methods including persistence images and persistence landscapes.
It also includes utilities for visualizing diagrams.

### [Cechmate](https://cechmate.scikit-tda.org)

A library for constructing Čech and Delaunay filtrations from point cloud data in
arbitrary dimensions. While Ripser handles Vietoris–Rips filtrations,
Cechmate provides access to the geometrically tighter Čech complex — useful when
exact topological guarantees (via the nerve theorem) are needed and computational
cost is acceptable.

### [Tadasets](https://tadasets.scikit-tda.org)

A library of benchmark datasets for TDA research. It provides clean, parameterized
point cloud generators, including circles, tori, Swiss rolls, figure-eights, and more. These are useful
for testing pipelines and building intuition. Datasets can be sampled with controlled
noise levels, making it easy to study how robust a method is to perturbation.

### [KeplerMapper](https://kepler-mapper.scikit-tda.org)

An implementation of the Mapper algorithm, a method for producing
low-dimensional graph summaries of high-dimensional data. Mapper covers the data
with overlapping bins (defined by a filter function and a cover), clusters within
each bin, and connects clusters that share points across bins. The result is a
simplicial complex — typically visualized as a graph — that captures the topological
shape of the data at a coarser level than a persistence diagram.
KeplerMapper provides flexible filter functions, cover strategies, and built-in
visualization tools.

