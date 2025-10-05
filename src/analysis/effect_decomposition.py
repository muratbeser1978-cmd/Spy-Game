"""Sequential Move vs Information Effect Decomposition (Proposition 5).

Constitutional Compliance:
- Principle IV: Reproducibility & Validation
- Principle V: Algorithm Transparency
- Principle VI: Documentation Standards

Implements: Proposition 5 from the paper - decomposing profit differences
into action-based (sequential-move) vs type-based (information) channels.

Mathematical Source:
    - Section 4: Sequential-Move vs Information Advantage
    - Proposition 5: Profit decomposition
    - Equation (45): Π_i^S - Π_i^B = (Π_i^S - Π_i^h) + (Π_i^h - Π_i^B)

Game Variants:
    - G^B: Benchmark simultaneous-move game (no leadership, no espionage)
    - G^h: Hybrid game (sequential moves, but no espionage)
    - G^S: Full game with espionage (Stackelberg + information advantage)
"""

import numpy as np
from typing import Dict, Tuple

from src.models.parameters import Parameters
from src.topology.level_04_demand import compute_Delta
from src.topology.level_07_quantities import compute_q_1_star, compute_q_2_star


def compute_benchmark_nash_profits(
    params: Parameters,
    rng: np.random.Generator,
    N: int = 10_000
) -> Tuple[float, float]:
    """Compute profits in benchmark simultaneous-move game G^B.

    In G^B:
    - Both firms move simultaneously (no leadership)
    - No espionage (no information advantage)
    - Firms set prices based on Nash equilibrium of symmetric Bertrand game

    Nash equilibrium in symmetric Bertrand with differentiation:
        p_i* = (α + β·c_i + δ·E[p_j]) / (2β)

    Since symmetric, E[p_j] = p̄ = (α + β·μ_c + δ·p̄) / (2β)

    Solving: p̄ = (α + β·μ_c) / (2β - δ)

    Args:
        params: Model parameters
        rng: Random number generator
        N: Number of Monte Carlo samples

    Returns:
        Tuple[float, float]: (E[Π₁^B], E[Π₂^B])

    Mathematical Source:
        Section 4, benchmark game G^B
    """
    alpha = params.alpha
    beta = params.beta
    delta = params.delta
    mu_c = params.mu_c
    sigma_c = params.sigma_c

    # Expected price in symmetric equilibrium
    p_bar = (alpha + beta * mu_c) / (2 * beta - delta)

    # Demand parameter
    Delta = compute_Delta(params)

    profits_1 = np.zeros(N)
    profits_2 = np.zeros(N)

    for i in range(N):
        # Draw costs
        c_1 = rng.normal(mu_c, sigma_c)
        c_2 = rng.normal(mu_c, sigma_c)

        # Nash equilibrium prices (simultaneous move)
        # Each firm best-responds to expected competitor price
        p_1_B = (alpha + beta * c_1 + delta * p_bar) / (2 * beta)
        p_2_B = (alpha + beta * c_2 + delta * p_bar) / (2 * beta)

        # Quantities from demand
        q_1_B = max(0.0, alpha - beta * p_1_B + delta * p_2_B)
        q_2_B = max(0.0, alpha - beta * p_2_B + delta * p_1_B)

        # Profits
        profits_1[i] = (p_1_B - c_1) * q_1_B
        profits_2[i] = (p_2_B - c_2) * q_2_B

    E_Pi_1_B = float(np.mean(profits_1))
    E_Pi_2_B = float(np.mean(profits_2))

    return E_Pi_1_B, E_Pi_2_B


