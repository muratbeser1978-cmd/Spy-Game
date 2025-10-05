"""Level 12: Interim Profit Functions (Theorem 4).

Constitutional Compliance:
- Principle I: Mathematical Fidelity (notation matches paper)
- Principle VI: Documentation Standards (equation references)

Implements: Theorem 4 from the paper - closed-form interim profit expressions.

Mathematical Source:
    - Theorem 4: Interim profit formulas
    - Equation (33): Π₁*(c₁; I₁, I₂) = (p₁* - c₁)² · B_{ρ,κ}
    - Equation (34): Π₂*(I₁, I₂) = Π₂^U + ρ · ΔΠ₂^Info(κ)
    - Equation (35): ΔΠ₂^Info(κ) = (δ²/(16β)) · κ · σ_c²
"""

import numpy as np

from src.models.parameters import Parameters
from src.topology.level_02_contest import compute_rho
from src.topology.level_03_signal import compute_kappa
from src.topology.level_04_demand import compute_Delta
from src.topology.level_05_intercept_components import compute_B_rho_kappa
from src.topology.level_06_fixed_point_intercept import compute_a_rho_kappa
from src.topology.level_05_intercept_components import (
    compute_numerator_a,
    compute_denominator_a,
)


def compute_Pi_1_interim(
    c_1: float,
    a_rho_kappa: float,
    B_rho_kappa: float,
    params: Parameters
) -> float:
    """Compute leader's interim profit (Theorem 4, equation 33).

    Π₁*(c₁; I₁, I₂) = (p₁* - c₁)² · B_{ρ,κ}

    where p₁* = a_{ρ,κ} + 0.5·c₁ (equation 30)

    This is the profit conditional on realized cost c₁, before market clears.

    Args:
        c_1: Leader's realized marginal cost
        a_rho_kappa: Fixed-point intercept a_{ρ,κ}
        B_rho_kappa: Bayesian updating component B_{ρ,κ}
        params: Model parameters

    Returns:
        float: Interim profit Π₁*(c₁)

    Mathematical Source:
        Theorem 4, equation (33)
    """
    # Leader's price (equation 30)
    p_1_star = a_rho_kappa + 0.5 * c_1

    # Price-cost markup
    markup = p_1_star - c_1

    # Interim profit (equation 33)
    Pi_1_interim = (markup ** 2) * B_rho_kappa

    return Pi_1_interim


def compute_Pi_2_uninformed(
    p_1_bar: float,
    c_2: float,
    params: Parameters
) -> float:
    """Compute follower's uninformed profit Π₂^U.

    This is the profit when espionage fails (no signal received).

    Π₂^U = (p₂^U - c₂)² · Δ

    where p₂^U = (α + β·c₂ + δ·p̄₁*)/(2β) (equation 22)

    Args:
        p_1_bar: Expected leader price p̄₁* = a_{ρ,κ} + 0.5·μ_c
        c_2: Follower's realized marginal cost
        params: Model parameters

    Returns:
        float: Uninformed profit Π₂^U

    Mathematical Source:
        Theorem 4 (building block for equation 34)
    """
    alpha = params.alpha
    beta = params.beta
    delta = params.delta

    # Uninformed price (equation 22)
    p_2_U = (alpha + beta * c_2 + delta * p_1_bar) / (2 * beta)

    # Markup
    markup = p_2_U - c_2

    # Compute Δ = β - δ²/β (equation 20)
    Delta = compute_Delta(params)

    # Uninformed profit
    Pi_2_U = (markup ** 2) * Delta

    return Pi_2_U


def compute_Delta_Pi_2_info(
    kappa: float,
    params: Parameters
) -> float:
    """Compute information value for follower (Theorem 4, equation 35).

    ΔΠ₂^Info(κ) = (δ²/(16β)) · κ · σ_c²

    This represents the expected profit gain from successful espionage.

    Args:
        kappa: Signal reliability weight κ ∈ [0,1]
        params: Model parameters

    Returns:
        float: Information value ΔΠ₂^Info(κ)

    Mathematical Source:
        Theorem 4, equation (35)
    """
    delta = params.delta
    beta = params.beta
    sigma_c_squared = params.sigma_c ** 2

    # Information value (equation 35)
    Delta_Pi_2_info = (delta ** 2 / (16 * beta)) * kappa * sigma_c_squared

    return Delta_Pi_2_info


