---
layout: page
title: TDA applied to fMRI
description: Using persistent homology on cubical complexes to study task-modulated brain activity.
img: assets/img/acc.png
importance: 7
category: tda
related_publications: true
---

Functional MRI (fMRI) measures blood-oxygen-level-dependent (BOLD) signals across the
brain over time, producing a 4D dataset: three spatial dimensions of voxels plus time.
Standard analyses often reduce this to summary statistics or connectivity matrices, which
can miss the fine-grained spatial structure of how regions activate.

This project applies topological data analysis to fMRI data using the natural geometry
that the voxel grid provides. Each brain region of interest is modeled as a
*cubical complex*, a topological space built from cubes rather than triangles. Cubical complexes are amenable to efficient homological calculations and 
are well-adapted to the rectangular grid of voxels. The fMRI BOLD signal then induces a
filtration on this complex: at each threshold value, we include all voxels whose signal
exceeds that value. Running persistent homology on this filtration yields a persistence
diagram encoding how clusters, loops, and voids in the activation pattern appear and
disappear across signal intensities.

The main application is the anterior cingulate cortex (ACC), a brain region involved
in cognitive control and task switching. The question is whether topological features of
ACC activation systematically differ between task conditions and is something connectivity-based
methods may not capture. A general mathematical framework for this approach is laid out in
{% cite salch_mathematics_2021 %}, and results applying it to the ACC are in
{% cite catanzaro2023topological %}. This work is joint with Vaibhav Diwadkar, Sam Rizzo,
Peter Bubenik, Andrew Salch, Adam Regalski, Hassan Abdallah, and Raviteja Suryadevara.
