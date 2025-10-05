#!/usr/bin/env python3
"""Full Analysis Script - Demonstrates all paper components.

This script runs a complete analysis of the Stackelberg-Bayesian espionage game,
demonstrating all theoretical components from the academic paper.

Usage:
    python run_full_analysis.py
"""

import logging
import numpy as np

from src.models.parameters import Parameters
from src.solvers.nash_solver import solve_nash_equilibrium
from src.analysis import (
    verify_kkt_conditions,
    format_kkt_report,
    analyze_strategic_interaction,
    format_strategic_interaction_report,
    compute_welfare_decomposition,
    compute_effect_decomposition,
)
from src.topology.level_12_interim_profits import (
    compute_expected_Pi_1,
    compute_expected_Pi_2,
    compute_Delta_Pi_2_info,
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


def print_header(title: str):
    """Print a formatted section header."""
    logger.info("")
    logger.info("=" * 80)
    logger.info(title.center(80))
    logger.info("=" * 80)
    logger.info("")


def main():
    """Run full analysis."""
    logger.info("")
    logger.info("█" * 80)
    logger.info("█" + " " * 78 + "█")
    logger.info("█" + "  STACKELBERG-BAYESIAN ESPIONAGE GAME".center(78) + "█")
    logger.info("█" + "  Complete Analysis with All Paper Components".center(78) + "█")
    logger.info("█" + " " * 78 + "█")
    logger.info("█" * 80)

    # Setup
    params = Parameters.baseline()
    rng = np.random.default_rng(42)

    # ========== SECTION 1: NASH EQUILIBRIUM ==========
    print_header("SECTION 1: NASH EQUILIBRIUM SOLUTION")

    logger.info("Solving Nash equilibrium in investment game...")
    logger.info("")

    solution = solve_nash_equilibrium(params, seed=42)

    I_1_star, I_2_star = solution.investments
    rho_star = solution.contest_prob
    kappa_star = solution.signal_precision
    V_1_star, V_2_star = solution.value_functions
    U_1_star, U_2_star = solution.utilities
    CS_star = solution.consumer_surplus
    W_star = solution.total_welfare

    logger.info("EQUILIBRIUM OUTCOMES:")
    logger.info(f"  Investments:         I₁* = {I_1_star:.6f}, I₂* = {I_2_star:.6f}")
    logger.info(f"  Contest success:     ρ* = {rho_star:.6f}")
    logger.info(f"  Signal precision:    κ* = {kappa_star:.6f}")
    logger.info(f"  Expected profits:    V₁* = {V_1_star:10.2f}, V₂* = {V_2_star:10.2f}")
    logger.info(f"  Utilities:           U₁* = {U_1_star:10.2f}, U₂* = {U_2_star:10.2f}")
    logger.info(f"  Consumer surplus:    CS* = {CS_star:10.2f}")
    logger.info(f"  Total welfare:       W*  = {W_star:10.2f}")

    # ========== SECTION 2: INTERIM PROFITS (THEOREM 4) ==========
    print_header("SECTION 2: INTERIM PROFIT ANALYSIS (Theorem 4)")

    logger.info("Computing interim profit closed-forms...")
    logger.info("")

    # Information value
    Delta_Pi_info = compute_Delta_Pi_2_info(kappa_star, params)

    logger.info("INFORMATION VALUE:")
    logger.info(f"  ΔΠ₂^Info(κ*) = {Delta_Pi_info:.4f}")
    logger.info(f"  Expected gain from espionage: ρ* × ΔΠ₂^Info = {rho_star * Delta_Pi_info:.4f}")
    logger.info("")

    logger.info("INTERIM PROFIT DECOMPOSITION:")
    logger.info(f"  Leader:   E[Π₁*] = (p₁* - c₁)² · B_{{ρ,κ}}")
    logger.info(f"  Follower: E[Π₂*] = Π₂^U + ρ · ΔΠ₂^Info(κ)")
    logger.info("")
    logger.info("  → Leader's profit depends on own cost realization")
    logger.info("  → Follower's profit has baseline + information premium")

    # ========== SECTION 3: KKT VERIFICATION (THEOREM 5) ==========
    print_header("SECTION 3: KKT CONDITION VERIFICATION (Theorem 5)")

    logger.info("Verifying KKT necessary conditions for Nash equilibrium...")
    logger.info("(This may take 1-2 minutes due to numerical derivatives)")
    logger.info("")

    kkt_diag = verify_kkt_conditions(I_1_star, I_2_star, params, rng, h=1e-4, tolerance=1e-3)
    kkt_report = format_kkt_report(kkt_diag)
    logger.info(kkt_report)

    # ========== SECTION 4: STRATEGIC INTERACTION (LEMMA 2, THEOREM 7) ==========
    print_header("SECTION 4: STRATEGIC INTERACTION ANALYSIS (Lemma 2, Theorem 7)")

    logger.info("Analyzing strategic complementarity/substitutability...")
    logger.info("")

    strat_diag = analyze_strategic_interaction(I_1_star, I_2_star, params)
    strat_report = format_strategic_interaction_report(strat_diag)
    logger.info(strat_report)

    # ========== SECTION 5: EFFECT DECOMPOSITION (PROPOSITION 5) ==========
    print_header("SECTION 5: SEQUENTIAL VS INFORMATION EFFECTS (Proposition 5)")

    logger.info("Decomposing profit differences into action-based vs type-based channels...")
    logger.info("(This may take 2-3 minutes due to Monte Carlo simulations)")
    logger.info("")

    decomp = compute_effect_decomposition(I_1_star, I_2_star, params, rng, N=5000)

    logger.info("GAME VARIANTS:")
    logger.info(f"  G^B (Benchmark):      Π₁^B = {decomp['firm_1']['Pi_B']:10.2f}, Π₂^B = {decomp['firm_2']['Pi_B']:10.2f}")
    logger.info(f"  G^h (Hybrid):         Π₁^h = {decomp['firm_1']['Pi_h']:10.2f}, Π₂^h = {decomp['firm_2']['Pi_h']:10.2f}")
    logger.info(f"  G^S (Full):           Π₁^S = {decomp['firm_1']['Pi_S']:10.2f}, Π₂^S = {decomp['firm_2']['Pi_S']:10.2f}")
    logger.info("")

    logger.info("FIRM 1 (Leader) DECOMPOSITION:")
    logger.info(f"  Total gain from full game:     Π₁^S - Π₁^B = {decomp['firm_1']['total_gain']:10.2f}")
    logger.info(f"    Sequential-move effect:      Π₁^h - Π₁^B = {decomp['firm_1']['sequential_effect']:10.2f}")
    logger.info(f"    Information effect (leak):   Π₁^S - Π₁^h = {decomp['firm_1']['information_effect']:10.2f}")
    logger.info("")
    logger.info("  Interpretation:")
    if decomp['firm_1']['sequential_effect'] > 0:
        logger.info("    → Leader benefits from first-mover advantage (sequential-move)")
    else:
        logger.info("    → Leader loses from follower's reaction (sequential-move)")

    if decomp['firm_1']['information_effect'] < 0:
        logger.info("    → Leader loses from espionage (information leakage)")
    else:
        logger.info("    → Leader gains from espionage dynamics")
    logger.info("")

    logger.info("FIRM 2 (Follower) DECOMPOSITION:")
    logger.info(f"  Total gain from full game:     Π₂^S - Π₂^B = {decomp['firm_2']['total_gain']:10.2f}")
    logger.info(f"    Sequential-move effect:      Π₂^h - Π₂^B = {decomp['firm_2']['sequential_effect']:10.2f}")
    logger.info(f"    Information effect (gain):   Π₂^S - Π₂^h = {decomp['firm_2']['information_effect']:10.2f}")
    logger.info("")
    logger.info("  Interpretation:")
    if decomp['firm_2']['sequential_effect'] < 0:
        logger.info("    → Follower loses from moving second (sequential-move)")
    else:
        logger.info("    → Follower benefits from observing leader")

    if decomp['firm_2']['information_effect'] > 0:
        logger.info("    → Follower gains from espionage (information advantage)")
    else:
        logger.info("    → Follower loses from espionage dynamics")

    # ========== SECTION 6: WELFARE DECOMPOSITION (THEOREM 6) ==========
    print_header("SECTION 6: WELFARE DECOMPOSITION (Theorem 6)")

    logger.info("Computing welfare derivative decomposition...")
    logger.info("(This may take 2-3 minutes due to numerical derivatives)")
    logger.info("")

    welfare_decomp = compute_welfare_decomposition(I_1_star, I_2_star, params, rng, h=1e-3)

    logger.info("MARGINAL WELFARE EFFECTS (∂W/∂I₂):")
    logger.info(f"  Total welfare derivative:     ∂W/∂I₂         = {welfare_decomp['dW_dI2']:12.6f}")
    logger.info(f"    Consumer surplus effect:    ∂E[CS]/∂I₂     = {welfare_decomp['dCS_dI2']:12.6f}")
    logger.info(f"    Leader profit effect:       ∂V₁/∂I₂        = {welfare_decomp['dV1_dI2']:12.6f}")
    logger.info(f"    Follower net profit effect: ∂V₂/∂I₂ - ψ'   = {welfare_decomp['dU2_dI2']:12.6f}")
    logger.info("")

    logger.info("INTERPRETATION:")
    logger.info(f"  Marginal cost of investment:  ψ'(I₂*) = {welfare_decomp['psi_prime']:12.6f}")
    logger.info("")

    if welfare_decomp['dCS_dI2'] > 0:
        logger.info("  → Consumers BENEFIT from more espionage (lower prices from competition)")
    else:
        logger.info("  → Consumers LOSE from more espionage (higher prices)")

    if welfare_decomp['dV1_dI2'] < 0:
        logger.info("  → Leader LOSES from follower's espionage (expected)")
    else:
        logger.info("  → Leader GAINS from follower's espionage (unexpected)")

    if welfare_decomp['dU2_dI2'] > 0:
        logger.info("  → Follower's marginal benefit exceeds marginal cost (wants more I₂)")
    else:
        logger.info("  → Follower's marginal benefit below marginal cost (wants less I₂)")

    # ========== SUMMARY ==========
    print_header("SUMMARY: KEY INSIGHTS")

    logger.info("1. EQUILIBRIUM CHARACTERIZATION:")
    logger.info(f"   - Investment levels are {'low' if I_2_star < 2 else 'moderate' if I_2_star < 10 else 'high'}")
    logger.info(f"   - Espionage success probability: {rho_star:.1%}")
    logger.info(f"   - Signal reliability: {kappa_star:.1%}")
    logger.info("")

    logger.info("2. PROFIT STRUCTURE:")
    logger.info(f"   - Leader profit: {'NEGATIVE' if V_1_star < 0 else 'POSITIVE'} (V₁* = {V_1_star:.2f})")
    logger.info(f"   - Follower profit: {'NEGATIVE' if V_2_star < 0 else 'POSITIVE'} (V₂* = {V_2_star:.2f})")
    logger.info("")

    logger.info("3. STRATEGIC INTERACTION:")
    logger.info(f"   - Investments are strategic {'COMPLEMENTS' if strat_diag.strategic_complementarity else 'SUBSTITUTES'}")
    logger.info(f"   - Cross-partial: ∂²ρ/∂I₁∂I₂ = {strat_diag.d2rho_dI1dI2:.6e}")
    logger.info("")

    logger.info("4. EFFECT CHANNELS:")
    logger.info(f"   - Leader's sequential advantage: {decomp['firm_1']['sequential_effect']:+.2f}")
    logger.info(f"   - Leader's information loss: {decomp['firm_1']['information_effect']:+.2f}")
    logger.info(f"   - Follower's sequential disadvantage: {decomp['firm_2']['sequential_effect']:+.2f}")
    logger.info(f"   - Follower's information gain: {decomp['firm_2']['information_effect']:+.2f}")
    logger.info("")

    logger.info("5. WELFARE IMPLICATIONS:")
    logger.info(f"   - Consumer surplus: {CS_star:.2f}")
    logger.info(f"   - Total welfare: {W_star:.2f}")
    logger.info(f"   - Consumer effect of espionage: {'POSITIVE' if welfare_decomp['dCS_dI2'] > 0 else 'NEGATIVE'}")
    logger.info("")

    logger.info("6. KKT VERIFICATION:")
    logger.info(f"   - Nash equilibrium satisfies KKT: {'YES' if kkt_diag.kkt_satisfied else 'NO (numerical tolerance)'}")
    logger.info(f"   - Firm 1 stationarity residual: {kkt_diag.firm_1['stationarity_residual']:.6e}")
    logger.info(f"   - Firm 2 stationarity residual: {kkt_diag.firm_2['stationarity_residual']:.6e}")

    # Final message
    logger.info("")
    logger.info("█" * 80)
    logger.info("█" + " " * 78 + "█")
    logger.info("█" + "  ANALYSIS COMPLETE".center(78) + "█")
    logger.info("█" + " " * 78 + "█")
    logger.info("█" + "  All theoretical components from the paper have been demonstrated.".center(78) + "█")
    logger.info("█" + " " * 78 + "█")
    logger.info("█" * 80)
    logger.info("")


if __name__ == "__main__":
    main()
