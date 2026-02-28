---
layout: page
title: Persistence Landscapes of Fractals
description: Proving that the persistence landscape of a fractal is itself self-similar.
img: assets/img/PL_H0Cantor.png
importance: 9
category: tda
related_publications: true
---
<div class="text-center">
{% include figure.liquid path="assets/img/PL_H0Cantor.png" caption="Persistence landscapes of the first few iterations of the Cantor set IFS, converging to the landscape of the limit fractal." zoomable=true width="60%" %}
</div>

A persistence landscape is a vectorization of a persistence diagram as a
sequence of piecewise-linear functions. Unlike the diagram itself, landscapes
live in a Hilbert space, which means you can average them, compute norms, and
apply statistical tests. This makes them a powerful representation of topological
features for use in machine learning pipelines.

On the other hand, a fractal is a set defined as the fixed point of an iterated
function system (IFS). Start with any compact set, repeatedly apply a finite
collection of contracting maps, and the sequence converges to a self-similar
limit. The Cantor set, Sierpinski triangle, and Koch snowflake are classical
examples. Because these sets are self-similar by definition, a natural question
is whether their topological summaries inherit that self-similarity.

This project answers that question affirmatively for persistence landscapes. We
show that for an affine IFS, there is an affine transformation on the space of
persistence landscapes that intertwines the action of the IFS. In other words,
the persistence landscape of the fractal satisfies a fixed-point equation of its
own. Thus, in a precise sense, the persistence landscape of a fractal is a 
fractal in the space of landscapes.
Rather than computing the
landscape of the fractal directly (which would require an infinite iteration),
this result implies that we can compute the landscapes of finitely many iterations and use the
intertwining map to extrapolate to the limit.

This project is joint work with Lee Przybylski and Eric Weber in
{% cite catanzaro_persistence_2022 %}.
