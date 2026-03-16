---
layout: page
published: true
title: Tabular Diffusion Models
description: Diffusion models with auxiliary networks to guide sampling over structured tabular data.
img: assets/img/tabular_diffusion_thumb.png
importance: 2
category: ml
related_publications: false
---

Denoising diffusion models have become the dominant paradigm for image and audio generation, but adapting them to tabular data requires rethinking nearly every design choice. Images and audio are continuous and locally correlated — properties that fit naturally with Gaussian noise processes. Tabular data breaks both assumptions: columns can be continuous, categorical, or ordinal, marginal distributions are often non-Gaussian or multimodal, and there is no natural notion of proximity across features.

This project describes our approach to training a diffusion model on a dataset
of roughly 50,000 tabular records, each consisting of 21 numerical features
subject to approximately 30 inter-column constraints. The goal was to generate
synthetic records that are statistically realistic and structurally valid while
satisfying the same constraints as real data.

## Approach

We treated all features as continuous after quantile normalization, which puts every column on a comparable scale with a near-uniform marginal. Rather than modifying the noise process to handle mixed types, we focused on two complementary mechanisms: **guidance at inference** to steer the denoising trajectory toward valid outputs, and **EMA weights** to stabilize the model and improve sample quality.

## Variance schedule

We compared linear, quadratic, and cosine noise schedules. The cosine schedule is often preferred because it preserves signal longer before dropping off, but in our case the linear schedule performed best. We attribute this partly to quantile normalization, which removes the distributional mismatch that cosine scheduling is often designed to compensate for.

## Time embeddings

The denoising network receives the current timestep $$t$$ as a sinusoidal embedding of dimension 128, analogous to positional encodings in transformers. The embedding is projected and injected into the network with a residual connection at both the input and output stages, giving the network a persistent signal about how noisy its input is.

## Exponential moving average

During training we maintained a shadow copy of the model weights via
exponential moving average (EMA) with a decay rate of 0.999. EMA weights were
used exclusively at inference. Compared to the raw training weights, EMA
samples were valid roughly **30% more often** and qualitatively more realistic.
Compared to the EMA samples, the non-EMA samples produced many more out-of-range or constraint-violating rows.

## Guidance

We used classifier guidance to steer sampling toward valid outputs. A validity classifier $$p(y \mid x_t)$$ was trained on noisy samples to predict whether a record would be valid after full denoising. At each reverse step, its gradient nudges the predicted mean:

$$
\tilde{\mu}_\theta(x_t, t) = \mu_\theta(x_t, t) + s \cdot \Sigma_\theta(x_t, t) \nabla_{x_t} \log p(y \mid x_t)
$$

In addition to the validity classifier, we trained over 30 auxiliary networks (one for each quantity of interest) and used their gradients as optional additional guidance signals during sampling.

## SDEdit

Once a model is trained, SDEdit offers a way to modify an existing sample
rather than generating from scratch. A known-valid record is noised forward to
some intermediate timestep $$t^* < T=1000$$, then denoised back to $$t=0$$. Smaller
$$t^*$$ keeps the output close to the original; larger $$t^*$$ allows more
deviation. Combined with auxiliary guidance during the reverse pass, SDEdit
becomes a targeted design tool: _instead of generating many random samples and
filtering, we can take a known-good record and modify it towards a desired region
of the data manifold_. We found it important to decay the guidance weights
$$\lambda_i$$ linearly to zero as $$t \to 0$$, letting the model's own
denoising close out the sample cleanly.

## Conditioning

Guidance steers sampling at inference time without modifying the model.
Conditioning bakes the desired properties into the model during training. We
conditioned on 6 scalar labels using a binary mask of the same length, so the
full conditioning vector had dimension 12. During training, random subsets of
the mask were zeroed out, which taught the model to generate valid samples
regardless of whether a full set of labels, a partial set, or no labels were
provided. At inference, only the mask entries for the relevant quantities are
set to 1; the model generates freely along the rest. It is important to realize
that conditioning and auxiliary
guidance are complementary procedures. Conditioning shapes the overall distribution,
while guidance nudges specific properties within it.

## Evaluation

Evaluating generative models for tabular data is an open problem. Common
proxies include train-on-synthetic/test-on-real (TSTR), statistical fidelity
metrics (marginal distributions, pairwise correlations), and privacy metrics
that measure how easily a real training record can be recovered from a
generated one. In our case the structural constraints gave us an additional
concrete signal--we could tell immediately if a generated sample was valid or not
by verifying that it satisfied all of the constraints. In general, no
single metric is sufficient and they often conflict, but the validity rate was
the most actionable metric during our development.

## Blog posts

Each of these aspects is described in more detail in the following posts:

- [Diffusion Models for Tabular Data]({% post_url 2025-05-06-tabular-diffusion %}): motivation, the diffusion framework, strategies for mixed types, and evaluation challenges.
- [Tabular Diffusion in Practice]({% post_url 2025-09-13-tabular-diffusion2 %}): variance schedules, time embeddings, EMA, and inference-time guidance.
- [Tabular Diffusion in Practice: SDEdit and Conditioning]({% post_url 2025-12-18-tabular-diffusion3 %}): two techniques for steering a trained diffusion model toward specific outputs without retraining it.
