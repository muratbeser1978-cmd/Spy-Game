"""Level 0: Exogenous Variables.

Constitutional Compliance:
- Principle I: Mathematical Fidelity (exact variable names)
- Principle II: Equation Implementation Exactness
- Principle III: Topological Execution Order (Level 0)
- Principle VI: Documentation Standards

Equations: Prior mean μ_c (exogenous parameter)
"""

from src.models.parameters import Parameters


def compute_mu_c(params: Parameters) -> float:
    """Compute prior mean μ_c.

    Level 0: Exogenous (no dependencies)
    Equation: μ_c (exogenous parameter from specification)

    Args:
        params: Model parameters containing mu_c

    Returns:
        float: Prior mean μ_c for cost draw θ ~ N(μ_c, σ_c²)

    Mathematical Source:
        Section II.B, parameter specification
        FR-006 baseline value: μ_c = 50.0

    Constitutional Principle:
        I. Mathematical Fidelity - Direct parameter retrieval, no transformation
    """
    return params.mu_c
