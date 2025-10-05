"""Level 1: Investment Costs.

Constitutional Compliance:
- Principle I: Mathematical Fidelity
- Principle II: Equation Implementation Exactness
- Principle III: Topological Execution Order (Level 1)
- Principle VI: Documentation Standards

Equations: κ₁, κ₂ (exogenous investment cost parameters)
"""

from src.models.parameters import Parameters


def compute_kappa_1(params: Parameters) -> float:
    """Compute firm 1 investment cost parameter κ₁.

    Level 1: Exogenous (depends only on parameters)
    Equation: κ₁ (exogenous from specification)

    Args:
        params: Model parameters containing kappa_1

    Returns:
        float: Firm 1 quadratic investment cost coefficient κ₁ > 0

    Mathematical Source:
        Section III.C, equation (3.8): Cost_i = (κ_i/2)I_i²
        FR-002: κ₁ must satisfy κ₁ > 0
        Baseline: κ₁ = 0.5

    Constitutional Principle:
        I. Mathematical Fidelity - Direct parameter retrieval
    """
    return params.kappa_1


def compute_kappa_2(params: Parameters) -> float:
    """Compute firm 2 investment cost parameter κ₂.

    Level 1: Exogenous (depends only on parameters)
    Equation: κ₂ (exogenous from specification)

    Args:
        params: Model parameters containing kappa_2

    Returns:
        float: Firm 2 quadratic investment cost coefficient κ₂ > 0

    Mathematical Source:
        Section III.C, equation (3.8): Cost_i = (κ_i/2)I_i²
        FR-002: κ₂ must satisfy κ₂ > 0
        Baseline: κ₂ = 0.5

    Constitutional Principle:
        I. Mathematical Fidelity - Direct parameter retrieval
    """
    return params.kappa_2
