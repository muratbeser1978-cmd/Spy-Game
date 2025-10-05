"""Level 4: Demand Derivatives.

Constitutional Compliance:
- Principle I: Mathematical Fidelity (exact formula, no pre-computation)
- Principle II: Equation Implementation Exactness
- Principle III: Topological Execution Order (Level 4)
- Principle VI: Documentation Standards

Equations: Δ = δ²/(2β) - demand interaction term
"""

from src.models.parameters import Parameters


def compute_Delta(params: Parameters) -> float:
    """Compute demand interaction term Δ = δ²/(2β).

    Level 4: Demand Derivatives (depends only on parameters)
    Equation: Δ = δ²/(2β)

    This term captures the strategic substitutability effect in the
    Bertrand duopoly. Higher Δ → stronger cross-price effects →
    more intense price competition.

    Args:
        params: Model parameters (delta, beta)

    Returns:
        float: Demand interaction term Δ > 0

    Mathematical Source:
        Section II.A: Linear demand system
        Inverse demand: p_i = α - β·q_i - δ·q_j
        Derived coefficient in equilibrium quantities

    Validation:
        Δ > 0 always holds since δ > 0, β > 0 per FR-001

    Constitutional Principle:
        I. Mathematical Fidelity - Formula kept as δ²/(2β), NOT pre-computed
           to maintain traceability to source equations
    """
    # Equation: Δ = δ²/(2β)
    # IMPORTANT: Keep formula explicit per Principle I
    Delta = (params.delta**2) / (2 * params.beta)

    # Validation (FR-010): Δ > 0 always satisfied if β > 0
    assert Delta > 0, f"Demand interaction Δ must be positive, got {Delta:.6e}"

    return Delta