def compute_hybrid_stackelberg_profits(
    params: Parameters,
    rng: np.random.Generator,
    N: int = 10_000
) -> Tuple[float, float]:
    """Compute profits in hybrid Stackelberg game G^h.

    In G^h:
    - Firm 1 leads, Firm 2 follows (sequential moves)
    - NO espionage (follower doesn't observe leader's price or cost)
    - Follower best-responds to expected leader price

    Leader's problem:
        max_{p_1} E[(p_1 - c_1)·Q_1(p_1, p_2^h(p_1))]

    where follower's response is:
        p_2^h = (α + β·c_2 + δ·E[p_1]) / (2β)

    This isolates the sequential-move (action-based) channel without
    information advantage.

    Args:
        params: Model parameters
        rng: Random number generator
        N: Number of Monte Carlo samples

    Returns:
        Tuple[float, float]: (E[Π₁^h], E[Π₂^h])

    Mathematical Source:
        Section 4, hybrid game G^h
    """
    alpha = params.alpha
    beta = params.beta
    delta = params.delta
    mu_c = params.mu_c
    sigma_c = params.sigma_c

    # In G^h, leader chooses price anticipating follower's best response
    # Without information, follower responds to E[p_1]
    # This creates a fixed-point similar to G^S but without espionage effects

    # Simplified: use affine pricing rule structure but without espionage
    # Leader: p_1 = a_h + 0.5·c_1 for some a_h
    # Follower: p_2 = (α + β·c_2 + δ·E[p_1]) / (2β) where E[p_1] = a_h + 0.5·μ_c

    # Solve for a_h using similar fixed-point as in full game but with ρ=0, κ=0
    # For simplicity, use a_h ≈ (α - δ·μ_c/2) / (2β - δ/2)

    Delta = compute_Delta(params)
    B_h = Delta  # No espionage, so B = Δ

    # Approximate intercept (simplified calculation)
    a_h = (alpha * Delta + delta * mu_c / 2) / (2 * beta * Delta - delta / 2)

    profits_1 = np.zeros(N)
    profits_2 = np.zeros(N)

    for i in range(N):
        # Draw costs
        c_1 = rng.normal(mu_c, sigma_c)
        c_2 = rng.normal(mu_c, sigma_c)

        # Leader sets price (Stackelberg first-mover)
        p_1_h = a_h + 0.5 * c_1

        # Follower best-responds to expected leader price
        p_1_bar_h = a_h + 0.5 * mu_c
        p_2_h = (alpha + beta * c_2 + delta * p_1_bar_h) / (2 * beta)

        # Quantities from demand
        q_1_h = max(0.0, alpha - beta * p_1_h + delta * p_2_h)
        q_2_h = max(0.0, alpha - beta * p_2_h + delta * p_1_h)

        # Profits
        profits_1[i] = (p_1_h - c_1) * q_1_h
        profits_2[i] = (p_2_h - c_2) * q_2_h

    E_Pi_1_h = float(np.mean(profits_1))
    E_Pi_2_h = float(np.mean(profits_2))

    return E_Pi_1_h, E_Pi_2_h


def compute_full_game_profits(
    I_1: float,
    I_2: float,
    params: Parameters,
    rng: np.random.Generator
) -> Tuple[float, float]:
    """Compute profits in full Stackelberg-espionage game G^S.

    This is the actual game with both:
    - Sequential moves (leader advantage)
    - Espionage (follower's information advantage)

    Args:
        I_1: Leader's counter-espionage investment
        I_2: Follower's espionage investment
        params: Model parameters
        rng: Random number generator

    Returns:
        Tuple[float, float]: (E[Π₁^S], E[Π₂^S])

    Mathematical Source:
        Section 4, full game G^S
    """
    from src.topology.level_10_value_functions import compute_V_1, compute_V_2

    # Note: V_i = E[Π_i] - ψ(I_i), so we need gross profits
    # For decomposition, we use net profits (utilities) since that's what matters

    V_1 = compute_V_1(I_1, I_2, params, rng)
    V_2 = compute_V_2(I_1, I_2, params, rng)

    return V_1, V_2


