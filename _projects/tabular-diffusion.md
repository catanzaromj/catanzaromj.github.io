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

This project describes our approach to training a diffusion model on a dataset of roughly 50,000 tabular records, each consisting of 21 numerical features subject to approximately 30 inter-column constraints. The goal was to generate synthetic records that are statistically realistic and structurally valid — satisfying the same constraints as real data.

## Approach

We treated all features as continuous after quantile normalization, which puts every column on a comparable scale with a near-uniform marginal. Rather than modifying the noise process to handle mixed types, we focused on two complementary mechanisms: **guidance at inference** to steer the denoising trajectory toward valid outputs, and **EMA weights** to stabilize the model and improve sample quality.

## Variance schedule

We compared linear, quadratic, and cosine noise schedules. The cosine schedule is often preferred because it preserves signal longer before dropping off, but in our case the linear schedule performed best. We attribute this partly to quantile normalization, which removes the distributional mismatch that cosine scheduling is often designed to compensate for.

## Time embeddings

The denoising network receives the current timestep $$t$$ as a sinusoidal embedding of dimension 128, analogous to positional encodings in transformers. The embedding is projected and injected into the network with a residual connection at both the input and output stages, giving the network a persistent signal about how noisy its input is.

## Exponential moving average

During training we maintained a shadow copy of the model weights via exponential moving average (EMA) with a decay rate of 0.999. EMA weights were used exclusively at inference. Compared to the raw training weights, EMA samples were valid roughly **30% more often** and qualitatively more realistic — the non-EMA samples produced more out-of-range or constraint-violating rows.

## Guidance

We used classifier guidance to steer sampling toward valid outputs. A validity classifier $$p(y \mid x_t)$$ was trained on noisy samples to predict whether a record would be valid after full denoising. At each reverse step, its gradient nudges the predicted mean:

$$
\tilde{\mu}_\theta(x_t, t) = \mu_\theta(x_t, t) + s \cdot \Sigma_\theta(x_t, t) \nabla_{x_t} \log p(y \mid x_t)
$$

In addition to the validity classifier, we trained over 30 auxiliary networks — one per quantity of interest — and used their gradients as optional additional guidance signals during sampling.

## Blog posts

- [Diffusion Models for Tabular Data]({% post_url 2025-05-06-tabular-diffusion %}) — motivation, the diffusion framework, strategies for mixed types, and evaluation challenges.
- [Tabular Diffusion in Practice]({% post_url 2025-09-13-tabular-diffusion2 %}) — variance schedules, time embeddings, EMA, and inference-time guidance.
- [Tabular Diffusion in Practice: SDEdit and Conditioning]({% post_url 2025-12-18-tabular-diffusion3 %}) — two techniques for steering a trained diffusion model toward specific outputs without retraining it.
