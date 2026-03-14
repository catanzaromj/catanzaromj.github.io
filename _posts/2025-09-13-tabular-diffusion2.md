---
layout: post
title: "Tabular Diffusion in Practice: Variance Schedules, Time Embeddings, and EMA"
date: 2025-09-13
description: A closer look at the implementation choices that matter when training a diffusion model on tabular data.
tags: [diffusion-models, generative-models, tabular-data, machine-learning]
categories: [ml]
---

This post assumes familiarity with the basics of denoising diffusion.
If you want a primer first, see [my earlier post]({% post_url 2025-05-06-tabular-diffusion %}).

Here I want to get into the details that I found matter in practice.
These include how you schedule noise, how the network knows where it is in the diffusion process, how you stabilize training,
and how you steer samples toward valid outputs at inference time. Most of what I write here are things that I found out
through experience, not necessarily in literature.

## Our project

The project we were working on consisted of roughly 50,000 data points of tabular data. Each data point consisted
of 21 numerical values, some unitless and some with units on very different scales. There were roughly 30 equations
which constrained the values in each row. So while the first column may have had a range of possible values
of say $$-10$$ to $$10$$, there were additional constraints on it involving the other columns. While our
intention was not to have the de-noising model learn all of these relationships explicitly, it tended to do so
in practice.

## Variance schedules

The variance schedule $$\{\beta_t\}$$ determines how noise accumulates
over the forward process. I found this choice to have a huge impact on
how much signal remains at intermediate timesteps and how hard the reverse
process is to learn.

We'll get to the individual variance schedules below. But regardless of which
form of $$\beta_t$$ you choose, an important quantity to track is the _cumulative product_
$$\bar{\alpha}(t) = \prod_{s=1}^{t}(1 - \beta_s)$$.

With this quantity, you can re-write the forward process in closed form directly
from $$x_0$$:

$$
q(x_t \mid x_0) = \mathcal{N}(x_t;\sqrt{\bar{\alpha}_t}x_0,
(1 - \bar{\alpha}_t) I)
$$

Now the variance term with $$(1 - \bar{\alpha}_t)I$$ makes explicit the signal
to noise ratio at each time step. We see that $$\bar{\alpha}_t$$ is essentially
the signal retention over time. Plotting this as a function of $$t$$ can help
us tweak and understand the diffusion model's performance.

We considered linear, quadratic, and cosine based schedules for variance.
A linear schedule looks something like

$$
\beta_t = \beta_{\min} + \frac{t-1}{T-1}(\beta_{\max} - \beta_{\min})
$$

with typical values $$\beta_{\min} = 10^{-4}$$, $$\beta_{\max} =
0.02$$, and $$T = 1000$$. You can imagine what a quadratic schedule looks
like based on this.

A cosine schedule typically takes the form

$$
\bar{\alpha}_t = \frac{f(t)}{f(0)}, \qquad f(t) =
  \cos\left(\frac{t/T + s}{1 + s} \cdot \frac{\pi}{2}\right)^2
$$

where $$s \approx 0.008$$ is a small offset to keep $$\beta_t$$ from
being too small near $$t = 0$$. Then $$\beta_t = 1 - \bar{\alpha}_t / \bar{\alpha}_{t-1}$$.

Plotting $$\bar{\alpha}_t$$ makes the differences between these three cases concrete:

<div id="alpha-bar-plot" style="width:100%; height:400px;"></div>
{% raw %}
<script>
(function() {
  function renderPlot() {
    const T = 1000;
    const betaMin = 0.0001;
    const betaMax = 0.02;
    const s = 0.008;

    const t = Array.from({length: T}, (_, i) => i + 1);

    const betaLinear = t.map(i => betaMin + (i - 1) / (T - 1) * (betaMax - betaMin));
    const betaQuad = t.map(i => betaMin + Math.pow((i - 1) / (T - 1), 2) * (betaMax - betaMin));

    function alphaBar(betas) {
      const out = [];
      let prod = 1;
      for (const b of betas) { prod *= (1 - b); out.push(prod); }
      return out;
    }

    const f0 = Math.pow(Math.cos((s / (1 + s)) * Math.PI / 2), 2);
    const abCosine = t.map(i => {
      const fi = Math.pow(Math.cos(((i / T) + s) / (1 + s) * Math.PI / 2), 2);
      return fi / f0;
    });

    const traces = [
      { x: t, y: alphaBar(betaLinear), name: 'Linear', mode: 'lines' },
      { x: t, y: alphaBar(betaQuad), name: 'Quadratic', mode: 'lines' },
      { x: t, y: abCosine, name: 'Cosine', mode: 'lines' },
    ];

    const layout = {
      xaxis: { title: 't' },
      yaxis: { title: 'ᾱ_t (signal retention)', range: [0, 1] },
      legend: { orientation: 'h', y: -0.2 },
      margin: { t: 20 },
    };

    Plotly.newPlot('alpha-bar-plot', traces, layout, { responsive: true });

}

if (window.Plotly) {
renderPlot();
} else {
var s = document.createElement('script');
s.src = 'https://cdn.plot.ly/plotly-3.4.0.min.js';
s.onload = renderPlot;
document.head.appendChild(s);
}
})();
</script>
{% endraw %}

The cosine schedule keeps this higher for longer
before dropping off, which is why it tends to produce better
samples.

Our choice was motivated by our results — we tried lots of different variance schedules
and found linear worked best. We believe it was in part because we also quantile normalized our data.
This puts all the features on similar scales with similar distributions.
We determined "best" by lots of trial and error, and validating the outputs. Because
our tabular data was pretty constrained, it is very easy to determine what percentage
of outputs are actually "valid" in a concrete way.