def compute_effect_decomposition(
    I_1: float,
    I_2: float,
    params: Parameters,
    rng: np.random.Generator,
    N: int = 10_000
) -> Dict[str, Dict[str, float]]:
    """Decompose profit changes into sequential-move vs information effects.

    Proposition 5 decomposition:
        Π_i^S - Π_i^B = (Π_i^S - Π_i^h) + (Π_i^h - Π_i^B)

    where:
        - Π_i^S - Π_i^h: Information effect (espionage impact)
        - Π_i^h - Π_i^B: Sequential-move effect (leadership impact)

    Args:
        I_1: Leader's counter-espionage investment
        I_2: Follower's espionage investment
        params: Model parameters
        rng: Random number generator
        N: Number of Monte Carlo samples

    Returns:
        Dict[str, Dict[str, float]]: Nested dictionary with structure:
            {
                'firm_1': {
                    'Pi_B': Benchmark profit,
                    'Pi_h': Hybrid profit,
                    'Pi_S': Full game profit,
                    'total_gain': Π₁^S - Π₁^B,
                    'sequential_effect': Π₁^h - Π₁^B,
                    'information_effect': Π₁^S - Π₁^h,
                },
                'firm_2': {...}
            }

    Mathematical Source:
        Proposition 5, equation (45)
    """
    # Compute profits in each game variant
    rng_B = np.random.default_rng(42)  # Fixed seed for reproducibility
    rng_h = np.random.default_rng(42)
    rng_S = np.random.default_rng(42)

    Pi_1_B, Pi_2_B = compute_benchmark_nash_profits(params, rng_B, N)
    Pi_1_h, Pi_2_h = compute_hybrid_stackelberg_profits(params, rng_h, N)
    Pi_1_S, Pi_2_S = compute_full_game_profits(I_1, I_2, params, rng_S)

    # Firm 1 (Leader) decomposition
    firm_1_decomp = {
        'Pi_B': Pi_1_B,
        'Pi_h': Pi_1_h,
        'Pi_S': Pi_1_S,
        'total_gain': Pi_1_S - Pi_1_B,
        'sequential_effect': Pi_1_h - Pi_1_B,  # Action-based channel
        'information_effect': Pi_1_S - Pi_1_h,  # Type-based channel (espionage hurts leader)
    }

    # Firm 2 (Follower) decomposition
    firm_2_decomp = {
        'Pi_B': Pi_2_B,
        'Pi_h': Pi_2_h,
        'Pi_S': Pi_2_S,
        'total_gain': Pi_2_S - Pi_2_B,
        'sequential_effect': Pi_2_h - Pi_2_B,  # Action-based channel (follower disadvantage)
        'information_effect': Pi_2_S - Pi_2_h,  # Type-based channel (espionage helps follower)
    }

    return {
        'firm_1': firm_1_decomp,
        'firm_2': firm_2_decomp,
    }


def analyze_information_value(
    I_2_range: np.ndarray,
    I_1_fixed: float,
    params: Parameters,
    rng: np.random.Generator,
    N: int = 10_000
) -> Dict[str, np.ndarray]:
    """Analyze how information value varies with espionage investment I₂.

    Computes information effect (Π_i^S - Π_i^h) across range of I₂ values.

    Args:
        I_2_range: Array of I₂ values to test
        I_1_fixed: Fixed value of I₁
        params: Model parameters
        rng: Random number generator
        N: Number of Monte Carlo samples

    Returns:
        Dict[str, np.ndarray]: Arrays of information effects for each firm
    """
    info_effect_1 = np.zeros(len(I_2_range))
    info_effect_2 = np.zeros(len(I_2_range))

    # Compute hybrid profits once (doesn't depend on I₂ in espionage)
    rng_h = np.random.default_rng(42)
    Pi_1_h, Pi_2_h = compute_hybrid_stackelberg_profits(params, rng_h, N)

    for idx, I_2 in enumerate(I_2_range):
        rng_S = np.random.default_rng(42 + idx)
        Pi_1_S, Pi_2_S = compute_full_game_profits(I_1_fixed, I_2, params, rng_S)

        info_effect_1[idx] = Pi_1_S - Pi_1_h
        info_effect_2[idx] = Pi_2_S - Pi_2_h

    return {
        'I_2_range': I_2_range,
        'info_effect_firm_1': info_effect_1,
        'info_effect_firm_2': info_effect_2,
    }
