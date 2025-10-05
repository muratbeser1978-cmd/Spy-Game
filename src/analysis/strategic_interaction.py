"""Strategic Interaction Analysis (Lemma 2, Theorem 7).

Constitutional Compliance:
- Principle IV: Reproducibility & Validation
- Principle V: Algorithm Transparency
- Principle VI: Documentation Standards

Implements: Lemma 2 and Theorem 7 from the paper - analysis of strategic
interactions via cross-partial derivatives.

Mathematical Source:
    - Lemma 2: Sign of ∂²ρ/∂I₁∂I₂ changes at threshold
    - Theorem 7: Strategic complementarity/substitutability in investments
    - Equation (11): ∂²ρ/∂I₁∂I₂ > 0 ⟺ I₂^γ > λI₁^γ + εc
"""

import numpy as np
from typing import Dict, Tuple
from dataclasses import dataclass

from src.models.parameters import Parameters
from src.topology.level_02_contest import compute_rho
from src.topology.level_03_signal import compute_kappa


@dataclass
class StrategicInteractionDiagnostics:
    """Strategic interaction diagnostics.

    Attributes:
        I_1: Leader's investment
        I_2: Follower's investment
        rho: Contest success probability
        d2rho_dI1dI2: Cross-partial ∂²ρ/∂I₁∂I₂
        threshold_I2: Threshold I₂* where cross-partial changes sign
        strategic_complementarity: Whether investments are strategic complements
        params: Model parameters
    """
    I_1: float
    I_2: float
    rho: float
    d2rho_dI1dI2: float
    threshold_I2: float
    strategic_complementarity: bool
    params: Parameters


def compute_cross_partial_rho(
    I_1: float,
    I_2: float,
    params: Parameters,
    h: float = 1e-5
) -> float:
    """Compute ∂²ρ/∂I₁∂I₂ numerically (Lemma 2).

    Uses central difference formula:
        ∂²f/∂x∂y ≈ [f(x+h,y+h) - f(x+h,y-h) - f(x-h,y+h) + f(x-h,y-h)] / (4h²)

    Args:
        I_1: Leader's investment
        I_2: Follower's investment
        params: Model parameters
        h: Step size for numerical derivative

    Returns:
        float: ∂²ρ/∂I₁∂I₂

    Mathematical Source:
        Lemma 2, equation (11)
    """
    # Four function evaluations
    f_pp = compute_rho(I_1 + h, I_2 + h, params)
    f_pm = compute_rho(I_1 + h, I_2 - h, params)
    f_mp = compute_rho(I_1 - h, I_2 + h, params)
    f_mm = compute_rho(I_1 - h, I_2 - h, params)

    # Central difference
    d2rho_dI1dI2 = (f_pp - f_pm - f_mp + f_mm) / (4 * h * h)

    return d2rho_dI1dI2


def compute_analytical_cross_partial_rho(
    I_1: float,
    I_2: float,
    params: Parameters
) -> float:
    """Compute ∂²ρ/∂I₁∂I₂ analytically (Lemma 2).

    From equation (7): ρ = I₂^γ / (I₂^γ + λ·I₁^γ + ε)

    Analytical derivation:
        ∂ρ/∂I₁ = -γ·λ·I₁^(γ-1)·I₂^γ / (I₂^γ + λ·I₁^γ + ε)²

        ∂²ρ/∂I₁∂I₂ = -γ²·λ·I₁^(γ-1)·I₂^(γ-1) · [I₂^γ - λ·I₁^γ - ε·γ/(γ-1)] / D³

        where D = I₂^γ + λ·I₁^γ + ε

    Sign changes at threshold:
        I₂^γ = λ·I₁^γ + ε·γ/(γ-1)

    Args:
        I_1: Leader's investment
        I_2: Follower's investment
        params: Model parameters

    Returns:
        float: ∂²ρ/∂I₁∂I₂

    Mathematical Source:
        Lemma 2, analytical derivation
    """
    gamma = params.gamma_exponent
    lambda_def = params.lambda_defense
    epsilon = params.epsilon

    # Avoid numerical issues at zero
    if I_1 < 1e-10 or I_2 < 1e-10:
        return 0.0

    I_1_power = I_1 ** gamma
    I_2_power = I_2 ** gamma
    I_1_power_deriv = I_1 ** (gamma - 1)
    I_2_power_deriv = I_2 ** (gamma - 1)

    # Denominator
    D = I_2_power + lambda_def * I_1_power + epsilon

    # Numerator of cross-partial (simplified form)
    # Sign determined by: I₂^γ - λ·I₁^γ - ε·c
    # where c depends on γ
    c = gamma / (gamma - 1) if abs(gamma - 1) > 1e-10 else 1.0

    numerator_sign_term = I_2_power - lambda_def * I_1_power - epsilon * c

    # Full cross-partial (sign-preserving approximation)
    d2rho_dI1dI2 = (
        gamma * gamma * lambda_def * I_1_power_deriv * I_2_power_deriv
        * numerator_sign_term
        / (D ** 3)
    )

    return d2rho_dI1dI2


