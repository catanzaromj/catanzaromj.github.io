---
layout: page
title: Stochastic Currents
description: A higher-dimensional generalization of electrical current, studied via algebraic topology and stochastic processes.
img: assets/img/torustest.png
importance: 8
category: algebraic topology
related_publications: true
---

In a graph, an **electrical current** is a flow along edges that satisfies
Kirchhoff's laws. Think of an electron moving through a wire.
The flow can be deterministic or stochastic, and so random walks on graphs
generate currents. In this case, the current encodes topological properties of the
graph and can be studied under various dynamical limits. We think of current as
a statistical object encoding how much net flow passes through each edge. This
relationship between probability and topology is classical and well understood
in dimension one.

My thesis generalizes this to **higher dimensions** {% cite
catanzaro_topological_2016 %}. Instead of measuring flow along edges (1-dimensional objects) in a
graph, we consider flow along higher-dimensional sub-objects, like embedded surfaces or volumes. We study these questions in both CW complexes and smooth manifolds.
In either case, A stochastic process can be defined, whether it is a Markov chain or a stochastic
differential equation. Instead of thinking about points moving around the graph, we
again generalize to moving higher-dimensional or extended objects around. These objects moving similarly generate a **higher current**, and
the central question is: what topological information does this current carry?

The project splits into two parallel settings and the tools involved vary for each:

- **Discrete case** (CW complexes with Markov processes): Under dynamical limits on
  the Markov process, the motion of the embedded object tends to be supported along
  _higher spanning trees_, the analog of a spanning tree on a graph. These higher
  spanning trees can be enumerated using **Reidemeister torsion**,
  an invariant from Algebraic K-theory.
  The combinatorial complexity here is much richer than the graph case and is
  analyzed in {% cite catanzaro_kirchhoffs_2015 %}.

- **Continuous case** (smooth manifolds with stochastic vector fields): The analogous
  invariant is **Ray-Singer torsion**, an analytic object defined via zeta-regularized
  determinants of Laplacians. The two settings are connected by Witten-style Laplacian
  deformations, which relate the discrete and analytic torsions.

There is an interactive version of this higher dimensional analogue of random
walks on a CW decomposition of a torus here: [random torus walk](/assets/html/Torus_walk_slider.html)

Beyond topology, there are also statistical mechanics implications of these
processes. Quantization of currents and their relationship
to nonequilibrium steady states are explored in {% cite catanzaro_stochastic_2016-1 %}
and {% cite catanzaro_stochastic_2016 %}. A mathematical generalization to a broader class
of hypercurrents is pursued in {% cite catanzaro_hypercurrents_2020 %}.

<div class="text-center">
{% include figure.liquid path="assets/img/torustest.png" caption="An initial cycle 
(shown on the right side) within a CW decomposition of a torus. The evolution of this
initial condition is also shown later during evolution (back left). 
While the evolved cycle may become more complicated, it is always homologous to the initial cycle throughout the process." zoomable=true width="60%" %}
</div>
