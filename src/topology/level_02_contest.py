"""Level 2: Contest Success Function (r-CSF).

Constitutional Compliance:
- Principle I: Mathematical Fidelity (exact equation structure)
- Principle II: Equation Implementation Exactness
- Principle III: Topological Execution Order (Level 2)
- Principle VI: Documentation Standards

Equations: ρ(I₁, I₂) - espionage success probability
"""

import warnings

from src.models.parameters import Parameters


def compute_rho(I_1: float, I_2: float, params: Parameters) -> float:
    """Compute espionage success probability ρ(I₁, I₂) - CORRECTED.

    Level 2: Contest Success Function (Regularized Tullock CSF)
    Equation (7): ρ(I₁, I₂) = I₂^γ / (I₂^γ + λ·I₁^γ + ε)

    ROLE DEFINITIONS (per document):
        - Firm 1 (I₁) = LEADER doing counter-espionage (DEFENSE)
        - Firm 2 (I₂) = FOLLOWER doing espionage (ATTACK)

    Args:
        I_1: Leader's counter-espionage (defense) investment I₁ ∈ [0, Ī]
        I_2: Follower's espionage (attack) investment I₂ ∈ [0, Ī]
        params: Model parameters (gamma_exponent, lambda_defense, epsilon)

    Returns:
        float: Espionage success probability ρ ∈ [0, 1]

    Mathematical Source:
        Document equation (7): ρ(I₁, I₂) = I₂^γ / (I₂^γ + λ·I₁^γ + ε)
        γ (gamma_exponent) ∈ (0,1]: Diminishing returns parameter
        λ (lambda_defense) > 0: Defense effectiveness multiplier
        ε (epsilon) > 0: Regularization constant

    Properties:
        - ∂ρ/∂I₂ > 0: More attack → higher success
        - ∂ρ/∂I₁ < 0: More defense → lower success
        - ρ → 0 as I₁ → ∞ (perfect defense)
        - ρ → 1 as I₂ → ∞ (overwhelming attack)
        - ρ ∈ [0,1] by construction
    """
    # Extract parameters
    gamma = params.gamma_exponent  # γ ∈ (0,1]
    lambda_def = params.lambda_defense  # λ > 0
    eps = params.epsilon  # ε > 0

    # Equation (7): ρ = I₂^γ / (I₂^γ + λ·I₁^γ + ε)
    I_2_power = I_2 ** gamma
    I_1_power = I_1 ** gamma

    numerator = I_2_power
    denominator = I_2_power + lambda_def * I_1_power + eps

    rho = numerator / denominator

    # Validation: should be in [0,1] by construction, but clip for numerical safety
    if not (0 <= rho <= 1):
        deviation = max(abs(rho), abs(rho - 1)) - 1
        if deviation > 1e-10:
            warnings.warn(
                f"CSF ρ(I₁={I_1:.4f}, I₂={I_2:.4f}) = {rho:.6e} "
                f"outside [0,1] by {deviation:.6e}. Clipping.",
                UserWarning,
                stacklevel=2,
            )
        rho = max(0.0, min(1.0, rho))

    return rho
