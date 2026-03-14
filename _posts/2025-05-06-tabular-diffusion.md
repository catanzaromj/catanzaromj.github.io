---
layout: post
title: Diffusion Models for Tabular Data
date: 2025-05-06
description: Why tabular data is a hard target for generative models, and how diffusion models are being adapted to handle it.
tags: [diffusion-models, generative-models, tabular-data, machine-learning]
categories: [ml]
---

Diffusion models have become the dominant paradigm for image and audio generation.
Extending them to the tabular data of spreadsheets and databases is less straightforward, and the reasons why are worth understanding.

## What makes tabular data different

There are a variety of reasons why image and audio data is significantly different than tabular data.
Images and audio data tend to be continuous and locally correlated. Nearby pixels tend to have similar
values, and the sound of a song tends to build and fall fairly continuously throughout a piece of music.
Diffusion models are based on a Gaussian noise process and so these data types tend to fit naturally
with this mathematical setup.
Unfortunately, tabular data breaks both assumptions.

A typical table might have a mix of continuous features (like age, income, temperature),
categorical features (like country, product type, diagnosis code), and
ordinal (or count features) that live somewhere in between.
There is no natural notion of "nearby" across columns, and the marginal distributions of individual columns can be wildly non-Gaussian.
They can be heavy-tailed, multimodal, or discrete and of course, all of this can vary from column to column.

## The diffusion framework, briefly

A diffusion model (here we take standard de-noising diffusion) works by defining a forward process that gradually noises initial data $$x_0$$ with Gaussian noise over $$T$$ steps:

$$
q(x_t \mid x_{t-1}) = \mathcal{N}(x_t;\, \sqrt{1 - \beta_t}\, x_{t-1},\, \beta_t I)
$$

The noise serves to corrupt the data over these time steps, turning your training data into pure noise.
The _variance schedule_ $$\{\beta_t\} = \beta_0, \beta_1, \beta_2, \ldots, \beta_T$$ controls
the statistics of the noise as a function of $$t$$. Maybe we'll explore this parameter in a future post but for now,
we think of it as the amount of noise added at each step.

A diffusion model is a neural network that learns to **reverse** this process. The network learns to predict $$x_{t-1}$$ given $$x_t$$.

$$
p_\theta(x_{t-1} \mid x_t) = \mathcal{N}(x_{t-1};\, \mu_\theta(x_t, t),\, \Sigma_\theta(x_t, t))
$$

where $$\mu_\theta$$ and $$\Sigma_\theta$$ are the mean and variance
predicted by the neural network. Again, maybe we'll dive into this
more in a future post, but for now, we view these as parameters
learned by the network to accurately predict the noise.

Again, this is worth saying: the network learns to predict the noise added each time step.
This is something that is easy to overlook, but important to remember. The network does not learn to generate new samples per se. It learns to
de-noise one data point at one time, into another at the next time.
During inference,
the network generates new instances of data by starting from pure (randomly generated) noise and denoising iteratively using the network.
During training, the network learns specific features and characteristics of the data to de-noise to.

The key requirement/assumption is that the noising process is tractable and that the data space is continuous and well-suited to Gaussian perturbations.
Tabular data satisfies neither cleanly.

## Approaches for handling mixed types

Several strategies have been explored:

1. Encode everything as continuous. Categorical variables can be embedded or one-hot encoded before diffusion, then decoded back post-sampling.
   The risk is that the model learns to sample in a space that doesn't respect category boundaries. I find this approach to be the least
   informed, but it does work in practice.

2. Score matching on a mixed space. You could do separate noise processes for continuous and discrete variables and then
   train a joint score function. This is more principled than option 1 but can be harder to train. There might not be a reason
   a priori to expect your data to split so nicely between continuous and discrete.

3. Auxiliary networks to guide sampling. Rather than modifying the noise process, one approach would be to add conditioning or
   a guidance network that steers the denoising trajectory toward valid, coherent outputs. This can be useful
   when tabular rows must satisfy structural constraints (e.g., clinical plausibility, valid configurations, etc). For
   the project I was involved with, this was the approach that we took.

## Why this is hard to evaluate

Evaluating generative models for tabular data is an open problem.
Even for generative imaging models, it is tough.
Image models can be assessed with FID or human judgment, but these may suffer from their own inherent biases or
may be too costly in practice.
For tabular data, common proxies include:

- Train on synthetic, test on real (TSTR). Train a downstream model on generated data, but then evaluate on real held-out data.
- Statistical fidelity. Compute marginal distributions, pairwise correlations, and higher-order statistics (again) on real vs. synthetic data.
- Privacy metrics. How easy is it to recover a real training record from a generated one?

None of these alone is sufficient, and they can conflict.

## My thoughts

Given the plentiful amounts of tabular data available, I find it surprising that more research isn't done on this. I know a picture is worth
1000 words, but there are tons of business opportunities for analyzing and re-creating such data. Images and audio often require curation and
labeling to be useful for training. Healthcare records, financial transactions, logistics data, etc. are already labeled. It seems like
there is a huge supply of interesting tabular data that exceeds what is being studied.

This last point also ties in to the privacy metrics point of view. A health clinic cannot release patient data just as a bank can't release
transaction data. A good generative model can help change that by allowing us to study data that can't be shared. Synthetic tabular data
generated from these sources has real and concrete use cases. This feels commercially real to me in a way that
image generation is only part of the time.

## Further reading

There are way better references for this material than this post. This is just meant to be my understanding of this at the
time of writing.

- [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) — Ho et al. (2020). The original paper this post is based on.
- [TabDDPM: Modelling Tabular Data with Diffusion Models](https://arxiv.org/abs/2209.15421) — Kotelnikov et al. (2023). A direct adaptation of DDPM to tabular data.
- [Score-Based Generative Modeling through Stochastic Differential Equations](https://arxiv.org/abs/2011.13456) — Song et al. (2020). The score matching perspective on diffusion.
- [Modeling Tabular Data using Conditional GAN](https://arxiv.org/abs/1907.00503) — Xu et al. (2019). A GAN-based baseline; useful for comparisons.
