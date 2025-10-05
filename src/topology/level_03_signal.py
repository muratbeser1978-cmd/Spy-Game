"""Level 3: Signal Precision Function - CORRECTED.

Equations: κ(I₂) - Bayesian reliability weight
Dependencies: Level 0 (σ_ε, σ_c), Level 2 (price variance)

CORRECTED: Now matches document equations (16-17)
"""

import warnings

from src.models.parameters import Parameters


def compute_kappa(I_2: float, params: Parameters) -> float:
    """Compute Bayesian reliability weight κ(I₂) - CORRECTED.

    Level 3: Bayesian Signal Precision (depends on I₂, NOT I₁)
    Equation (16): κ(I₂) = τ_p² / (τ_p² + σ_ε²/(I₂+ι))

    where τ_p² = Var(p₁*) = σ_c²/4 (from equation 13-14)

    NOTE: κ depends ONLY on I₂ (follower's espionage investment),
    NOT on I₁. Higher I₂ → lower noise → higher κ.

    Args:
        I_2: Follower's espionage investment I₂ ∈ [0, Ī]
        params: Model parameters (sigma_epsilon, sigma_c, iota)

    Returns:
        float: Bayesian reliability weight κ ∈ [0, 1]

    Mathematical Source:
        Equation (13-14): τ_p² = σ_c²/4 (price variance with 50% pass-through)
        Equation (11): ε ~ N(0, σ_ε²/(I₂+ι)) (noise variance decreases with I₂)
        Equation (16): κ(I₂) = τ_p² / (τ_p² + σ_ε²/(I₂+ι)) (Bayesian weight)

    Interpretation:
        - κ → 0 when I₂ → 0 (very noisy signal, prior dominates)
        - κ → 1 when I₂ → ∞ (perfect signal, data dominates)
        - ∂κ/∂I₂ > 0 (more espionage → better signal)

    Properties:
        - κ ∈ [0,1] by construction (Bayesian weight)
        - Equation (17): E[p₁|s] = (1-κ)·p̄₁* + κ·s
    """
    # Equation (14): τ_p² = Var(p₁*) = σ_c²/4
    tau_p_squared = (params.sigma_c ** 2) / 4.0

    # Equation (11): Noise variance = σ_ε²/(I₂+ι)
    noise_variance = (params.sigma_epsilon ** 2) / (I_2 + params.iota)

    # Equation (16): κ(I₂) = τ_p² / (τ_p² + noise_variance)
    kappa = tau_p_squared / (tau_p_squared + noise_variance)

    # Validation: should be in [0,1] by construction
    if not (0 <= kappa <= 1):
        deviation = max(abs(kappa), abs(kappa - 1)) - 1
        if deviation > 1e-10:
            warnings.warn(
                f"Bayesian weight κ(I₂={I_2:.4f}) = {kappa:.6e} "
                f"outside [0,1] by {deviation:.6e}. Clipping.",
                UserWarning,
                stacklevel=2,
            )
        kappa = max(0.0, min(1.0, kappa))

    return kappa
