"""KKT Condition Verification (Theorem 5).

Constitutional Compliance:
- Principle IV: Reproducibility & Validation
- Principle V: Algorithm Transparency
- Principle VI: Documentation Standards

Implements: Theorem 5 from the paper - KKT necessary conditions for
Nash equilibrium in investment game.

Mathematical Source:
    - Theorem 5: KKT conditions for Nash equilibrium
    - Stationarity: ∂V_i/∂I_i - ψ'(I_i) - μ_i^L + μ_i^U = 0
    - Primal feasibility: 0 ≤ I_i ≤ Ī
    - Dual feasibility: μ_i^L, μ_i^U ≥ 0
    - Complementary slackness: μ_i^L·I_i = 0, μ_i^U·(Ī - I_i) = 0
"""

import numpy as np
from typing import Dict, Tuple
from dataclasses import dataclass

from src.models.parameters import Parameters


@dataclass
class KKTDiagnostics:
    """KKT condition diagnostics for Nash equilibrium.

    Attributes:
        I_1_star: Leader's equilibrium investment
        I_2_star: Follower's equilibrium investment
        firm_1: KKT diagnostics for firm 1
        firm_2: KKT diagnostics for firm 2
        kkt_satisfied: Whether KKT conditions are satisfied (within tolerance)
        tolerance: Numerical tolerance used
    """
    I_1_star: float
    I_2_star: float
    firm_1: Dict[str, float]
    firm_2: Dict[str, float]
    kkt_satisfied: bool
    tolerance: float


def compute_marginal_value(
    i: int,
    I_1: float,
    I_2: float,
    params: Parameters,
    rng: np.random.Generator,
    h: float = 1e-5
) -> float:
    """Compute ∂V_i/∂I_i numerically.

    Args:
        i: Firm index (1 or 2)
        I_1: Leader's investment
        I_2: Follower's investment
        params: Model parameters
        rng: Random number generator
        h: Step size for numerical derivative

    Returns:
        float: ∂V_i/∂I_i

    Mathematical Source:
        Theorem 5, stationarity condition
    """
    from src.topology.level_10_value_functions import compute_V_1, compute_V_2

    # Create independent RNGs for reproducibility
    rng_plus = np.random.default_rng(42)
    rng_minus = np.random.default_rng(42)

    if i == 1:
        # ∂V₁/∂I₁
        V_plus = compute_V_1(I_1 + h, I_2, params, rng_plus)
        V_minus = compute_V_1(I_1 - h, I_2, params, rng_minus)
    else:
        # ∂V₂/∂I₂
        V_plus = compute_V_2(I_1, I_2 + h, params, rng_plus)
        V_minus = compute_V_2(I_1, I_2 - h, params, rng_minus)

    dV_dI = (V_plus - V_minus) / (2 * h)

    return dV_dI


def compute_marginal_investment_cost(
    I_i: float,
    kappa_i: float
) -> float:
    """Compute ψ'(I_i) = κ_i·I_i (marginal investment cost).

    Investment cost function: ψ(I_i) = (κ_i/2)·I_i²

    Args:
        I_i: Investment level
        kappa_i: Investment cost parameter

    Returns:
        float: ψ'(I_i)

    Mathematical Source:
        Equation (3.8) in paper
    """
    return kappa_i * I_i


def compute_lagrange_multipliers(
    dV_dI: float,
    psi_prime: float,
    I_i: float,
    I_bar: float,
    tolerance: float = 1e-6
) -> Tuple[float, float]:
    """Compute Lagrange multipliers μ^L and μ^U from stationarity.

    Stationarity condition:
        ∂V_i/∂I_i - ψ'(I_i) - μ_i^L + μ_i^U = 0

    Combined with complementary slackness:
        - If I_i = 0: μ^L = ∂V_i/∂I_i - ψ'(I_i), μ^U = 0
        - If 0 < I_i < Ī: μ^L = 0, μ^U = 0
        - If I_i = Ī: μ^L = 0, μ^U = ψ'(I_i) - ∂V_i/∂I_i

    Args:
        dV_dI: Marginal value ∂V_i/∂I_i
        psi_prime: Marginal cost ψ'(I_i)
        I_i: Investment level
        I_bar: Investment upper bound
        tolerance: Numerical tolerance for boundary detection

    Returns:
        Tuple[float, float]: (μ^L, μ^U)

    Mathematical Source:
        Theorem 5, complementary slackness
    """
    # Lagrangian gradient: ∂V_i/∂I_i - ψ'(I_i)
    lagrangian_grad = dV_dI - psi_prime

    # Case 1: Lower bound active (I_i ≈ 0)
    if I_i < tolerance:
        mu_L = max(0.0, lagrangian_grad)  # μ^L ≥ 0
        mu_U = 0.0
        return mu_L, mu_U

    # Case 2: Upper bound active (I_i ≈ Ī)
    if abs(I_i - I_bar) < tolerance:
        mu_L = 0.0
        mu_U = max(0.0, -lagrangian_grad)  # μ^U ≥ 0
        return mu_L, mu_U

    # Case 3: Interior solution (0 < I_i < Ī)
    mu_L = 0.0
    mu_U = 0.0
    return mu_L, mu_U


