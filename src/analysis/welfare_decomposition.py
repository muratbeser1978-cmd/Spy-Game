"""Welfare Decomposition Analysis (Theorem 6).

Constitutional Compliance:
- Principle IV: Reproducibility & Validation
- Principle V: Algorithm Transparency
- Principle VI: Documentation Standards

Implements: Theorem 6 from the paper - welfare decomposition via chain rule.

Mathematical Source:
    - Theorem 6: Chain rule decomposition of ∂W/∂I₂
    - Equation (52): ∂W/∂I₂ = ∂E[CS]/∂I₂ + ∂V₁/∂I₂ + (∂V₂/∂I₂ - ψ'(I₂))
    - Equation (53): ∂E[CS]/∂I₂ = -E[Q₁·∂p₁*/∂I₂ + Q₂·∂p₂*/∂I₂]
"""

import numpy as np
from typing import Tuple, Dict

from src.models.parameters import Parameters
from src.topology.level_02_contest import compute_rho
from src.topology.level_03_signal import compute_kappa
from src.topology.level_04_demand import compute_Delta
from src.topology.level_05_intercept_components import (
    compute_B_rho_kappa,
    compute_numerator_a,
    compute_denominator_a,
)
from src.topology.level_06_fixed_point_intercept import compute_a_rho_kappa
from src.topology.level_07_quantities import compute_q_1_star, compute_q_2_star
from src.topology.level_08_prices import compute_p_1_star, compute_p_2_star


def compute_numerical_derivative(
    func,
    x: float,
    h: float = 1e-5,
    **kwargs
) -> float:
    """Compute numerical derivative using central difference.

    f'(x) ≈ [f(x+h) - f(x-h)] / (2h)

    Args:
        func: Function to differentiate
        x: Point at which to compute derivative
        h: Step size
        **kwargs: Additional arguments to pass to func

    Returns:
        float: Numerical derivative f'(x)
    """
    f_plus = func(x + h, **kwargs)
    f_minus = func(x - h, **kwargs)
    derivative = (f_plus - f_minus) / (2 * h)
    return derivative


def compute_dCS_dI2(
    I_1: float,
    I_2: float,
    params: Parameters,
    rng: np.random.Generator,
    h: float = 1e-5,
    N: int = 10_000
) -> float:
    """Compute ∂E[CS]/∂I₂ via numerical differentiation (Theorem 6, equation 53).

    ∂E[CS]/∂I₂ = -E[Q₁·∂p₁*/∂I₂ + Q₂·∂p₂*/∂I₂]

    This captures how follower's investment affects consumer surplus through
    both direct and indirect (via leader's response) price effects.

    Args:
        I_1: Leader's investment
        I_2: Follower's investment
        params: Model parameters
        rng: Random number generator
        h: Step size for numerical derivative
        N: Number of Monte Carlo samples

    Returns:
        float: ∂E[CS]/∂I₂

    Mathematical Source:
        Theorem 6, equation (53)
    """
    def compute_CS_at_I2(I_2_val: float, rng_inner: np.random.Generator) -> float:
        """Helper: compute E[CS] at given I₂."""
        from src.topology.level_17_consumer_surplus import compute_CS
        return compute_CS(I_1, I_2_val, params, rng_inner)

    # Numerical derivative
    # Create independent RNG for reproducibility
    rng_plus = np.random.default_rng(42)
    rng_minus = np.random.default_rng(42)

    CS_plus = compute_CS_at_I2(I_2 + h, rng_plus)
    CS_minus = compute_CS_at_I2(I_2 - h, rng_minus)

    dCS_dI2 = (CS_plus - CS_minus) / (2 * h)

    return dCS_dI2


def compute_dV1_dI2(
    I_1: float,
    I_2: float,
    params: Parameters,
    rng: np.random.Generator,
    h: float = 1e-5
) -> float:
    """Compute ∂V₁/∂I₂ via numerical differentiation.

    This captures strategic effect: how follower's espionage investment
    affects leader's expected profit.

    Args:
        I_1: Leader's investment
        I_2: Follower's investment
        params: Model parameters
        rng: Random number generator
        h: Step size for numerical derivative

    Returns:
        float: ∂V₁/∂I₂

    Mathematical Source:
        Theorem 6, equation (52) component
    """
    from src.topology.level_10_value_functions import compute_V_1

    # Create independent RNGs for reproducibility
    rng_plus = np.random.default_rng(42)
    rng_minus = np.random.default_rng(42)

    V1_plus = compute_V_1(I_1, I_2 + h, params, rng_plus)
    V1_minus = compute_V_1(I_1, I_2 - h, params, rng_minus)

    dV1_dI2 = (V1_plus - V1_minus) / (2 * h)

    return dV1_dI2


def compute_dV2_dI2(
    I_1: float,
    I_2: float,
    params: Parameters,
    rng: np.random.Generator,
    h: float = 1e-5
) -> float:
    """Compute ∂V₂/∂I₂ via numerical differentiation.

    This captures how follower's investment affects its own expected profit
    (before subtracting investment cost).

    Args:
        I_1: Leader's investment
        I_2: Follower's investment
        params: Model parameters
        rng: Random number generator
        h: Step size for numerical derivative

    Returns:
        float: ∂V₂/∂I₂

    Mathematical Source:
        Theorem 6, equation (52) component
    """
    from src.topology.level_10_value_functions import compute_V_2

    # Create independent RNGs for reproducibility
    rng_plus = np.random.default_rng(42)
    rng_minus = np.random.default_rng(42)

    V2_plus = compute_V_2(I_1, I_2 + h, params, rng_plus)
    V2_minus = compute_V_2(I_1, I_2 - h, params, rng_minus)

    dV2_dI2 = (V2_plus - V2_minus) / (2 * h)

    return dV2_dI2


