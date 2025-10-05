"""Level 8: Stage 4 Equilibrium Prices - CORRECTED.

Equations: p₁*(c₁), p₂*(c₂) via direct pricing rules
Dependencies: Level 6 (a_{ρ,κ}), NOT quantities

MAJOR CHANGE: Stackelberg pricing, not inverse demand!
"""

from src.models.parameters import Parameters


def compute_p_1_star(
    a_rho_kappa: float, c_1: float
) -> float:
    """Compute leader's (Firm 1) equilibrium price p₁*(c₁) - CORRECTED.

    Level 8: Leader's Affine Pricing Rule
    Equation (30): p₁*(c₁) = a_{ρ,κ} + (1/2)·c₁

    This is the Stackelberg leader's optimal pricing strategy.
    50% cost pass-through to price.

    Args:
        a_rho_kappa: Fixed-point intercept from Level 6
        c_1: Leader's cost realization c₁

    Returns:
        float: Leader's price p₁*(c₁)

    Mathematical Source:
        Document equation (30): Affine pricing rule
        ∂p₁*/∂c₁ = 1/2 (cost pass-through)

    NOTE: This is NOT inverse demand! Leader chooses price directly
    based on cost, then follower best-responds.
    """
    p_1_star = a_rho_kappa + 0.5 * c_1

    return p_1_star


def compute_p_2_star(
    rho: float,
    kappa: float,
    p_1_bar: float,
    c_2: float,
    params: Parameters,
    espionage_success: bool = False,
    signal: float = 0.0
) -> float:
    """Compute follower's (Firm 2) equilibrium price p₂* - CORRECTED.

    Level 8: Follower's Best Response to Leader
    Equation (22-23):
        p₂^I(s,c₂) = [α + β·c₂ + δ·E[p₁|s]] / (2β)  [if espionage succeeds]
        p₂^U(c₂) = [α + β·c₂ + δ·p̄₁*] / (2β)        [if espionage fails]

    Args:
        rho: Espionage success probability ρ
        kappa: Bayesian reliability weight κ
        p_1_bar: Prior mean of leader's price p̄₁*
        c_2: Follower's cost realization c₂
        params: Model parameters (alpha, beta, delta)
        espionage_success: Whether espionage succeeded
        signal: Observed noisy signal s (if espionage succeeded)

    Returns:
        float: Follower's price p₂*

    Mathematical Source:
        Equation (22): p₂^I with Bayesian updating E[p₁|s] = (1-κ)·p̄₁* + κ·s
        Equation (23): p₂^U with prior mean p̄₁*
    """
    alpha = params.alpha
    beta = params.beta
    delta = params.delta

    if espionage_success:
        # Bayesian posterior: E[p₁|s] = (1-κ)·p̄₁* + κ·s
        expected_p1 = (1 - kappa) * p_1_bar + kappa * signal
        # Equation (22): p₂^I(s,c₂)
        p_2_star = (alpha + beta * c_2 + delta * expected_p1) / (2 * beta)
    else:
        # Equation (23): p₂^U(c₂) using prior
        p_2_star = (alpha + beta * c_2 + delta * p_1_bar) / (2 * beta)

    return p_2_star
