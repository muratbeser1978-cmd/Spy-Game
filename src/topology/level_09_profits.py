"""Level 9: Stage 4 Equilibrium Profits.

Equations: π₁*(θ), π₂*(θ)
Dependencies: Level 8 (p₁*, p₂*), Level 7 (q₁*, q₂*)
"""

from src.models.parameters import Parameters


def compute_pi_1_star(
    p_1_star: float, q_1_star: float, c_1: float
) -> float:
    """Compute Leader (Firm 1) equilibrium profit π₁*(c₁).

    Level 9: Leader's Profit
    Equation: π₁*(c₁) = (p₁* - c₁)·q₁*

    Where c₁ ~ N(μ_c, σ_c²) is Leader's RANDOM private cost (target of espionage).

    Args:
        p_1_star: Leader's price from Level 8
        q_1_star: Leader's quantity from Level 7
        c_1: Leader's cost realization

    Returns:
        float: Leader's profit π₁*(c₁) (can be negative if p < c₁)

    Mathematical Source:
        Section II.B: Firm profit functions
        Leader has private cost information
    """
    pi_1_star = (p_1_star - c_1) * q_1_star

    return pi_1_star


def compute_pi_2_star(p_2_star: float, q_2_star: float, c_2: float) -> float:
    """Compute Follower (Firm 2) equilibrium profit π₂*(c₂).

    Level 9: Follower's Profit
    Equation: π₂*(c₂) = (p₂* - c₂)·q₂*

    Where c₂ = γ is Follower's FIXED public cost (known to all).

    Args:
        p_2_star: Follower's price from Level 8
        q_2_star: Follower's quantity from Level 7
        c_2: Follower's cost (fixed at γ)

    Returns:
        float: Follower's profit π₂*(c₂) (can be negative if p < c₂)

    Mathematical Source:
        Section II.B: Firm profit functions
        Follower has public cost information
    """
    pi_2_star = (p_2_star - c_2) * q_2_star

    return pi_2_star
