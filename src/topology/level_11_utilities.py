"""Level 11: Stage 3 Utility Functions.

Equations: U₁(I₁,I₂), U₂(I₁,I₂) = V_i - (κ_i/2)I_i²
Dependencies: Level 10 (V₁, V₂)
"""


def compute_U_1(V_1: float, I_1: float, kappa_1: float) -> float:
    """Compute firm 1 net utility U₁(I₁,I₂).

    Level 11: Utility after investment cost
    Equation: U₁(I₁,I₂) = V₁(I₁,I₂) - (κ₁/2)I₁²

    Args:
        V_1: Expected profit from Level 10
        I_1: Investment level I₁
        kappa_1: Investment cost parameter κ₁

    Returns:
        float: Net utility U₁

    Mathematical Source:
        Section III.C: Quadratic investment costs
    """
    U_1 = V_1 - (kappa_1 / 2) * (I_1**2)

    return U_1


def compute_U_2(V_2: float, I_2: float, kappa_2: float) -> float:
    """Compute firm 2 net utility U₂(I₁,I₂).

    Level 11: Utility after investment cost
    Equation: U₂(I₁,I₂) = V₂(I₁,I₂) - (κ₂/2)I₂²

    Args:
        V_2: Expected profit from Level 10
        I_2: Investment level I₂
        kappa_2: Investment cost parameter κ₂

    Returns:
        float: Net utility U₂
    """
    U_2 = V_2 - (kappa_2 / 2) * (I_2**2)

    return U_2
