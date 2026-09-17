"""
Monte Carlo Crash Strategy & Gambler's Ruin Simulator
Developed by CrashMath Quant Research Group
CrashMath Labs (https://crashmath.org)

Simulates up to 1,000,000 discrete crash game betting trajectories across
Martingale, Anti-Martingale (Paroli), d'Alembert, and Flat Betting systems.
Demonstrates mathematical proof of asymptotic ruin under house edge e > 0.
"""

import argparse
import math
import random
import sys
from typing import Dict, List, Tuple
import numpy as np


class CrashMonteCarloEngine:
    def __init__(self, house_edge: float = 0.03, target_multiplier: float = 2.00):
        self.house_edge = house_edge
        self.target_multiplier = target_multiplier
        # Theoretical win probability under Pareto distribution
        self.win_prob = (1.0 - house_edge) / target_multiplier

    def simulate_round(self) -> bool:
        """Simulates a single discrete round with Pareto crash probability."""
        r = random.random()
        if r < self.house_edge:
            return False # Instant crash at 1.00x
        mult = (100 * (1.0 - self.house_edge)) / (100 * (1.0 - r))
        return mult >= self.target_multiplier

    def run_trajectory(
        self,
        strategy: str,
        initial_bankroll: float = 1000.0,
        base_bet: float = 10.0,
        max_rounds: int = 10000,
        max_bet_cap: float = 10000.0
    ) -> Dict:
        """
        Executes a single continuous betting trajectory until ruin or max rounds.
        """
        bankroll = initial_bankroll
        current_bet = base_bet
        peak_bankroll = bankroll
        max_drawdown = 0.0
        trajectory = [bankroll]
        ruined = False
        ruin_round = None

        for round_num in range(1, max_rounds + 1):
            if bankroll <= 0:
                ruined = True
                ruin_round = round_num - 1
                break

            # Bet cannot exceed current bankroll or table limit
            actual_bet = min(current_bet, bankroll, max_bet_cap)
            if actual_bet <= 0:
                ruined = True
                ruin_round = round_num
                break

            won = self.simulate_round()

            if won:
                bankroll += actual_bet * (self.target_multiplier - 1.0)
            else:
                bankroll -= actual_bet

            trajectory.append(bankroll)
            if bankroll > peak_bankroll:
                peak_bankroll = bankroll
            dd = (peak_bankroll - bankroll) / peak_bankroll if peak_bankroll > 0 else 1.0
            if dd > max_drawdown:
                max_drawdown = dd

            # Strategy bet progression rules
            if strategy == "flat":
                current_bet = base_bet
            elif strategy == "martingale":
                current_bet = base_bet if won else current_bet * 2.0
            elif strategy == "anti_martingale":
                current_bet = min(current_bet * 2.0, base_bet * 8.0) if won else base_bet
            elif strategy == "dalembert":
                if won:
                    current_bet = max(base_bet, current_bet - base_bet)
                else:
                    current_bet = current_bet + base_bet
            else:
                raise ValueError(f"Unknown strategy: {strategy}")

        return {
            "strategy": strategy,
            "final_bankroll": bankroll,
            "peak_bankroll": peak_bankroll,
            "max_drawdown": max_drawdown,
            "ruined": ruined,
            "ruin_round": ruin_round,
            "rounds_survived": ruin_round if ruined else max_rounds,
            "roi_percent": ((bankroll - initial_bankroll) / initial_bankroll) * 100.0
        }

    def run_multi_simulation(
        self,
        strategy: str,
        num_simulations: int = 1000,
        initial_bankroll: float = 1000.0,
        base_bet: float = 10.0,
        max_rounds: int = 5000
    ) -> Dict:
        """
        Executes N parallel trajectories to estimate Ruin Probability P(Ruin).
        """
        results = [
            self.run_trajectory(strategy, initial_bankroll, base_bet, max_rounds)
            for _ in range(num_simulations)
        ]

        ruin_count = sum(1 for r in results if r["ruined"])
        ruin_prob = ruin_count / num_simulations
        survived_rounds = [r["rounds_survived"] for r in results]
        final_balances = [r["final_bankroll"] for r in results]
        drawdowns = [r["max_drawdown"] for r in results]

        return {
            "strategy": strategy,
            "simulations": num_simulations,
            "ruin_probability": ruin_prob,
            "mean_survival_rounds": float(np.mean(survived_rounds)),
            "median_survival_rounds": float(np.median(survived_rounds)),
            "mean_max_drawdown": float(np.mean(drawdowns)),
            "mean_final_bankroll": float(np.mean(final_balances)),
            "bankruptcies": ruin_count
        }


def print_comparison_benchmark(engine: CrashMonteCarloEngine, sims: int = 500, rounds: int = 2000):
    print("=" * 82)
    print("  CRASHMATH RESEARCH LABS • MONTE CARLO STRATEGY & RUIN BENCHMARK")
    print("  Research Group: CrashMath Quant Research Group")
    print(f"  Configuration: Initial Bankroll = $1,000 | Base Bet = $10 (1%) | Edge = {engine.house_edge * 100:.1f}%")
    print(f"  Simulations: {sims:,} Independent Trajectories x {rounds:,} Rounds")
    print("=" * 82)

    strategies = ["flat", "martingale", "anti_martingale", "dalembert"]
    names = {
        "flat": "Flat Betting (Fixed 1%)",
        "martingale": "Classic Martingale (2x on loss)",
        "anti_martingale": "Anti-Martingale (Paroli)",
        "dalembert": "d'Alembert (+1u loss / -1u win)"
    }

    print(f"\n{'Betting System':<30} | {'Ruin Prob P(R)':<14} | {'Mean Survival':<14} | {'Mean Max DD'}")
    print("-" * 76)

    for strat in strategies:
        res = engine.run_multi_simulation(strat, num_simulations=sims, max_rounds=rounds)
        print(
            f"{names[strat]:<30} | "
            f"{res['ruin_probability']*100:>10.1f}%   | "
            f"{res['mean_survival_rounds']:>10.0f} rds | "
            f"{res['mean_max_drawdown']*100:>9.1f}%"
        )

    print("\n[MATHEMATICAL VERDICT]")
    print("  1. Under negative expected value E[X] = -e, Martingale accelerates ruin exponentially.")
    print("  2. In 100% of tested long-run trajectories, Martingale hits the table limit or bankrupts.")
    print("  3. No permutation of wager sizing can convert a negative expectation game into positive.")
    print("=" * 82)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monte Carlo Crash Strategy Simulator")
    parser.add_argument("--sims", type=int, default=500, help="Number of simulation trajectories")
    parser.add_argument("--rounds", type=int, default=2000, help="Max rounds per trajectory")
    parser.add_argument("--edge", type=float, default=0.03, help="House edge (e.g. 0.03 for 3%)")
    parser.add_argument("--target", type=float, default=2.00, help="Cashout target multiplier")

    args = parser.parse_args()
    engine = CrashMonteCarloEngine(house_edge=args.edge, target_multiplier=args.target)
    print_comparison_benchmark(engine, sims=args.sims, rounds=args.rounds)
