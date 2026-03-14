---
layout: page
published: true
title: Multi-Agent Reinforcement Learning
description: Using topological stratifications to improve PPO and DQN agents in a multi-agent command-and-control environment.
img: assets/img/publication_preview/rl_preview.png
img_max_height: 150px
importance: 1
category: ml
related_publications: true
---

This project investigates multi-agent reinforcement learning (MARL) for command-and-control
(C2) orchestration, where multiple autonomous agents must coordinate to accomplish
shared objectives in a partially observable environment.

The goal of the game is to get trained agents to work together to track a target. Each agent
has an energy bank that is depleted while they are actively tracking the target. There is a
harsh penalty for losing track of the target and smaller penalties for "using energy" with
tracking devices.

## Environment

Agents were trained in grid-based environments built on
[Griddly](https://github.com/Bam4d/Griddly), a fast and flexible game engine
designed for RL research. Griddly provides an extremely fast game engine
written in C++, boasting over 30,000 frames per second during simulation. The
environment interface was initially implemented using OpenAI Gym, which later
migrated to [Farama Foundation Gymnasium](https://gymnasium.farama.org/) as
the community standard (and maintenance) shifted. The multi-agent coordination layer was handled
via [PettingZoo](https://pettingzoo.farama.org/), which provides a standard
API for multi-agent environments compatible with Gymnasium.
We used ray's RLLib for parallelization and interfacing between Griddly and Gymnasium.
The RLLib aspect of the project was responsible for handling the distributed policy
mapping for the multi-agent setup.

## Algorithms

### Baseline

We trained agents using two standard deep RL algorithms:

- **PPO** (Proximal Policy Optimization) — an on-policy actor-critic method well-suited to
  cooperative multi-agent settings due to its stability and sample efficiency.
- **DQN** (Deep Q-Network) — an off-policy value-based method, used here as a baseline
  and point of comparison for the policy gradient approach.

Both algorithms were applied in the decentralized execution setting, where each agent
maintains its own policy but training incorporates shared reward signals reflecting
team-level objectives. As the size of the environment increases, the performance with
both of these algorithms plummets. The agents cannot overcome the additional size of the
grid worl and never come close to succesfully tracking the target.

## Topological stratifications

Our main contribution was the use of **topological stratifications**
to improve agent performance. The state-action space of the C2 environment has natural geometric
structure in which agents occupy specific positions and each sensor has limited range. In
order for them to work collaboratively they must interact across a spatial domain.
Competing against this is their energy budget, ensuring they must only send information to one another or
track the target when it is feasible and efficient.
The stratified nature of this setup can be exploited to improve performance both during training
and evaluation.

A stratification decomposes the state-action space into several strata of different topological,
reflecting qualitative differences in the coordination problem (e.g., isolated agents
vs. connected clusters vs. encirclement configurations). By incorporating topological
features derived from their geometric arrangement in the grid world (computed using persistent homology)
into the agent's observation, the policy
receives a richer signal about the global structure of the current configuration, not
just local observations. Meta-agents can be deployed to orchestrate the stratification
or it can be learned directly.

### Improvements with Topology

This approach improved performance for both PPO and DQN agents relative to baselines
without topological augmentation, suggesting that topological features provide
complementary information to standard spatial observations in cooperative MARL tasks.

{% capture fig_caption %}
The mean reward for collaborative tracking in a C2 system highlighting the efficiency of
using topological stratifications.
Taken from {% cite catanzaro_topological_2024 %}.
{% endcapture %}

<div class="text-center">
{% include figure.liquid path="assets/img/ppo_vs_dqn.png" caption=fig_caption
zoomable=true %}
</div>

The above plot compares performance of baseline PPO vs topologically-enhanced PPO for this
game. The episode reward mean is shown together with more common sense metrics for the
tracking game. In all arrangements, we see significant improvements when we use
stratifications during learning (Mask) compared to only during inference (no Mask). The
comparison between naive training and topologically-informed training is not shown on this
plot but can be found in {% cite catanzaro_topological_2024 %}--it is even more stark.
