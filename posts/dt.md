---
title: From Decision Theories to Multi-Agent Reinforcement Learning
date: Mar 26, 2026
excerpt: Notes on rational decision-making in predictor environments and how it relates to RL.
tags: Alignment, RL
---

In the last post on Newcomb's problem, we briefly touched the different rational decision theories that lead to the one-box and two-box policies, and mused about their correlations with positions on alignment.
As it turns out, Newcomb's problem is actually a classical dilemma in decision theory, the mathematical framework in which many questions about AI alignment can be discussed. These are my notes from learning the subject.

Let us first take a look at the setup and two classical decision theories discussed in the context of Newcomb's problem.

A *decision task* is an optimization problem where, given a stochastic environment reward $R$, the policy $\pi$ needs to be chosen to maximize the expected payout $\mathbb{E}_\pi[R]$. The optimal policy is denoted by $\pi^*$. Unlike reinforcement learning environments modeled as Markov decision processes (MDPs) where the transition function $T(s, a)$ depends on the state $s$ and the action $a$, decision-theoretic environments allow *predictors*: the transition function $T(s, \pi)$ is allowed to depend on the full policy $\pi$.

According to Joyce's representation theorem, conditional likelihood and preference rankings that obey certain axioms give rise to a global *supposition function* $P(a \to o \mid x)$ and utility function $u(x)$ from which an expected utility can be defined as
$$V(x \mid a) = \sum_i P(a \to o_i \mid x) u(o_i).$$

Crucially, decision theories differ not in their notions of value, but in their supposition functions.

**Evidential Decision Theory (EDT)** sets $P(a \to o \mid x) = P(o \mid x, a)$ as standard Bayesian conditioning, regardless of causal structure. If in Newcomb's problem, the agent's *predisposition* $C$ affects both *prediction* $Y$ and *action* $A$, conditioning on $A = a$ changes the distribution of predictions $Y$ via $C$.

**Causal Decision Theory (CDT)** introduces the concept of a *causal intervention*. In Judea Pearl's $do$ calculus, a causal structure is assumed to be given, i.e. an orientation of the undirected conditional dependence graph that makes it a directed acyclic graph. The supposition function can then be set as $P(a \to o \mid x) = P(o \mid x, do(A = a))$, with the meaning of: remove all incoming edges to $A$, then evaluate the conditional $P(o \mid x, A=a)$ in the new graph.

EDT one-boxes in Newcomb's problem because one-boxing is correlated with a full second box, while CDT two-boxes because the (physical) causal graph dictates that the action cannot influence the content of the box.

There are also examples where EDT acts suboptimally (e.g. the smoking lesion problem), and ultimately, neither of them is apt for predictor environments where the policy can be instantiated by a predictor (e.g. in Parfit's hitchhiker problem) or face itself (e.g. in the twin prisoner's dilemma).

There are two more recent developments in decision theory attempting to find a formal framework capable of resolving such predictor dilemmas.

**Updateless Decision Theory (UDT)** introduces the notion of *pre-commitment* to a deterministic policy, which resolves the question of how to deal with multiple instantiations of $\pi$ in the environment. It can be defined simply as computing the optimal policy $\pi^*$ upfront and following it at evaluation time. An initial version operated with pre-commitment to unconditional actions, but pre-commitment to the full policy (conditional actions) is required to solve problems such as the transparent version of Newcomb's problem where the agent can pre-commit to one-boxing *except if* the second box should happen to be empty.