def verify_kkt_conditions(
    I_1_star: float,
    I_2_star: float,
    params: Parameters,
    rng: np.random.Generator,
    h: float = 1e-5,
    tolerance: float = 1e-4
) -> KKTDiagnostics:
    """Verify KKT necessary conditions for Nash equilibrium (Theorem 5).

    Checks all four KKT conditions:
    1. Stationarity: ∂V_i/∂I_i - ψ'(I_i) - μ_i^L + μ_i^U = 0
    2. Primal feasibility: 0 ≤ I_i ≤ Ī
    3. Dual feasibility: μ_i^L, μ_i^U ≥ 0
    4. Complementary slackness: μ_i^L·I_i = 0, μ_i^U·(Ī - I_i) = 0

    Args:
        I_1_star: Leader's equilibrium investment
        I_2_star: Follower's equilibrium investment
        params: Model parameters
        rng: Random number generator
        h: Step size for numerical derivatives
        tolerance: Numerical tolerance for verification

    Returns:
        KKTDiagnostics: Complete KKT diagnostics

    Mathematical Source:
        Theorem 5
    """
    I_bar = params.I_bar

    # ========== Firm 1 (Leader) ==========
    # Compute marginal value and cost
    dV1_dI1 = compute_marginal_value(1, I_1_star, I_2_star, params, rng, h)
    psi1_prime = compute_marginal_investment_cost(I_1_star, params.kappa_1)

    # Compute Lagrange multipliers
    mu_1_L, mu_1_U = compute_lagrange_multipliers(
        dV1_dI1, psi1_prime, I_1_star, I_bar, tolerance
    )

    # Check stationarity residual
    stationarity_1 = dV1_dI1 - psi1_prime - mu_1_L + mu_1_U

    # Check primal feasibility
    primal_feasible_1 = (0.0 <= I_1_star <= I_bar)

    # Check dual feasibility
    dual_feasible_1 = (mu_1_L >= -tolerance) and (mu_1_U >= -tolerance)

    # Check complementary slackness
    cs_lower_1 = abs(mu_1_L * I_1_star) < tolerance
    cs_upper_1 = abs(mu_1_U * (I_bar - I_1_star)) < tolerance
    comp_slack_1 = cs_lower_1 and cs_upper_1

    # Overall KKT satisfaction for firm 1
    kkt_1_satisfied = (
        abs(stationarity_1) < tolerance
        and primal_feasible_1
        and dual_feasible_1
        and comp_slack_1
    )

    firm_1_diagnostics = {
        'dV_dI': dV1_dI1,
        'psi_prime': psi1_prime,
        'mu_L': mu_1_L,
        'mu_U': mu_1_U,
        'stationarity_residual': stationarity_1,
        'primal_feasible': primal_feasible_1,
        'dual_feasible': dual_feasible_1,
        'complementary_slackness': comp_slack_1,
        'kkt_satisfied': kkt_1_satisfied,
    }

    # ========== Firm 2 (Follower) ==========
    # Compute marginal value and cost
    dV2_dI2 = compute_marginal_value(2, I_1_star, I_2_star, params, rng, h)
    psi2_prime = compute_marginal_investment_cost(I_2_star, params.kappa_2)

    # Compute Lagrange multipliers
    mu_2_L, mu_2_U = compute_lagrange_multipliers(
        dV2_dI2, psi2_prime, I_2_star, I_bar, tolerance
    )

    # Check stationarity residual
    stationarity_2 = dV2_dI2 - psi2_prime - mu_2_L + mu_2_U

    # Check primal feasibility
    primal_feasible_2 = (0.0 <= I_2_star <= I_bar)

    # Check dual feasibility
    dual_feasible_2 = (mu_2_L >= -tolerance) and (mu_2_U >= -tolerance)

    # Check complementary slackness
    cs_lower_2 = abs(mu_2_L * I_2_star) < tolerance
    cs_upper_2 = abs(mu_2_U * (I_bar - I_2_star)) < tolerance
    comp_slack_2 = cs_lower_2 and cs_upper_2

    # Overall KKT satisfaction for firm 2
    kkt_2_satisfied = (
        abs(stationarity_2) < tolerance
        and primal_feasible_2
        and dual_feasible_2
        and comp_slack_2
    )

    firm_2_diagnostics = {
        'dV_dI': dV2_dI2,
        'psi_prime': psi2_prime,
        'mu_L': mu_2_L,
        'mu_U': mu_2_U,
        'stationarity_residual': stationarity_2,
        'primal_feasible': primal_feasible_2,
        'dual_feasible': dual_feasible_2,
        'complementary_slackness': comp_slack_2,
        'kkt_satisfied': kkt_2_satisfied,
    }

    # Overall KKT satisfaction
    kkt_satisfied = kkt_1_satisfied and kkt_2_satisfied

    return KKTDiagnostics(
        I_1_star=I_1_star,
        I_2_star=I_2_star,
        firm_1=firm_1_diagnostics,
        firm_2=firm_2_diagnostics,
        kkt_satisfied=kkt_satisfied,
        tolerance=tolerance,
    )


