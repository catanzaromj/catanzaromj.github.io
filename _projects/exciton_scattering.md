---
layout: page
title: Exciton Scattering
description: Applying algebraic topology to count quasi-particle excitations in molecular systems.
img: assets/img/exciton_pair.png
importance: 5
category: algebraic topology
related_publications: true
---

When light strikes a molecule, it can create an exciton.
Excitons are naturally occurring quasi-particles associated with the conversion of light to energy (e.g. photosynthesis). We think of these as bound electron-hole pairs
that carry energy without carrying charge. Excitons are central to photosynthesis,
organic semiconductors, and photovoltaic devices, so counting how many distinct
excitations a system can support is a question of real physical interest.

Our work applies algebraic topology to study and in particular, to count, the
number of such excitations in certain systems.  The exciton counting problem has
a clean topological formulation in terms of intersection theory. The electronic
Hamiltonian of a molecular system traces out a curve in the space of $$n \times
n$$ unitary matrices $$U(n)$$. Excitons correspond to intersections of this
curve with a particular stratified subspace--the set of matrices with at least
one eigenvalue equal to one. Each intersection carries a multiplicity, and the
total exciton count is a *topological winding number* computable via an
index-like theorem. Because the answer depends only on the topology of the curve
and the stratification, it is robust to small perturbations of the system.

The mathematical intersection theory for curves in stratified subspaces of $$U(n)$$ is developed in
{% cite catanzaro_exciton_2017 %}. The theory was applied to conjugated molecules in
{% cite li_excited-state_2014 %} and to organic semiconductor systems in
{% cite catanzaro_counting_2015 %}.
