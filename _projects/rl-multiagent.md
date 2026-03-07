---
layout: page
published: false
title: Multi-Agent Reinforcement Learning
description: Using topological stratifications to improve PPO and DQN agents in a multi-agent command-and-control environment.
img:
importance: 1
category: ml
related_publications: true
---

This project investigates multi-agent reinforcement learning (MARL) for command-and-control
(C2) orchestration, where multiple autonomous agents must coordinate to accomplish
shared objectives in a partially observable environment.

## Environment

Agents were trained in grid-based environments built on [Griddly](https://github.com/Bam4d/Griddly),
a fast and flexible game engine designed for RL research. The environment interface
was initially implemented using OpenAI Gym, and later migrated to
[Farama Foundation Gymnasium](https://gymnasium.farama.org/) as the community
standard shifted. The multi-agent coordination layer was handled via
[PettingZoo](https://pettingzoo.farama.org/), which provides a standard API
for multi-agent environments compatible with Gymnasium.

## Algorithms

We trained agents using two standard deep RL algorithms:

- **PPO** (Proximal Policy Optimization) — an on-policy actor-critic method well-suited to
  cooperative multi-agent settings due to its stability and sample efficiency.
- **DQN** (Deep Q-Network) — an off-policy value-based method, used here as a baseline
  and point of comparison for the policy gradient approach.

Both algorithms were applied in the decentralized execution setting, where each agent
maintains its own policy but training incorporates shared reward signals reflecting
team-level objectives.

## Topological stratifications

The central contribution of this project is the use of **topological stratifications**
to improve agent performance. The state space of the C2 environment has natural geometric
structure — agents occupy positions, form coalitions, and interact across a spatial domain
— and this structure can be exploited.

A stratification decomposes the state space into strata of different topological type,
reflecting qualitative differences in the coordination problem (e.g., isolated agents
vs. connected clusters vs. encirclement configurations). By incorporating topological
features derived from persistent homology into the agent's observation, the policy
receives a richer signal about the global structure of the current configuration, not
just local observations.

This approach improved performance for both PPO and DQN agents relative to baselines
without topological augmentation, suggesting that topological features provide
complementary information to standard spatial observations in cooperative MARL tasks.