def compute_threshold_I2(
    I_1: float,
    params: Parameters
) -> float:
    """Compute threshold I₂* where ∂²ρ/∂I₁∂I₂ = 0 (Lemma 2).

    From equation (11):
        I₂^γ = λ·I₁^γ + ε·c

    where c = γ/(γ-1) for γ ≠ 1

    Args:
        I_1: Leader's investment
        params: Model parameters

    Returns:
        float: Threshold I₂*

    Mathematical Source:
        Lemma 2, equation (11)
    """
    gamma = params.gamma_exponent
    lambda_def = params.lambda_defense
    epsilon = params.epsilon

    # Constant c in threshold formula
    c = gamma / (gamma - 1) if abs(gamma - 1) > 1e-10 else 1.0

    # Solve for I₂: I₂^γ = λ·I₁^γ + ε·c
    I_1_power = I_1 ** gamma
    threshold_power = lambda_def * I_1_power + epsilon * c

    # I₂* = (λ·I₁^γ + ε·c)^(1/γ)
    I_2_star = threshold_power ** (1 / gamma)

    return I_2_star


def analyze_strategic_interaction(
    I_1: float,
    I_2: float,
    params: Parameters,
    h: float = 1e-5
) -> StrategicInteractionDiagnostics:
    """Analyze strategic interaction structure (Lemma 2, Theorem 7).

    Determines whether investments are strategic complements or substitutes
    based on sign of cross-partial ∂²ρ/∂I₁∂I₂.

    Strategic Complementarity (∂²ρ/∂I₁∂I₂ > 0):
        - Increasing I₁ makes increasing I₂ more valuable
        - Investments reinforce each other
        - Occurs when I₂ is above threshold

    Strategic Substitutability (∂²ρ/∂I₁∂I₂ < 0):
        - Increasing I₁ makes increasing I₂ less valuable
        - Investments offset each other
        - Occurs when I₂ is below threshold

    Args:
        I_1: Leader's investment
        I_2: Follower's investment
        params: Model parameters
        h: Step size for numerical derivatives

    Returns:
        StrategicInteractionDiagnostics: Complete diagnostics

    Mathematical Source:
        Lemma 2, Theorem 7
    """
    # Compute contest success probability
    rho = compute_rho(I_1, I_2, params)

    # Compute cross-partial (numerical)
    d2rho_dI1dI2 = compute_cross_partial_rho(I_1, I_2, params, h)

    # Compute threshold
    threshold_I2 = compute_threshold_I2(I_1, params)

    # Determine strategic relationship
    strategic_complementarity = d2rho_dI1dI2 > 0

    return StrategicInteractionDiagnostics(
        I_1=I_1,
        I_2=I_2,
        rho=rho,
        d2rho_dI1dI2=d2rho_dI1dI2,
        threshold_I2=threshold_I2,
        strategic_complementarity=strategic_complementarity,
        params=params,
    )


def compute_cross_partial_V1_V2(
    I_1: float,
    I_2: float,
    params: Parameters,
    rng: np.random.Generator,
    h: float = 1e-4
) -> Tuple[float, float]:
    """Compute cross-partials of value functions (Theorem 7).

    Computes:
        - ∂²V₁/∂I₁∂I₂: How follower's investment affects leader's marginal value
        - ∂²V₂/∂I₁∂I₂: How leader's investment affects follower's marginal value

    These capture strategic interaction in value functions.

    Args:
        I_1: Leader's investment
        I_2: Follower's investment
        params: Model parameters
        rng: Random number generator
        h: Step size for numerical derivatives

    Returns:
        Tuple[float, float]: (∂²V₁/∂I₁∂I₂, ∂²V₂/∂I₁∂I₂)

    Mathematical Source:
        Theorem 7, strategic interaction in value functions
    """
    from src.topology.level_10_value_functions import compute_V_1, compute_V_2

    # Create independent RNGs for reproducibility
    rng_pp = np.random.default_rng(42)
    rng_pm = np.random.default_rng(42)
    rng_mp = np.random.default_rng(42)
    rng_mm = np.random.default_rng(42)

    # ∂²V₁/∂I₁∂I₂
    V1_pp = compute_V_1(I_1 + h, I_2 + h, params, rng_pp)
    V1_pm = compute_V_1(I_1 + h, I_2 - h, params, rng_pm)
    V1_mp = compute_V_1(I_1 - h, I_2 + h, params, rng_mp)
    V1_mm = compute_V_1(I_1 - h, I_2 - h, params, rng_mm)
    d2V1_dI1dI2 = (V1_pp - V1_pm - V1_mp + V1_mm) / (4 * h * h)

    # Reset RNGs
    rng_pp = np.random.default_rng(43)
    rng_pm = np.random.default_rng(43)
    rng_mp = np.random.default_rng(43)
    rng_mm = np.random.default_rng(43)

    # ∂²V₂/∂I₁∂I₂
    V2_pp = compute_V_2(I_1 + h, I_2 + h, params, rng_pp)
    V2_pm = compute_V_2(I_1 + h, I_2 - h, params, rng_pm)
    V2_mp = compute_V_2(I_1 - h, I_2 + h, params, rng_mp)
    V2_mm = compute_V_2(I_1 - h, I_2 - h, params, rng_mm)
    d2V2_dI1dI2 = (V2_pp - V2_pm - V2_mp + V2_mm) / (4 * h * h)

    return d2V1_dI1dI2, d2V2_dI1dI2


