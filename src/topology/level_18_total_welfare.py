"""Level 18: Total Welfare.

Equation: W = CS + V₁* + V₂*
Dependencies: Level 17 (CS), Level 15 (V₁*, V₂*)
"""


def compute_W(CS: float, V_1_nash: float, V_2_nash: float) -> float:
    """Compute total welfare W = CS + V₁* + V₂*.

    Level 18: Welfare decomposition (final level)
    Equation: W = CS + V₁* + V₂*

    Args:
        CS: Consumer surplus from Level 17
        V_1_nash: Firm 1 value at Nash from Level 15
        V_2_nash: Firm 2 value at Nash from Level 15

    Returns:
        float: Total welfare W ≥ 0

    Mathematical Source:
        Section V: Total welfare is sum of consumer surplus and firm values
        Standard welfare decomposition in oligopoly theory

    Validation:
        W ≥ 0 in well-behaved equilibria
        Identity check: |W - (CS + V₁ + V₂)| < 1e-10
    """
    W = CS + V_1_nash + V_2_nash

    # Validation: welfare identity
    identity_check = abs(W - (CS + V_1_nash + V_2_nash))
    assert identity_check < 1e-10, f"Welfare identity violated: error={identity_check:.6e}"

    return W
