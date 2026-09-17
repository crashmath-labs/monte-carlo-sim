# Monte Carlo Crash Strategy & Gambler's Ruin Simulator

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](https://opensource.org/licenses/MIT)
[![Research: Quantitative Risk](https://img.shields.io/badge/Research-Applied%20Probability-purple.svg)](https://crashmath.org)

A high-performance **Monte Carlo risk simulation engine** evaluating sequential betting systems (Martingale, Anti-Martingale, d'Alembert, Flat Betting) against Provably Fair crash game probability distributions.

Developed by the **CrashMath Quant Research Group** at [CrashMath Labs](https://crashmath.org).

---

## The Gambler's Ruin Theorem in Crash Games

Many recreational crash game participants believe that systematic staking progressions (e.g. doubling wagers after a loss) can overcome the house edge.

This library provides exact mathematical simulations and proofs showing that under any continuous game with house edge $e > 0$, **the probability of complete capital ruin converges to 1 as the number of rounds $N \to \infty$**:

$$\lim_{N \to \infty} P(\text{Bankroll}_N \le 0) = 1.00$$

### Expected Value Invariance (Doob's Theorem)

By Doob's Optional Stopping Theorem, for a supermartingale process with negative drift:

$$\mathbb{E}[B_t] = B_0 - e \sum_{i=1}^{t} w_i$$

Where $B_t$ is bankroll at time $t$, $B_0$ is initial capital, $e$ is house edge ($e = 0.03$ or $0.01$), and $w_i$ is the wager at round $i$. Because wagers $w_i$ grow exponentially under Martingale ($w_i = w_0 \cdot 2^{i-1}$), expected total loss accelerates directly with betting progression.

---

## Empirical Benchmark (1,000 Trajectories x 5,000 Rounds)

Simulation parameters: Initial Bankroll = $1,000 | Base Wager = $10 (1%) | House Edge = 3.0% ($e=0.03$) | Target = 2.00x:

| Betting System | Formula / Rule | Ruin Probability $P(\text{Ruin})$ | Median Survival | Mean Max Drawdown |
| :--- | :--- | :---: | :---: | :---: |
| **Flat Betting** | Fixed $w = 1\%$ bankroll | **18.4%** | 5,000+ rds | 42.1% |
| **d'Alembert** | $+1u$ on loss / $-1u$ on win | **76.2%** | 2,140 rds | 88.5% |
| **Anti-Martingale (Paroli)** | Double on win (capped 3x) | **41.8%** | 4,200 rds | 64.7% |
| **Classic Martingale** | Double $w \times 2$ on every loss | **99.8%** | **412 rds** | **100.0%** |

> **Key Takeaway**: Martingale does not reduce risk; it compresses risk into rare, catastrophic liquidation events. A sequence of just 7 consecutive losses ($0.515^7 \approx 0.94\%$, occurring on average once every 106 rounds) requires a $1,280 wager, immediately exhausting the entire bankroll.

---

## Quickstart

### Installation

```bash
git clone https://github.com/crashmath-labs/monte-carlo-sim.git
cd monte-carlo-sim
pip install -r requirements.txt
```

### Run Multi-Strategy Comparison

```bash
# Run benchmark across 500 parallel trajectories
python simulator.py --sims 500 --rounds 2000 --edge 0.03 --target 2.00
```

Sample Terminal Output:
```text
==================================================================================
  CRASHMATH RESEARCH LABS • MONTE CARLO STRATEGY & RUIN BENCHMARK
  Research Group: CrashMath Quant Research Group
  Configuration: Initial Bankroll = $1,000 | Base Bet = $10 (1%) | Edge = 3.0%
  Simulations: 500 Independent Trajectories x 2,000 Rounds
==================================================================================

Betting System                 | Ruin Prob P(R) | Mean Survival  | Mean Max DD
----------------------------------------------------------------------------
Flat Betting (Fixed 1%)        |       12.4%   |       1890 rds |      38.6%
Classic Martingale (2x on loss)|       99.6%   |        428 rds |     100.0%
Anti-Martingale (Paroli)       |       38.2%   |       1680 rds |      62.1%
d'Alembert (+1u loss / -1u win)|       68.8%   |       1240 rds |      84.2%

[MATHEMATICAL VERDICT]
  1. Under negative expected value E[X] = -e, Martingale accelerates ruin exponentially.
  2. In 100% of tested long-run trajectories, Martingale hits table limits or bankrupts.
  3. No permutation of wager sizing can convert a negative expectation game into positive.
==================================================================================
```

---

## Interactive Strategy Backtester

To test customized bankroll sizes, cashout multipliers, and stop-loss limits in a visual CAD-style interface, visit the [CrashMath Strategy Backtester](https://crashmath.org/#backtester).

---

## Technical Whitepaper Reference

This simulation framework forms Section 4.2 of the open technical report:

> CrashMath Labs (2026). *Empirical Evaluation of 50,000 Provably Fair Rounds: Autocorrelation, House Edge Invariance, and Resistance to Machine Learning Predictors*. Technical Report CRASHMATH-TECH-2026-04, CrashMath Labs.  
> PDF: [`https://crashmath.org/papers/provably-fair-empirical-study-2026.pdf`](https://crashmath.org/papers/provably-fair-empirical-study-2026.pdf)

```bibtex
@software{crashmath2026montecarlosim,
  author = {CrashMath Quant Research Group},
  title = {Monte Carlo Crash Strategy & Gambler's Ruin Simulator},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/crashmath-labs/monte-carlo-sim}}
}
```

---

## License

MIT © 2026 CrashMath Labs.
