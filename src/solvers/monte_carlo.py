"""Monte Carlo Expectation Evaluation.

Constitutional Compliance:
- Principle IV: Reproducibility & Validation (fixed seed, deterministic)
- Principle V: Algorithm Transparency (diagnostic output)
- Principle VI: Documentation Standards

Implements: FR-006 (Monte Carlo with N=10,000, seed=42)
"""

from typing import Callable

import numpy as np

from src.models.parameters import Parameters


def evaluate_expectation(
    func: Callable[[float], float],
    I_1: float,
    I_2: float,
    params: Parameters,
    rng: np.random.Generator,
) -> float:
    """Evaluate E[func(θ)] via Monte Carlo simulation.

    Algorithm:
        1. Draw N samples: θ_i ~ N(μ_c, σ_c²), i=1,...,N
        2. Evaluate: func(θ_i) for each sample (typically profit π*(θ))
        3. Return: (1/N) Σ func(θ_i)

    Args:
        func: Function to evaluate, typically profit π_i*(θ)
              Signature: func(theta: float) -> float
        I_1: Firm 1 investment (used in func evaluation context)
        I_2: Firm 2 investment (used in func evaluation context)
        params: Model parameters (mu_c for prior mean, N_samples for sample size)
        rng: NumPy random generator (must be seeded for reproducibility)

    Returns:
        float: Monte Carlo estimate of E[func(θ)]

    Mathematical Source:
        Monte Carlo integration with normal sampling
        Standard error: σ/√N where σ = std(func(θ))
        For N=10,000: √N error ≈ 1% per research.md decision 8

    Reproducibility (FR-006, Principle IV):
        Same seed → same random draws → identical results
        Use: rng = np.random.default_rng(seed=42)

    Performance:
        N=10,000 samples chosen for 1% accuracy in < 60s
        See research.md for sample size analysis

    Constitutional Principle:
        IV. Reproducibility - Fixed seed=42, deterministic sampling
        V. Algorithm Transparency - Explicit sampling process, no black box
    """
    # FR-006: Use N_samples from parameters (default 10,000 for baseline)
    N = params.N_samples if hasattr(params, "N_samples") else 10_000

    # Draw θ samples from N(μ_c, σ_c²)
    # Note: params may not have sigma_c_sq, using default σ_c=10 from specification
    sigma_c = 10.0  # Standard deviation for cost uncertainty
    theta_samples = rng.normal(params.mu_c, sigma_c, size=N)

    # Evaluate func(θ) for each sample
    func_values = np.array([func(theta) for theta in theta_samples])

    # Return sample mean: (1/N) Σ func(θ_i)
    expectation = float(np.mean(func_values))

    return expectation


def evaluate_expectation_vectorized(
    func_vectorized: Callable[[np.ndarray], np.ndarray],
    params: Parameters,
    rng: np.random.Generator,
) -> float:
    """Evaluate E[func(θ)] via vectorized Monte Carlo (faster for array ops).

    This is an optimized version for functions that accept array inputs.
    Use this when func can process entire numpy arrays at once.

    Args:
        func_vectorized: Vectorized function accepting ndarray of θ values
                        Signature: func(theta: ndarray) -> ndarray
        params: Model parameters
        rng: NumPy random generator (seeded)

    Returns:
        float: Monte Carlo estimate of E[func(θ)]

    Example:
        >>> def profit_vectorized(theta_arr):
        ...     return (price - theta_arr) * quantity  # Element-wise ops
        >>> E_profit = evaluate_expectation_vectorized(profit_vectorized, params, rng)
    """
    N = params.N_samples if hasattr(params, "N_samples") else 10_000
    sigma_c = 10.0

    # Draw all samples at once
    theta_samples = rng.normal(params.mu_c, sigma_c, size=N)

    # Vectorized evaluation (much faster)
    func_values = func_vectorized(theta_samples)

    return float(np.mean(func_values))
