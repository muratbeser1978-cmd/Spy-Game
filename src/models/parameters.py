"""Type contract for model parameters.

Constitutional Compliance:
- Principle I: Mathematical Fidelity (variable names match notation)
- Principle VI: Documentation Standards (equation references)

Implements: FR-001 to FR-006 (parameter validation)
"""

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Parameters:
    """Exogenous model parameters (Level 0 in topological ordering).

    All parameters validated on construction per FR-001 to FR-006.

    Attributes:
        alpha (float): Market size parameter α > 0 (demand intercept)
        beta (float): Own-price sensitivity β > 0 (demand slope)
        delta (float): Cross-price sensitivity δ, constrained 0 < δ < β (substitutability)
        gamma (float): Follower's marginal cost γ ≥ 0 (Firm 2 has FIXED public cost = γ, Firm 1 has RANDOM private cost ~ N(μ_c, σ_c²))
        kappa_1 (float): Firm 1 investment cost κ₁ > 0 (espionage quadratic cost)
        kappa_2 (float): Firm 2 investment cost κ₂ > 0 (counter-espionage quadratic cost)
        epsilon (float): Contest regularization ε ≥ 0 (prevents division by zero)
        xi (float): Contest effectiveness ξ ≥ 0 (espionage technology parameter)
        r_0 (float): Contest baseline r₀ ≥ 0 (minimum success probability)
        iota (float): Signal regularization ι ≥ 0 (prevents division by zero)
        s_0 (float): Signal baseline s₀ ≥ 0 (minimum informativeness)
        I_bar (float): Investment upper bound Ī > 0 (maximum allowed investment)
        mu_c (float): Prior mean μ_c > 0 (expected cost draw for θ)

    Mathematical Source:
        - Demand parameters (α, β, δ): Section II.A
        - Cost parameters (γ, μ_c): Section II.B
        - Contest technology (ε, ξ, r₀): Section III.A, equation (3.2)
        - Signal structure (ι, s₀): Section III.B, equation (3.5)
        - Investment costs (κ₁, κ₂, Ī): Section III.C, equation (3.8)
    """

    # Demand parameters (FR-001)
    alpha: float  # α > 0
    beta: float  # β > 0
    delta: float  # 0 < δ < β

    # Cost parameters (FR-002)
    gamma: float  # γ ≥ 0
    kappa_1: float  # κ₁ > 0
    kappa_2: float  # κ₂ > 0

    # Contest technology (FR-003)
    epsilon: float  # ε > 0, regularization
    gamma_exponent: float  # γ ∈ (0,1], diminishing returns in CSF
    lambda_defense: float  # λ > 0, defense effectiveness multiplier

    # Signal structure (FR-004)
    iota: float  # ι > 0, signal variance regularization
    sigma_epsilon: float  # σ_ε > 0, base noise standard deviation
    sigma_c: float  # σ_c > 0, cost standard deviation

    # Investment bounds (FR-005)
    I_bar: float  # Ī > 0

    # Prior mean (FR-006)
    mu_c: float  # μ_c > 0

    def __post_init__(self) -> None:
        """Validate all parameter constraints per FR-001 to FR-006.

        Raises:
            ValueError: If any constraint violated, with reference to source inequality
        """
        # FR-001: Demand constraints
        if self.alpha <= 0:
            raise ValueError(
                f"Demand parameter alpha must be positive (α > 0), got {self.alpha}"
            )
        if self.beta <= 0:
            raise ValueError(
                f"Demand parameter beta must be positive (β > 0), got {self.beta}"
            )
        if not (0 < self.delta < self.beta):
            raise ValueError(
                f"Substitutability requires 0 < δ < β, got δ={self.delta}, β={self.beta}"
            )

        # FR-002: Cost constraints
        if self.gamma < 0:
            raise ValueError(
                f"Cost asymmetry must be non-negative (γ ≥ 0), got {self.gamma}"
            )
        if self.kappa_1 <= 0:
            raise ValueError(
                f"Firm 1 investment cost must be positive (κ₁ > 0), got {self.kappa_1}"
            )
        if self.kappa_2 <= 0:
            raise ValueError(
                f"Firm 2 investment cost must be positive (κ₂ > 0), got {self.kappa_2}"
            )

        # FR-003: Contest technology constraints
        if self.epsilon <= 0:
            raise ValueError(
                f"Contest regularization must be positive (ε > 0), got {self.epsilon}"
            )
        if not (0 < self.gamma_exponent <= 1):
            raise ValueError(
                f"CSF exponent must be in (0,1] (γ ∈ (0,1]), got {self.gamma_exponent}"
            )
        if self.lambda_defense <= 0:
            raise ValueError(
                f"Defense multiplier must be positive (λ > 0), got {self.lambda_defense}"
            )

        # FR-004: Signal structure constraints
        if self.iota <= 0:
            raise ValueError(
                f"Signal regularization must be positive (ι > 0), got {self.iota}"
            )
        if self.sigma_epsilon <= 0:
            raise ValueError(
                f"Noise std must be positive (σ_ε > 0), got {self.sigma_epsilon}"
            )
        if self.sigma_c <= 0:
            raise ValueError(
                f"Cost std must be positive (σ_c > 0), got {self.sigma_c}"
            )

        # FR-005: Investment bounds
        if self.I_bar <= 0:
            raise ValueError(
                f"Investment upper bound must be positive (Ī > 0), got {self.I_bar}"
            )

        # FR-006: Prior mean
        if self.mu_c <= 0:
            raise ValueError(
                f"Prior mean must be positive (μ_c > 0), got {self.mu_c}"
            )

    @classmethod
    def baseline(cls) -> "Parameters":
        """Return baseline parameter set from Table 1.

        Returns:
            Parameters: Validated baseline configuration with:
                - Demand: α=100, β=2.0, δ=0.5
                - Costs: γ=1.0, κ₁=1.0, κ₂=1.0 (increased for stability)
                - Contest: ε=1.0, ξ=0.3, r₀=0.1 (adjusted for stability)
                - Signal: ι=1.0, s₀=0.1 (adjusted to keep κ in [0,1])
                - Bounds: Ī=5.0 (reduced to prevent boundary issues)
                - Prior: μ_c=50.0

        Source:
            FR-001 to FR-006 baseline values (adjusted for numerical stability)
        """
        return cls(
            # Demand parameters (reasonable market structure)
            alpha=100.0,      # Market size (intercept)
            beta=1.5,         # Own-price elasticity (consumers sensitive to own price)
            delta=0.3,        # Cross-price elasticity (products are substitutes but not perfect)

            # Cost parameters
            gamma=45.0,       # Follower's FIXED cost (HIGHER than leader's expected cost - leader has advantage)
            kappa_1=0.5,      # Investment cost for leader (counter-espionage - cheaper to defend)
            kappa_2=1.0,      # Investment cost for follower (espionage - more expensive to attack)

            # Contest technology (defense has advantage - leader protection)
            epsilon=0.5,           # Regularization prevents extreme outcomes
            gamma_exponent=0.6,    # Moderate diminishing returns (standard in contests)
            lambda_defense=1.5,    # Defense more effective (leader has natural advantage)

            # Signal structure (moderate information quality)
            iota=2.0,              # Signal variance regularization
            sigma_epsilon=10.0,    # Moderate noise (signal is informative but not perfect)
            sigma_c=8.0,           # Moderate cost uncertainty (realistic variation)

            # Investment bounds (reasonable scale)
            I_bar=20.0,       # Higher ceiling allows strategic investment

            # Prior mean (reasonable cost level)
            mu_c=40.0,        # Expected marginal cost (allows positive markups)
        )

    def to_dict(self) -> Dict[str, float]:
        """Convert parameters to dictionary for serialization.

        Returns:
            Dict[str, float]: All parameter key-value pairs
        """
        return {
            "alpha": self.alpha,
            "beta": self.beta,
            "delta": self.delta,
            "gamma": self.gamma,
            "kappa_1": self.kappa_1,
            "kappa_2": self.kappa_2,
            "epsilon": self.epsilon,
            "gamma_exponent": self.gamma_exponent,
            "lambda_defense": self.lambda_defense,
            "iota": self.iota,
            "sigma_epsilon": self.sigma_epsilon,
            "sigma_c": self.sigma_c,
            "I_bar": self.I_bar,
            "mu_c": self.mu_c,
        }
