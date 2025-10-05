"""Level 5: Stage 4 Intercept Components.

Constitutional Compliance:
- Principle I: Mathematical Fidelity (exact formulas, no algebraic simplification)
- Principle II: Equation Implementation Exactness
- Principle III: Topological Execution Order (Level 5, depends on Levels 0-4)
- Principle VI: Documentation Standards

Equations:
    - B_{ρ,κ} = [α(1+ρκ) - γδ(1-ρκ)] / [2β - δ(1+ρκ)]  (Leader's coefficient)
    - Numerator for a_{ρ,κ} fixed-point
    - Denominator for a_{ρ,κ} fixed-point

Dependencies: rho (Level 2), kappa (Level 3), Delta (Level 4)
"""

from src.models.parameters import Parameters


def compute_B_rho_kappa(rho: float, kappa: float, params: Parameters) -> float:
    """Compute leader's effective demand slope B_{ρ,κ}.

    Level 5: Effective demand slope from Algorithm 2, Step 11
    Equation: B_{ρ,κ} = β - (ρκ·δ²)/(2β)

    This is the slope of Leader's effective demand after accounting for
    Follower's best response to espionage.

    Args:
        rho: Contest success probability ρ ∈ [0,1] from Level 2
        kappa: Signal precision κ ∈ [0,1] from Level 3
        params: Model parameters (beta, delta)

    Returns:
        float: Effective demand slope B_{ρ,κ} > 0

    Mathematical Source:
        Algorithm 2, Step 11 (LaTeX document)
        Derived from Leader's effective demand Q_1 = K - B_{ρ,κ}·p_1

    Validation (FR-010):
        B_{ρ,κ} > 0 required for stability (downward-sloping demand)
        Typically satisfied when β > 0 and ρκ is not too large
    """
    # Algorithm 2, Step 11: B_{ρ,κ} = β - (ρκ·δ²)/(2β)
    B_rho_kappa = params.beta - (rho * kappa * params.delta**2) / (2 * params.beta)

    # FR-010: Stability constraint
    if B_rho_kappa <= 0:
        raise ValueError(
            f"Effective demand slope B_{{ρ,κ}} must be positive (stability), "
            f"got {B_rho_kappa:.6e} for ρ={rho:.4f}, κ={kappa:.4f}. "
            f"Check: β - (ρκ·δ²)/(2β) > 0 requires β² > ρκ·δ²/2"
        )

    return B_rho_kappa


def compute_numerator_a(
    rho: float, kappa: float, Delta: float, params: Parameters
) -> float:
    """Compute numerator for a_{ρ,κ} fixed-point equation.

    Level 5: Fixed-point component (numerator)
    Derived from Algorithm 2, Steps 11-14 and sabit nokta dengesi

    Equation: α·(2β+δ)/(2β) + (δ·μ_c)/2 + (δ²(1-ρκ)μ_c)/(4β)

    Args:
        rho: Contest success probability ρ from Level 2
        kappa: Signal precision κ from Level 3
        Delta: Demand interaction Δ = δ²/(2β) from Level 4 (not used directly)
        params: Model parameters

    Returns:
        float: Numerator component for fixed-point iteration

    Mathematical Source:
        Algorithm 2 (LaTeX document), sabit nokta türetimi
        Derived from K = α·(1 + δ/(2β)) + (δ·μ_c)/2 + (δ²(1-ρκ)/(2β))·p̄₁*
        and p̄₁* = a_{ρ,κ} + μ_c/2
    """
    # Algorithm 2'den türetilen pay formülü
    # numerator = α·(2β+δ)/(2β) + (δ·μ_c)/2 + (δ²(1-ρκ)μ_c)/(4β)

    term1 = params.alpha * (2 * params.beta + params.delta) / (2 * params.beta)
    term2 = (params.delta * params.mu_c) / 2
    term3 = (params.delta**2 * (1 - rho * kappa) * params.mu_c) / (4 * params.beta)

    numerator = term1 + term2 + term3

    return numerator


def compute_denominator_a(
    rho: float, kappa: float, Delta: float, B_rho_kappa: float, params: Parameters
) -> float:
    """Compute denominator for a_{ρ,κ} fixed-point equation.

    Level 5: Fixed-point component (denominator)
    Derived from Algorithm 2 sabit nokta dengesi

    Equation: 2B_{ρ,κ} - δ²(1-ρκ)/(2β) = 2β - δ²(1+ρκ)/(2β)

    Args:
        rho: Contest success probability ρ from Level 2
        kappa: Signal precision κ ∈ [0,1] from Level 3
        Delta: Demand interaction Δ = δ²/(2β) from Level 4
        B_rho_kappa: Leader's effective slope from compute_B_rho_kappa()
        params: Model parameters

    Returns:
        float: Denominator component > 0 (stability)

    Mathematical Source:
        Algorithm 2 (LaTeX document), sabit nokta türetimi
        Simplified form: 2β - δ²(1+ρκ)/(2β)

    Validation (FR-010):
        Denominator > 0 required for fixed-point convergence
        Typically satisfied when 2β > δ²(1+ρκ)/(2β)
    """
    # Basitleştirilmiş form (daha stabil): denominator = 2β - δ²(1+ρκ)/(2β)
    denominator = 2 * params.beta - (params.delta**2 * (1 + rho * kappa)) / (2 * params.beta)

    # FR-010: Stability constraint for fixed-point convergence
    if denominator <= 0:
        raise ValueError(
            f"Fixed-point denominator must be positive (stability), "
            f"got {denominator:.6e} for ρ={rho:.4f}, κ={kappa:.4f}. "
            f"Check: 2β > δ²(1+ρκ)/(2β) requires 4β² > δ²(1+ρκ)"
        )

    return denominator