def format_kkt_report(diagnostics: KKTDiagnostics) -> str:
    """Format KKT diagnostics as human-readable report.

    Args:
        diagnostics: KKT diagnostics from verify_kkt_conditions

    Returns:
        str: Formatted report
    """
    report = []
    report.append("=" * 80)
    report.append("KKT CONDITION VERIFICATION (Theorem 5)")
    report.append("=" * 80)
    report.append("")
    report.append(f"Nash Equilibrium: I₁* = {diagnostics.I_1_star:.6f}, I₂* = {diagnostics.I_2_star:.6f}")
    report.append(f"Tolerance: {diagnostics.tolerance:.2e}")
    report.append(f"Overall KKT Satisfied: {diagnostics.kkt_satisfied}")
    report.append("")

    # Firm 1
    report.append("-" * 80)
    report.append("FIRM 1 (Leader)")
    report.append("-" * 80)
    f1 = diagnostics.firm_1
    report.append(f"  ∂V₁/∂I₁         = {f1['dV_dI']:12.6f}")
    report.append(f"  ψ'(I₁)          = {f1['psi_prime']:12.6f}")
    report.append(f"  μ₁^L (lower)    = {f1['mu_L']:12.6f}")
    report.append(f"  μ₁^U (upper)    = {f1['mu_U']:12.6f}")
    report.append(f"  Stationarity residual: {f1['stationarity_residual']:12.6e}")
    report.append(f"  Primal feasible: {f1['primal_feasible']}")
    report.append(f"  Dual feasible: {f1['dual_feasible']}")
    report.append(f"  Complementary slackness: {f1['complementary_slackness']}")
    report.append(f"  ✓ KKT satisfied: {f1['kkt_satisfied']}")
    report.append("")

    # Firm 2
    report.append("-" * 80)
    report.append("FIRM 2 (Follower)")
    report.append("-" * 80)
    f2 = diagnostics.firm_2
    report.append(f"  ∂V₂/∂I₂         = {f2['dV_dI']:12.6f}")
    report.append(f"  ψ'(I₂)          = {f2['psi_prime']:12.6f}")
    report.append(f"  μ₂^L (lower)    = {f2['mu_L']:12.6f}")
    report.append(f"  μ₂^U (upper)    = {f2['mu_U']:12.6f}")
    report.append(f"  Stationarity residual: {f2['stationarity_residual']:12.6e}")
    report.append(f"  Primal feasible: {f2['primal_feasible']}")
    report.append(f"  Dual feasible: {f2['dual_feasible']}")
    report.append(f"  Complementary slackness: {f2['complementary_slackness']}")
    report.append(f"  ✓ KKT satisfied: {f2['kkt_satisfied']}")
    report.append("")

    report.append("=" * 80)

    return "\n".join(report)
