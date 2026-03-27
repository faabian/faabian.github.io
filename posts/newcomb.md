---
title: Newcomb's Paradox, Free Will and Superintellignce
date: Mar 24, 2026
excerpt: What could Newcomb's Paradox on near-perfect prediction of human behavior mean for alignment?
tags: Alignment
---

You enter a room with two boxes. One of them is open and contains \$1,000. The other one is closed, hence we'll call it the *mystery box*. Its contents have been set by a supercomputer before you entered the room. It can contain \$1,000,000 or be empty. You can either choose to take the contents of both boxes, or only of the mystery box. But here's the catch: you know that the supercomputer predicts whether you will choose both boxes or the mystery box only, and it placed the money into the mystery box if and only if it predicted that you would take only that box. You are also told that the supercomputer has had near-perfect prediction accuracies for both actions in the past.

The paradox is called **Newcomb's Paradox** and it is famous for having two strategies that both appear evident to a large proportion of respondents with low "conversion rates" between the solutions.

**One-boxers** set $p$ as the probability that the supercomputer accurately predicts your choice (assumed symmetric for simplicity) and calculate
$$
E[\text{one box}] = 1\,000\,000p + (1-p) \cdot 0
$$
and
$$
E[\text{two boxes}] = 1\,000p + (1-p) \cdot 1\,001\,000
$$
so
$$
\begin{align*}
E[\text{one box}] &\ge E[\text{two boxes}] \\
1\,000\,000p &\ge 1\,000p + 1\,001\,000(1-p) \\
2\,000\,000p &\ge 1\,001\,000 \\
p &\ge 0.5005
\end{align*}
$$
This appears highly likely given that the supercomputer has had high prediction success rates on both actions in the past, and the threshold is only marginally above chance.

**Two-boxers** appeal to causality (the mystery box has already been set regardless of your decision) and strategic dominance (no matter the box contents, two boxes will contain \$1,000 more than the mystery box only).

Ultimately, the paradox reduces to free will vs determinism, or time travel paradoxes. 
If one-boxers take home a million dollars, they must concede that it was not because of their "decision" but precisely because their choice was entirely predictable for the supercomputer and they were merely lucky for having a given predisposition. This, however, renders the question on optimal behavior moot to begin with. Conversely, if we insist on true free will (in the sense of unpredictable agency), the only way a predictor could achieve near-perfect accuracy is by inspecting our future choices, which requires backward-in-time causation.

Here I'd like to take another angle. Once we understand that the assumptions of free will, no time travel and near-perfect prediction are logically inconsistent, the paradox serves less as a logical riddle and more as test of the respondent's priors on these hypotheses. While thought experiments usually ask us to accept their premises *no questions asked*, an inconsistent thought experiment forces us to compute our posterior from our prior beliefs *and* the hypotheses of the thought experiment.
Hence, the modern framing of the action predictor as a "supercomputer" is no longer arbitrary.
Robert Nozick's original 1969 publication framed the predictor simply as an alien "being" with advanced science. Updating this entity to a supercomputer (as Veritasium does) turns the paradox into a proxy for superintelligence and alignment. It implicitly measures - amongst others - whether respondents believe that their agency can *outsmart the machine* or whether they are willing to accept the premise of a predictive superintelligence. Woth which specific stances on alignment are one-boxers and two-boxers correlated?

### Related Material
* [Wikipedia: Interpretations of Newcomb's Problem](https://en.wikipedia.org/wiki/Newcomb%27s_problem#Interpretations)
* [Veritasium: The Paradox That Splits Smart People 50/50](https://www.youtube.com/watch?v=Ol18JoeXlVI)