## Time embeddings

The network needs to know which timestep $$t$$ it is operating at. In particular, the noise
behavior changes as a function of $$t$$ and so the network needs
to have some internal state of this. Denoising at $$t=1$$ with tiny
noise is very different than at $$t=1000$$ which is pure noise. The model needs to be able to
adapt its denoising behavior to how noisy the input is. This seems like a
trivial task--just give it the time parameter $$t$$ with the current noised
data point $$x_t$$. But neural networks work with respect to arrays and tensors,
not integers. So instead we embed time into the network via a sinusoidal embedding,
analogous to positional encodings in transformers.

First, we define the fundamental "frequencies"

$$
\omega_k = \exp!\left(-\frac{k \ln(P)}{\lfloor d/2 \rfloor}\right),
 \qquad k = 0, 1, \ldots, \lfloor d/2 \rfloor - 1
$$

Then we can define the formal embedding by concatenating cosine and sine halves

$$
\text{emb}(t) = \bigl[\cos(a_{t,0}),\ \ldots,\ \cos(a_{t,\lfloor
d/2\rfloor-1}),\ \sin(a_{t,0}),\ \ldots,\ \sin(a_{t,\lfloor
d/2\rfloor-1})\bigr]
$$

where the arguments are defined as (outer product of timesteps and frequencies):

$$
a_{t,k} = t \cdot \omega_k
$$

where $$d = 128$$, the embedding dimension and $$P$$ is the maximum period. Note
that our implementation puts cosine first, then sine, which is the opposite of
the transformer convention, but functionally equivalent.

The embedding is projected and injected into the network with a residual connection to inject
this information early on and again at the end. Our network was a


## Exponential moving average

During training, model weights are updated via gradient descent as usual. Exponential moving average (EMA) maintains a separate shadow copy of the weights as a running average:

$$
\theta_{\text{ema}} \leftarrow \mu \cdot \theta_{\text{ema}} + (1 - \mu) \cdot \theta
$$

where $$\mu$$ is the decay rate (typically 0.999 or 0.9999). The EMA weights are not used during training — only at inference.

The intuition is that the EMA weights average out gradient noise and tend to
sit in flatter regions of the loss landscape. For tabular data, where training
sets can be small relative to image benchmarks, this stabilization matters more
than you might expect.

We found a pretty dramatic difference between EMA and non-EMA samples. EMA samples tended to be valid almost 30% more of the time
compared to the non-EMA samples. They also tended to be more realistic, with the non-EMA samples being more wild.

## Guidance at inference

A guidance function steers the denoising trajectory toward outputs that satisfy some external criterion — without retraining the diffusion model. At each reverse step, the gradient of a guidance signal with respect to $$x_t$$ nudges the predicted mean:

$$
\tilde{\mu}_\theta(x_t, t) = \mu_\theta(x_t, t) + s \cdot \Sigma_\theta(x_t, t) \nabla_{x_t} \log p(y \mid x_t)
$$

where $$s$$ is a guidance scale and $$p(y \mid x_t)$$ scores how plausible or valid a noisy sample is. In practice,
we let $$s$$ be near 0.4, but of course this depends on the magnitude of the gradient. This parameter was
adjusted several times throughout, especially after re-training (see below).

In our set-up, we had a variety of guidance functions to choose from. First, we had a trained classifier that
predicted if a sample was valid or not (exactly the $$p$$ described above). But we could also augment the above
formula with other guidance functions. In addition, we trained over 30 neural networks to predict auxiliary quantities of
interest for each produced sample, trained on the initial training set. With these additional neural networks,
the mean for the sampling process becomes

$$
\tilde{\mu}_\theta(x_t, t) = \mu_\theta(x_t, t) + s \cdot \Sigma_\theta(x_t, t) \nabla_{x_t} \log p(y \mid x_t) -
\sum_i \lambda_i \nabla_{x_t} f_{\phi_i}(x_t)
$$

where $$f_{\phi_i}$$ are the auxiliary guidance functions. By tuning the $$\lambda_i$$ parameters, we can
modify the influence of each specific auxiliary function.

Initially, we trained the classifier $$p(y)$$ for predicting valid samples to near 100% accuracy on
the training set. As a result, the classifier was over confident and its gradient became
very unstable. In particular, the gradient term dominated the guided diffusion and biased the samples to
one of three local regions with the total sample space. We realized this mistake and
re-trained the classifier with:

- noisy data: we added noise to our training data during sampling
- label smoothing: we turned hard targets like `valid` and `invalid`, codified as `[1,0]` and `[0,1]`, into
  soft targets like `[0.9, 0.1]`
- increase regularization: we increased the dropout rates and weight decays
- early stopping: we modified the stopping criteria to be based on calibration and confidence, not accuracy.

With these modifications, the samples generated from the diffusion model were much more realistic and varied. The key lesson here is that guidance quality is as important as diffusion quality. A poorly calibrated classifier can actively harm sample diversity even when the underlying model is strong.

## Takeaways

A few things that surprised us or that I would have liked to know earlier:

- Quantile normalization changed the data distribution enough that the cosine schedule's advantages largely disappeared. Benchmark your schedule choice after deciding on normalization.
- For tabular data with smaller training sets, the ~30% validity improvement we saw from EMA was not a marginal gain. For us, it was the difference between a usable and an unusable model.
- Mode collapse disguised as high accuracy is a real failure mode. Train the guidance classifier on noisy inputs, use label smoothing, and evaluate on calibration rather than raw accuracy.
- The $$\lambda_i$$ parameters let you dial in how strongly each auxiliary function influences sampling, which is much more flexible than
  retraining the diffusion model itself.