def compute_Pi_2_interim(
    rho: float,
    kappa: float,
    p_1_bar: float,
    c_2: float,
    params: Parameters
) -> float:
    """Compute follower's interim profit (Theorem 4, equation 34).

    Π₂*(I₁, I₂) = Π₂^U + ρ · ΔΠ₂^Info(κ)

    This decomposes follower's profit into:
    - Π₂^U: Baseline profit without information
    - ρ · ΔΠ₂^Info(κ): Expected information gain from espionage

    Args:
        rho: Espionage success probability ρ(I₁, I₂)
        kappa: Signal reliability κ(I₂)
        p_1_bar: Expected leader price p̄₁*
        c_2: Follower's realized marginal cost
        params: Model parameters

    Returns:
        float: Interim profit Π₂*

    Mathematical Source:
        Theorem 4, equation (34)
    """
    # Uninformed profit (baseline)
    Pi_2_U = compute_Pi_2_uninformed(p_1_bar, c_2, params)

    # Information value
    Delta_Pi_2_info = compute_Delta_Pi_2_info(kappa, params)

    # Total interim profit (equation 34)
    Pi_2_interim = Pi_2_U + rho * Delta_Pi_2_info

    return Pi_2_interim


def compute_expected_Pi_1(
    I_1: float,
    I_2: float,
    params: Parameters,
    rng: np.random.Generator,
    N: int = 10_000
) -> float:
    """Compute expected leader profit via Monte Carlo over cost draws.

    E[Π₁*] = E_{c₁}[(p₁*(c₁) - c₁)² · B_{ρ,κ}]

    Args:
        I_1: Leader's investment
        I_2: Follower's investment
        params: Model parameters
        rng: Random number generator
        N: Number of Monte Carlo samples

    Returns:
        float: Expected profit E[Π₁*]
    """
    # Compute equilibrium parameters
    rho = compute_rho(I_1, I_2, params)
    kappa = compute_kappa(I_2, params)
    Delta = compute_Delta(params)
    B_rho_kappa = compute_B_rho_kappa(rho, kappa, params)

    numerator = compute_numerator_a(rho, kappa, Delta, params)
    denominator = compute_denominator_a(rho, kappa, Delta, B_rho_kappa, params)
    a_rho_kappa, _, _ = compute_a_rho_kappa(
        rho, kappa, B_rho_kappa, numerator, denominator, params
    )

    # Monte Carlo over cost draws
    profits = np.zeros(N)
    for i in range(N):
        c_1 = rng.normal(params.mu_c, params.sigma_c)
        profits[i] = compute_Pi_1_interim(c_1, a_rho_kappa, B_rho_kappa, params)

    return float(np.mean(profits))


def compute_expected_Pi_2(
    I_1: float,
    I_2: float,
    params: Parameters,
    rng: np.random.Generator,
    N: int = 10_000
) -> float:
    """Compute expected follower profit via Monte Carlo over cost draws.

    E[Π₂*] = E_{c₂}[Π₂^U + ρ · ΔΠ₂^Info(κ)]

    Args:
        I_1: Leader's investment
        I_2: Follower's investment
        params: Model parameters
        rng: Random number generator
        N: Number of Monte Carlo samples

    Returns:
        float: Expected profit E[Π₂*]
    """
    # Compute equilibrium parameters
    rho = compute_rho(I_1, I_2, params)
    kappa = compute_kappa(I_2, params)
    Delta = compute_Delta(params)
    B_rho_kappa = compute_B_rho_kappa(rho, kappa, params)

    numerator = compute_numerator_a(rho, kappa, Delta, params)
    denominator = compute_denominator_a(rho, kappa, Delta, B_rho_kappa, params)
    a_rho_kappa, _, _ = compute_a_rho_kappa(
        rho, kappa, B_rho_kappa, numerator, denominator, params
    )

    p_1_bar = a_rho_kappa + 0.5 * params.mu_c

    # Monte Carlo over cost draws
    profits = np.zeros(N)
    for i in range(N):
        c_2 = rng.normal(params.mu_c, params.sigma_c)
        profits[i] = compute_Pi_2_interim(rho, kappa, p_1_bar, c_2, params)

    return float(np.mean(profits))
