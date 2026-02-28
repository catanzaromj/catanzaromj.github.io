---
layout: page
title: Multiparameter Persistence
description: Geometric models for multiparameter persistent homology via generic families of Morse functions.
img: assets/img/multip_bar.png
importance: 6
category: tda
related_publications: true
---

{% capture fig_caption %}
A higher-dimensional analogue of the barcode for multiparameter persistence. Degree 0 features are shown in blue and degree 1 features shown in red. Taken
from {% cite bubenik_multiparameter_2021 %}.
{% endcapture %}

<div class="text-center">
{% include figure.liquid path="assets/img/multip_bar.png" caption=fig_caption
zoomable=true %}
</div>

Standard persistent homology tracks topological features across a single scale
parameter. This is typically visualized by growning the radii of balls around
datapoints, or increasing the height of a sub-level set, and tracking topological
features as a function of such. This one-parameter
theory is well understood from a variety of mathematical viewpoints including
representation theory, graph theory, and from computational perspectives. 
The output in this simple case is a barcode, a collection of
intervals that is provably a complete invariant of the filtration.

We often want to understand real data from a collection of perspectives, meaning
there are often multiple natural parameters we'd like to vary simultaneously.  A
function on a manifold may have both a height and a density filtration; or a
dataset of images might be filtered by both intensity and gradient; or we might
want to filter the same manifold by multiple directions simultaneously. 
**Multiparameter persistence** generalizes the theory of persistence to these
settings, but th
algebra becomes significantly harder. Unlike the one-parameter case, there is no
complete discrete invariant analogous to the barcode. From a representation theoretic
perspective, the structure of
multiparameter persistence modules is wild in general.

This project develops geometric models to study multiparameter persistence using
tools from Morse theory and geometric topology. One classical source of
one-parameter persistence is the sublevel-set filtration of a single Morse
function on a manifold. The natural generalization is to consider *generic
families of Morse functions* parameterized by a manifold. Thus, as you move through
the parameter space, the Morse function changes, and the associated persistence
changes with it. Together with Peter Bubenik, we use this setup in {% cite
bubenik_multiparameter_2021 %} to construct and partially decompose
multiparameter persistence modules, obtaining structure analogous to a barcode
in several cases.
