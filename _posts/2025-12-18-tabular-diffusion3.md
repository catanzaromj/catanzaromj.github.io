---
layout: post
title: "Tabular Diffusion in Practice: SDEdit and Conditioning"
date: 2025-12-18
description: Two techniques for steering a trained diffusion model toward specific outputs without retraining it.
tags: [diffusion-models, generative-models, tabular-data, machine-learning]
categories: [ml]
---

This post continues from [part two]({% post_url 2025-09-13-tabular-diffusion2 %}), which covered
variance schedules, time embeddings, EMA, and classifier guidance. Here I want to focus on two
techniques that let you get more out of a model you have already trained: SDEdit for targeted
sample modification, and conditioning for steering generation toward specific properties.

## SDEdit for targeted sample modification

Once you have a trained diffusion model, generating samples from pure noise is only one option. 
Given an existing valid sample, can we produce a nearby sample
with slightly different properties? This is exactly what
[SDEdit](https://arxiv.org/abs/2108.01073) (Meng et al., 2021) enables.

The idea is straightforward. Rather than starting from $$x_T \sim \mathcal{N}(0, I)$$, take an existing
sample $$x_0$$, add noise up to some intermediate timestep $$t^* < T$$, and run the reverse
process from there. Formally,

$$
x_{t^*} = \sqrt{\bar{\alpha}_{t^*}}\, x_0 + \sqrt{1 - \bar{\alpha}_{t^*}}\, \epsilon,
\qquad \epsilon \sim \mathcal{N}(0, I)
$$

then denoise from $$t^*$$ back to $$0$$ as usual. The choice of $$t^*$$ controls the
fidelity-diversity tradeoff: a small $$t^*$$ produces outputs close to the original,
while a large $$t^*$$ allows the model more freedom to deviate.

For our tabular setting this is particularly useful. We have a library of known-valid samples
from the training set. Using SDEdit we can take one of these, noise it slightly, and denoise
it back, producing a new sample that respects the overall data distribution without starting
from scratch.

### Combining SDEdit with auxiliary guidance

The more interesting case is using SDEdit together with our auxiliary guidance functions.
During the reverse process from $$t^*$$, we apply the same guided update as in standard
sampling:

$$
\tilde{\mu}_\theta(x_t, t) = \mu_\theta(x_t, t) + s \cdot \Sigma_\theta(x_t, t) \nabla_{x_t} \log p(y \mid x_t) -
\sum_i \lambda_i \nabla_{x_t} f_{\phi_i}(x_t)
$$

By tuning the $$\lambda_i$$ during the SDEdit reverse pass, we can steer the output toward
specific auxiliary properties. We can try to nudge a sample to have a higher value of a
particular predicted quantity, while keeping it grounded in a valid starting point. This
gives a practical tool for targeted design: instead of generating a thousand random samples
and filtering, you can take a known-good sample and walk it toward a desired region of the
data manifold.

One subtlety we found important is that applying constant $$\lambda_i$$ throughout the entire
reverse pass tends to over-steer the sample. The guidance signal is strongest and most
meaningful at intermediate timesteps, where the sample has enough structure for the auxiliary
network gradients to be informative. Near $$t = 0$$, the sample is nearly clean and small
gradient nudges can introduce artifacts or push it outside the valid region.

To address this, we scheduled the $$\lambda_i$$ to decay toward zero as $$t \to 0$$. A
simple linear decay works well:

$$
\lambda_i(t) = \lambda_i \cdot \frac{t}{t^*}
$$

so that guidance is at full strength at the start of the reverse pass and switched off
entirely at the final step. This lets the model's own learned denoising close out the
sample cleanly, without the auxiliary functions fighting against it at the last moment.

## Conditioning

Classifier guidance (covered in [part two]({% post_url 2025-09-13-tabular-diffusion2 %})) steers
sampling at inference time using the gradient of an external classifier. Conditioning instead
bakes the desired properties directly into the diffusion model during training,
so that the model learns to generate samples that respect them from the start.

Our conditioning signal consisted of 6 scalar labels. These were a mix of guidance function values
and input parameters
that we wanted to be able to specify at generation time. To handle the case where only some labels are
known, we augmented the condition vector with a binary mask of the same length. The full
conditioning input was therefore a vector of dimension 12:

$$
c = [v_1, \ldots, v_6,\; m_1, \ldots, m_6], \qquad m_i \in \{0, 1\}
$$

where $$m_i = 1$$ indicates that label $$v_i$$ is active and should be respected, and
$$m_i = 0$$ indicates that no constraint is placed on that dimension. During training, we
randomly zeroed out subsets of the mask, which taught the model to generate valid samples
whether a full set of conditions, a partial set, or no conditions at all were provided.
This is the core idea behind classifier-free guidance, but applied per-label rather than
all-or-nothing.

The conditioning vector $$c$$ was injected into the denoising network alongside the time
embedding, so at each reverse step the model sees both where it is in the diffusion process
and what properties the final sample should have.

At inference, you specify whichever labels matter for a given run and set the corresponding
mask entries to 1, leaving the rest at 0. The model generates freely along unconstrained
dimensions while respecting the active labels. This is particularly useful in our setting
because the 6 quantities of interest were not always all specified.  Only 2 or 3 labels
were typically relevant for a given design goal.

## Takeaways

SDEdit and conditioning solve related but distinct problems. One way to think
about them is as follows. SDEdit is about the starting point of the diffusion process.
Rather than generating from pure noise, you begin from a known-good sample and let the reverse
process explore nearby. Conditioning is about the endpoint constraints. Conditioning allows
the model to learn to generate samples that satisfy specified properties regardless of where it starts.

Used together, they are complementary. You can take a known-valid sample, noise it to $$t^*$$,
and run a conditioned reverse pass. This grounds the output in a realistic starting point while
steering it toward a desired region of the design space.

A few things worth carrying forward:

- Randomly dropping label subsets during training means one
  model covers all possible partially-specified queries at inference. Separate models for each
  query pattern would be impractical.
- Whether using SDEdit or standard sampling with auxiliary
  functions, decaying $$\lambda_i$$ toward zero near $$t = 0$$ consistently improved output
  quality. Guidance is most useful when the sample is still rough; let the model finish on its
  own terms.
- During conditioned generation you can still apply
  auxiliary guidance functions on top. The conditioning shapes the overall distribution; the
  guidance nudges specific properties within it. They operate at different levels and do not
  cancel each other out.