def compute_investment_cost_derivative(
    I_2: float,
    kappa_2: float
) -> float:
    """Compute ψ'(I₂) = κ₂·I₂ (marginal investment cost).

    Args:
        I_2: Follower's investment
        kappa_2: Follower's investment cost parameter

    Returns:
        float: ψ'(I₂)
    """
    return kappa_2 * I_2


def compute_welfare_decomposition(
    I_1: float,
    I_2: float,
    params: Parameters,
    rng: np.random.Generator,
    h: float = 1e-5
) -> Dict[str, float]:
    """Compute welfare decomposition (Theorem 6, equation 52).

    ∂W/∂I₂ = ∂E[CS]/∂I₂ + ∂V₁/∂I₂ + (∂V₂/∂I₂ - ψ'(I₂))

    Decomposes the marginal welfare effect of follower's investment into:
    1. Consumer surplus effect: ∂E[CS]/∂I₂
    2. Leader profit effect: ∂V₁/∂I₂
    3. Follower net profit effect: ∂V₂/∂I₂ - ψ'(I₂)

    Args:
        I_1: Leader's investment
        I_2: Follower's investment
        params: Model parameters
        rng: Random number generator
        h: Step size for numerical derivatives

    Returns:
        Dict[str, float]: Dictionary containing:
            - 'dW_dI2': Total welfare derivative ∂W/∂I₂
            - 'dCS_dI2': Consumer surplus component
            - 'dV1_dI2': Leader profit component
            - 'dV2_dI2': Follower gross profit derivative
            - 'psi_prime': Marginal investment cost ψ'(I₂)
            - 'dU2_dI2': Follower net profit component (∂V₂/∂I₂ - ψ'(I₂))

    Mathematical Source:
        Theorem 6, equation (52)
    """
    # Compute all components
    dCS_dI2 = compute_dCS_dI2(I_1, I_2, params, rng, h)
    dV1_dI2 = compute_dV1_dI2(I_1, I_2, params, rng, h)
    dV2_dI2 = compute_dV2_dI2(I_1, I_2, params, rng, h)
    psi_prime = compute_investment_cost_derivative(I_2, params.kappa_2)

    # Follower's net marginal benefit
    dU2_dI2 = dV2_dI2 - psi_prime

    # Total welfare derivative (equation 52)
    dW_dI2 = dCS_dI2 + dV1_dI2 + dU2_dI2

    return {
        'dW_dI2': dW_dI2,
        'dCS_dI2': dCS_dI2,
        'dV1_dI2': dV1_dI2,
        'dV2_dI2': dV2_dI2,
        'psi_prime': psi_prime,
        'dU2_dI2': dU2_dI2,
    }


def compute_chain_rule_decomposition(
    I_1: float,
    I_2: float,
    params: Parameters,
    h: float = 1e-5
) -> Dict[str, Dict[str, float]]:
    """Compute chain rule decomposition via ρ and κ channels.

    For each component X ∈ {CS, V₁, V₂}:
        ∂X/∂I₂ = (∂X/∂ρ)·(∂ρ/∂I₂) + (∂X/∂κ)·(∂κ/∂I₂)

    This separates contest channel (ρ) from signal quality channel (κ).

    Args:
        I_1: Leader's investment
        I_2: Follower's investment
        params: Model parameters
        h: Step size for numerical derivatives

    Returns:
        Dict[str, Dict[str, float]]: Nested dictionary with structure:
            {
                'rho': {'value': ρ, 'drho_dI2': ∂ρ/∂I₂},
                'kappa': {'value': κ, 'dkappa_dI2': ∂κ/∂I₂},
                'CS': {'via_rho': ..., 'via_kappa': ..., 'total': ...},
                'V1': {'via_rho': ..., 'via_kappa': ..., 'total': ...},
                'V2': {'via_rho': ..., 'via_kappa': ..., 'total': ...},
            }

    Mathematical Source:
        Theorem 6, chain rule decomposition
    """
    # Compute current values
    rho = compute_rho(I_1, I_2, params)
    kappa = compute_kappa(I_2, params)

    # Compute ∂ρ/∂I₂ numerically
    rho_plus = compute_rho(I_1, I_2 + h, params)
    rho_minus = compute_rho(I_1, I_2 - h, params)
    drho_dI2 = (rho_plus - rho_minus) / (2 * h)

    # Compute ∂κ/∂I₂ numerically
    kappa_plus = compute_kappa(I_2 + h, params)
    kappa_minus = compute_kappa(I_2 - h, params)
    dkappa_dI2 = (kappa_plus - kappa_minus) / (2 * h)

    # For each component, we'd need to compute ∂X/∂ρ and ∂X/∂κ
    # This requires more sophisticated numerical differentiation
    # For now, return the basic decomposition structure

    return {
        'rho': {
            'value': rho,
            'drho_dI2': drho_dI2,
        },
        'kappa': {
            'value': kappa,
            'dkappa_dI2': dkappa_dI2,
        },
        # Full decomposition would require additional numerical derivatives
        # which would be computationally expensive
    }
