"""Level 10: Stage 3 Value Functions via Monte Carlo - COMPLETELY REWRITTEN.

Now follows correct game sequence:
1. Leader's private cost c₁ ~ N(μ_c, σ_c²) drawn (RANDOM - target of espionage!)
2. Follower's public cost c₂ = γ (FIXED - known to all)
3. Leader sets p₁* = a + 0.5·c₁
4. Espionage succeeds with prob ρ
5. Follower observes noisy signal (if espionage succeeds)
6. Follower sets p₂* (best response using Bayesian updating)
7. Quantities determined from prices via demand
8. Profits computed

This is the CORRECT Stackelberg-Bayesian game with asymmetric information!
"""

import numpy as np

from src.models.parameters import Parameters
from src.topology.level_02_contest import compute_rho
from src.topology.level_03_signal import compute_kappa
from src.topology.level_06_fixed_point_intercept import compute_a_rho_kappa
from src.topology.level_04_demand import compute_Delta
from src.topology.level_05_intercept_components import (
    compute_B_rho_kappa,
    compute_numerator_a,
    compute_denominator_a,
)
from src.topology.level_07_quantities import compute_q_1_star, compute_q_2_star
from src.topology.level_08_prices import compute_p_1_star, compute_p_2_star
from src.topology.level_09_profits import compute_pi_1_star, compute_pi_2_star


def compute_V_1(
    I_1: float, I_2: float, params: Parameters, rng: np.random.Generator
) -> float:
    """Compute leader's (Firm 1) expected profit - CORRECTED.

    Monte Carlo over cost realizations and espionage outcomes.

    Algorithm:
        For each sample:
            1. Draw (c₁, c₂) ~ N(μ_c, σ_c²)
            2. Leader sets p₁* = a_{ρ,κ} + 0.5·c₁
            3. Draw espionage outcome: success with prob ρ
            4. If success: draw noise ε, signal s = p₁* + ε
            5. Follower sets p₂* (using signal if available)
            6. Compute quantities from prices
            7. Compute leader's profit π₁*
        Return: E[π₁*]

    Args:
        I_1: Leader's counter-espionage investment
        I_2: Follower's espionage investment
        params: Model parameters
        rng: Random number generator (for reproducibility)

    Returns:
        float: Expected profit V₁(I₁,I₂)
    """
    N = 50_000  # Increased for lower variance in optimization

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

    # Prior mean of leader's price (for follower's prior)
    # Leader's cost is RANDOM ~ N(mu_c, sigma_c^2), so E[p_1] = a + 0.5*mu_c
    p_1_bar = a_rho_kappa + 0.5 * params.mu_c

    profits = np.zeros(N)

    for i in range(N):
        # 1. Draw costs
        # CORRECTED: Leader (Firm 1) has RANDOM private cost, Follower (Firm 2) has FIXED public cost
        c_1 = rng.normal(params.mu_c, params.sigma_c)  # Leader's cost is RANDOM (private info - target of espionage!)
        c_2 = params.gamma  # Follower's cost is FIXED (public knowledge)

        # 2. Leader sets price
        p_1 = compute_p_1_star(a_rho_kappa, c_1)

        # 3. Espionage outcome
        espionage_succeeds = rng.random() < rho

        # 4. Generate signal if espionage succeeds
        if espionage_succeeds:
            noise_std = params.sigma_epsilon / np.sqrt(I_2 + params.iota)
            noise = rng.normal(0, noise_std)
            signal = p_1 + noise
        else:
            signal = 0.0  # Not used

        # 5. Follower sets price
        p_2 = compute_p_2_star(
            rho, kappa, p_1_bar, c_2, params,
            espionage_success=espionage_succeeds,
            signal=signal
        )

        # 6. Quantities from demand
        q_1 = compute_q_1_star(p_1, p_2, params)
        q_2 = compute_q_2_star(p_1, p_2, params)

        # 7. Leader's profit (price - cost) × quantity
        pi_1 = (p_1 - c_1) * q_1
        profits[i] = pi_1

    V_1 = float(np.mean(profits))
    return V_1


def compute_V_2(
    I_1: float, I_2: float, params: Parameters, rng: np.random.Generator
) -> float:
    """Compute follower's (Firm 2) expected profit - CORRECTED.

    Same Monte Carlo procedure as V_1 but tracking follower's profit.

    Args:
        I_1: Leader's counter-espionage investment
        I_2: Follower's espionage investment
        params: Model parameters
        rng: Random number generator

    Returns:
        float: Expected profit V₂(I₁,I₂)
    """
    N = 50_000  # Increased for lower variance in optimization

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

    # Leader's cost is RANDOM ~ N(mu_c, sigma_c^2), so E[p_1] = a + 0.5*mu_c
    p_1_bar = a_rho_kappa + 0.5 * params.mu_c

    profits = np.zeros(N)

    for i in range(N):
        # Same game sequence as V_1
        # CORRECTED: Leader (Firm 1) has RANDOM private cost, Follower (Firm 2) has FIXED public cost
        c_1 = rng.normal(params.mu_c, params.sigma_c)  # Leader's cost is RANDOM (private info - target of espionage!)
        c_2 = params.gamma  # Follower's cost is FIXED (public knowledge)

        p_1 = compute_p_1_star(a_rho_kappa, c_1)

        espionage_succeeds = rng.random() < rho

        if espionage_succeeds:
            noise_std = params.sigma_epsilon / np.sqrt(I_2 + params.iota)
            noise = rng.normal(0, noise_std)
            signal = p_1 + noise
        else:
            signal = 0.0

        p_2 = compute_p_2_star(
            rho, kappa, p_1_bar, c_2, params,
            espionage_success=espionage_succeeds,
            signal=signal
        )

        q_1 = compute_q_1_star(p_1, p_2, params)
        q_2 = compute_q_2_star(p_1, p_2, params)

        # Follower's profit (follower has zero cost in baseline)
        pi_2 = (p_2 - c_2) * q_2
        profits[i] = pi_2

    V_2 = float(np.mean(profits))
    return V_2