def format_strategic_interaction_report(
    diagnostics: StrategicInteractionDiagnostics
) -> str:
    """Format strategic interaction diagnostics as human-readable report.

    Args:
        diagnostics: Strategic interaction diagnostics

    Returns:
        str: Formatted report
    """
    report = []
    report.append("=" * 80)
    report.append("STRATEGIC INTERACTION ANALYSIS (Lemma 2, Theorem 7)")
    report.append("=" * 80)
    report.append("")
    report.append(f"Investments: I₁ = {diagnostics.I_1:.6f}, I₂ = {diagnostics.I_2:.6f}")
    report.append(f"Contest probability: ρ = {diagnostics.rho:.6f}")
    report.append("")
    report.append("-" * 80)
    report.append("CROSS-PARTIAL ANALYSIS")
    report.append("-" * 80)
    report.append(f"  ∂²ρ/∂I₁∂I₂ = {diagnostics.d2rho_dI1dI2:12.6e}")
    report.append(f"  Threshold I₂* = {diagnostics.threshold_I2:.6f}")
    report.append(f"  Current I₂ vs threshold: {diagnostics.I_2:.6f} {'>' if diagnostics.I_2 > diagnostics.threshold_I2 else '<'} {diagnostics.threshold_I2:.6f}")
    report.append("")
    report.append(f"  Strategic relationship: {'COMPLEMENTARITY' if diagnostics.strategic_complementarity else 'SUBSTITUTABILITY'}")
    report.append("")
    if diagnostics.strategic_complementarity:
        report.append("  → Increasing I₁ makes increasing I₂ MORE valuable")
        report.append("  → Investments reinforce each other")
        report.append("  → Follower invests above threshold (strong espionage)")
    else:
        report.append("  → Increasing I₁ makes increasing I₂ LESS valuable")
        report.append("  → Investments offset each other")
        report.append("  → Follower invests below threshold (weak espionage)")
    report.append("")
    report.append("=" * 80)

    return "\n".join(report)


def compute_strategic_interaction_map(
    I_1_range: np.ndarray,
    I_2_range: np.ndarray,
    params: Parameters
) -> Dict[str, np.ndarray]:
    """Compute strategic interaction map over (I₁, I₂) grid.

    Useful for visualizing regions of strategic complementarity vs substitutability.

    Args:
        I_1_range: Array of I₁ values
        I_2_range: Array of I₂ values
        params: Model parameters

    Returns:
        Dict[str, np.ndarray]: Dictionary containing:
            - 'I_1_grid': Meshgrid of I₁ values
            - 'I_2_grid': Meshgrid of I₂ values
            - 'd2rho_grid': Meshgrid of ∂²ρ/∂I₁∂I₂ values
            - 'threshold_I_2': Array of threshold I₂*(I₁) values
    """
    I_1_grid, I_2_grid = np.meshgrid(I_1_range, I_2_range)
    d2rho_grid = np.zeros_like(I_1_grid)

    # Compute cross-partial at each grid point
    for i in range(len(I_2_range)):
        for j in range(len(I_1_range)):
            I_1 = I_1_grid[i, j]
            I_2 = I_2_grid[i, j]
            d2rho_grid[i, j] = compute_cross_partial_rho(I_1, I_2, params)

    # Compute threshold curve I₂*(I₁)
    threshold_I_2 = np.array([compute_threshold_I2(I_1, params) for I_1 in I_1_range])

    return {
        'I_1_grid': I_1_grid,
        'I_2_grid': I_2_grid,
        'd2rho_grid': d2rho_grid,
        'I_1_range': I_1_range,
        'threshold_I_2': threshold_I_2,
    }