**Functional Decision Theory (FDT)** attempts to provide a formal framework for *computing* $\pi^*$ in certain situations. It treats the output of running the algorithm on observation $x$ within a world model $M$ as a variable $FDT(\ulcorner M \urcorner, \ulcorner x \urcorner)$ within $M$. (According to Kleene's second recursion theorem, such quoted variables can easily be represented.) 
FDT then argues that we should set $P(a \to o \mid x) = P(o \mid x, do(FDT(x) = a))$, which would allow reasoning about actions in state $x$ as pre-committed, causal interventions.
This contrasts with CDT where there is no such notion of pre-committed actions in a given state, breaking the logical linking between multiple instantiations of $\pi$ in Newcomblike environments.

However, the exact scientific status of FDT remains disputed. While the construction of quoted variables $\ulcorner x \urcorner$ appears logically sound, the notion of conditioning on a causal intervention by a false statement (a function outputting something that it doesn't output) cannot be given a value in standard probability theory.
This is the problem of *counterpossibles*, counterfactuals with impossible antecedents. Perhaps the FDT equations could be viewed as fixpoint equations that constrain the optimal policy, not as defining equations.

Moreover, the FDT authors further argue that a policy-level variant should be used that conditions on the choice of the entire algorithm $do(FDT=\pi)$ in order to solve multi-agent coordination problems. 
While conceptually correct, this removes the computational appeal of FDT, collapsing FDT to the same abstract definition as UDT: the optimal policy is a deterministic policy that "implicitly knows about itself".
Follow-up works on Logical Induction at MIRI approach the question of epistemic beliefs about logical statements over time (amount of compute), but crucially still lack a mechanism for counterfactual intervention as required by FDT.

## Decision Theories and RL

Which decision theories do RL algorithms converge to? Can they extend from Markov decision processes (MDPs) to Newcomblike decision processes (NDPs) with predictors as defined above? The following sections are less well researched (I expect there to be plenty of existing literature and thought experiments), but represent my notes from learning and thinking about the subject, including where I question the usefulness of the decsion-theoretic framing. 

### Stochastic policies
So far, we have ignored questions about deterministic vs stochastic policies. Since a stochastic policy can be parametrized by a deterministic function, this situation is covered by the UDT definition of optimal pre-committed policies. Again, policy-level FDT reduces to UDT, while action-level FDT is unable to represent all optimal policies, including stochastic ones.

LLMs are a prime example of deterministic functions that parametrize distributions, sampling from which defines stochastic policies. How would we frame this in Newcomblike environments with predictors? We can obtain a perfect predictor by giving at access to the weights $\theta$ *and* the sampling seed of the random number generator. The policy is fully deterministic from the point of view of the predictor. (The predictor is white box attacker.)  Conversely, we can have the predictor treat the policy as a true stcohastic policy without access to the sampling seed. (The predictor is a black box attacker.)

Offline reinforcement learning is concerned with $\mathbb{E}[R \mid s, a]$, i.e. it could be seen as implementing EDT, which comes with its known shortcomings from confounders and spurious correlations.
Online RL addresses this issue by implementing an exploration mechanism (e.g. $\epsilon$-greedy or softmax sampling) that serves as a causal intervention: by means of sampling actions, the algorithm approximates $ \mathbb{E}[R \mid s, do(a)]$ and online RL algorithms could be seen as an implementation of CDT.

Value-based online RL is therefore unsound in Newcomblike environments: the Bellman equation assumes an MDP structure and conflates $Q$-values for the same $(s,a)$-pair coming from different policies $\pi$.
On the other hand, in the open-box case of predictors with access to the seed, policy gradient methods already operate at the level of pre-committed policies. This is the UDT setup and *converged* policy gradient policies should be optimal.

We will leave open the questions of predictors for stochastic policies as it would likely require a proper adversarial objective for the predictor, and of treating the learning process as an environment instead of the converged policy. The latter is the question of alignment and requires a separate post.

### Performative RL and Multi-Agent RL
As mentioned above, value-based RL relies on the Bellman equation for MDPs, which is false for general NDPs where the environment dynamics $T(s, \pi)$ may depend upon the full policy as well as the reward $R(s, \pi)$. Performative reinforcement learning studies reinforcement learning where the environment depends upon a policy $\mu$. The overall objective is hence of the form $J(\pi, \mu)$ and the Newcombike case is where $\mu = \pi$, i.e. $J(\pi, \pi)$. Unlike in the case of MDPs, the performative Bellman equation no longer lends itself to an iteration algorithm for computing $Q$-values. Policy-gradient methods instead can be salvaged: the performative policy gradient theorem adds the additional terms resulting from environment drift $\nabla_\theta \log T_\theta$ and $\nabla_\theta R_\theta$ that are dropped in MDPs where $T$ and $R$ do not depend on $\theta$.

Whether we actually have access to differentiable environment dynamics depends upon the setup. The only situation where $\theta$ could currently be used realistically in the environment is by running inference on the policy, in which case the situation is dealt with by game-theoretic approaches to multi-agent reinforcement learning. This is likely the correct setup for studying such problems in machine learning in practice: it is stochastic by design, does not search for discrete rational decision rules in vain, but uses the established notions of policy optimization, equilibria and convergence to solve problems without closed-form solution. 

In practice, having access to differentiable environment dynamics $T(s,\pi​)$ is rare. The realistic scenario where $\pi$ directly influences the environment is when the environment - or another agent within it - runs inference on the policy. This shifts the framework from single-agent performative RL to Multi-Agent Reinforcement Learning (MARL).

MARL provides the machine learning framework for dealing with Newcomblike decision processes without the need for a discrete rational decision rule such as FDT. Game-theoretic RL treats the predictor as a player, is stochastic by design and provides the notion of convergence to joint equilibria which captures that of optimal behavior.

## References

Gerstgrasser, Matthias, and David C. Parkes. "Oracles & followers: Stackelberg equilibria in deep multi-agent reinforcement learning." International Conference on Machine Learning. [PMLR, 2023.](https://proceedings.mlr.press/v202/gerstgrasser23a/gerstgrasser23a.pdf)

Gerstgrasser, Matthias, and David C. Parkes. "Oracles & followers: Stackelberg equilibria in deep multi-agent reinforcement learning." International Conference on Machine Learning. [PMLR, 2023.](https://proceedings.mlr.press/v202/gerstgrasser23a/gerstgrasser23a.pdf)

Joyce, James M. The foundations of causal decision theory. Cambridge University Press, 1999. [Chapter PDF.](https://gwern.net/doc/statistics/decision/1999-joyce.pdf)

Yudkowsky, Eliezer, and Nate Soares. "Functional decision theory: A new theory of instrumental rationality." [Arxiv.](https://arxiv.org/abs/1710.05060)

