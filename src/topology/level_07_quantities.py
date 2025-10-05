"""Level 7: Stage 4 Demand Quantities - CORRECTED.

Equations: Q_i(p_i, p_j) - Derived FROM prices, not the other way around
Dependencies: Level 8 (prices)

MAJOR CHANGE: Quantities are computed from prices via demand function!
"""

from src.models.parameters import Parameters


def compute_quantity_from_prices(
    p_i: float,
    p_j: float,
    params: Parameters
) -> float:
    """Compute firm i's quantity from prices via demand function - CORRECTED.

    Level 7: Linear Demand System
    Equation (18): Q_i(p_i, p_j) = max{0, α - β·p_i + δ·p_j}

    This is the CORRECT order: prices → quantities (not quantities → prices!)

    Args:
        p_i: Firm i's price
        p_j: Firm j's price (competitor)
        params: Model parameters (alpha, beta, delta)

    Returns:
        float: Firm i's quantity Q_i ≥ 0

    Mathematical Source:
        Document equation (18): Linear demand with truncation
        ∂Q_i/∂p_i = -β < 0 (own-price effect)
        ∂Q_i/∂p_j = +δ > 0 (cross-price effect, substitutes)

    Properties:
        - Downward sloping in own price
        - Upward sloping in competitor's price
        - Truncated at zero (no negative quantities)
    """
    quantity = params.alpha - params.beta * p_i + params.delta * p_j

    # Truncation: quantities must be non-negative
    quantity = max(0.0, quantity)

    return quantity


# Convenience wrappers for backwards compatibility
def compute_q_1_star(p_1: float, p_2: float, params: Parameters) -> float:
    """Compute firm 1 quantity from prices."""
    return compute_quantity_from_prices(p_1, p_2, params)


def compute_q_2_star(p_1: float, p_2: float, params: Parameters) -> float:
    """Compute firm 2 quantity from prices."""
    return compute_quantity_from_prices(p_2, p_1, params)
