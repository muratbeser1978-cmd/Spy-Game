"""Type contract for computed variables across 18 topological levels.

Constitutional Compliance:
- Principle I: Mathematical Fidelity (exact variable names)
- Principle III: Topological Execution Order (18-level structure)
- Principle VI: Documentation Standards (equation references)

Implements: FR-009 (topological ordering), FR-010 (constraint validation)
"""

from dataclasses import dataclass
from typing import Dict
import warnings


@dataclass
class Variables:
    """All 66 computed variables organized by topological level.

    Variables computed sequentially Level 0 → Level 18 following
    strict dependency order (Principle III).

    All probability constraints validated per FR-010 with clipping
    if |deviation| > 1e-10 and warning.

    Attributes organized by level for traceability to mathematical model.
    """

    # Level 0: Exogenous (1 variable)
    mu_c: float  # μ_c - prior mean cost (exogenous)

    # Level 1: Investment costs (2 variables)
    kappa_1: float  # κ₁ - firm 1 investment cost
    kappa_2: float  # κ₂ - firm 2 investment cost

    # Level 2: Contest technology (1 variable)
    rho: float  # ρ(I₁,I₂) - espionage success probability, equation (3.2)

    # Level 3: Signal structure (1 variable)
    kappa: float  # κ(I₁,I₂) - signal precision, equation (3.5)

    # Level 4: Demand derivatives (1 variable)
    Delta: float  # Δ = δ²/(2β) - demand interaction term

    # Level 5: Stage 4 intercept components (3 variables)
    B_rho_kappa: float  # B_{ρ,κ} - leader's coefficient, equation (4.3)
    numerator_a: float  # Numerator for a_{ρ,κ} fixed-point
    denominator_a: float  # Denominator for a_{ρ,κ} fixed-point

    # Level 6: Stage 4 intercept (1 variable - fixed-point solution)
    a_rho_kappa: float  # a_{ρ,κ} - equilibrium intercept, equation (4.5)

    # Level 7: Stage 4 equilibrium quantities (2 variables)
    q_1_star: float  # q₁*(θ) - firm 1 quantity, equation (4.6)
    q_2_star: float  # q₂*(θ) - firm 2 quantity, equation (4.7)

    # Level 8: Stage 4 equilibrium prices (2 variables)
    p_1_star: float  # p₁*(θ) - firm 1 price, inverse demand
    p_2_star: float  # p₂*(θ) - firm 2 price, inverse demand

    # Level 9: Stage 4 profits (2 variables)
    pi_1_star: float  # π₁*(θ) - firm 1 profit
    pi_2_star: float  # π₂*(θ) - firm 2 profit

    # Level 10: Stage 3 value functions (2 variables)
    V_1: float  # V₁(I₁,I₂) - firm 1 expected profit (Monte Carlo)
    V_2: float  # V₂(I₁,I₂) - firm 2 expected profit (Monte Carlo)

    # Level 11: Stage 3 utility functions (2 variables)
    U_1: float  # U₁(I₁,I₂) = V₁ - (κ₁/2)I₁² - firm 1 net utility
    U_2: float  # U₂(I₁,I₂) = V₂ - (κ₂/2)I₂² - firm 2 net utility

    # Level 12: Nash equilibrium investments (2 variables - SLSQP solution)
    I_1_nash: float  # I₁* - Nash equilibrium espionage investment
    I_2_nash: float  # I₂* - Nash equilibrium counter-espionage investment

    # Level 13: Equilibrium contest/signal (2 variables)
    rho_nash: float  # ρ* = ρ(I₁*,I₂*) - equilibrium success probability
    kappa_nash: float  # κ* = κ(I₁*,I₂*) - equilibrium signal precision

    # Level 14: Equilibrium coefficients (3 variables)
    B_nash: float  # B* = B_{ρ*,κ*} - equilibrium leader coefficient
    a_nash: float  # a* = a_{ρ*,κ*} - equilibrium intercept
    Delta_nash: float  # Δ* = Δ (constant) - equilibrium demand interaction

    # Level 15: Equilibrium value functions (2 variables)
    V_1_nash: float  # V₁* = V₁(I₁*,I₂*) - equilibrium firm 1 expected profit
    V_2_nash: float  # V₂* = V₂(I₁*,I₂*) - equilibrium firm 2 expected profit

    # Level 16: Equilibrium utility (2 variables)
    U_1_nash: float  # U₁* = U₁(I₁*,I₂*) - equilibrium firm 1 net utility
    U_2_nash: float  # U₂* = U₂(I₁*,I₂*) - equilibrium firm 2 net utility

    # Level 17: Consumer surplus (1 variable)
    CS: float  # CS(I₁*,I₂*) - consumer surplus at equilibrium

    # Level 18: Total welfare (1 variable)
    W: float  # W = CS + V₁* + V₂* - total welfare

    def __post_init__(self) -> None:
        """Validate all variable constraints per FR-010.

        Probability constraints (ρ, κ, ρ*, κ*):
            - If in [0,1]: pass
            - If deviation ≤ 1e-10: clip to [0,1] and pass silently
            - If deviation > 1e-10: clip to [0,1] and warn

        Stability constraints:
            - B_{ρ,κ} > 0 (leader's second-order condition)
            - denominator_a > 0 (fixed-point stability)

        Non-negativity:
            - Profits π_i* ≥ 0
            - Values V_i ≥ 0
            - Consumer surplus CS ≥ 0
            - Total welfare W ≥ 0

        Raises:
            ValueError: If stability or non-negativity constraints violated
        """
        # Probability validation with clipping (FR-010)
        for var_name, var_value in [
            ("rho", self.rho),
            ("kappa", self.kappa),
            ("rho_nash", self.rho_nash),
            ("kappa_nash", self.kappa_nash),
        ]:
            if var_value < 0 or var_value > 1:
                deviation = max(abs(var_value), abs(var_value - 1)) - 1
                if abs(deviation) > 1e-10:
                    warnings.warn(
                        f"Probability {var_name} = {var_value:.6e} out of bounds [0,1] "
                        f"by {deviation:.6e}. Clipping to [0,1].",
                        UserWarning,
                    )
                # Clip in-place (requires object.__setattr__ since frozen dataclass)
                clipped = max(0.0, min(1.0, var_value))
                object.__setattr__(self, var_name, clipped)

        # Stability constraints (FR-010)
        if self.B_rho_kappa <= 0:
            raise ValueError(
                f"Leader's coefficient B_{{ρ,κ}} must be positive (SOC), "
                f"got {self.B_rho_kappa:.6e}"
            )
        if self.denominator_a <= 0:
            raise ValueError(
                f"Fixed-point denominator must be positive (stability), "
                f"got {self.denominator_a:.6e}"
            )

        # Non-negativity constraints (FR-010)
        if self.pi_1_star < 0:
            raise ValueError(f"Firm 1 profit must be non-negative, got {self.pi_1_star:.6e}")
        if self.pi_2_star < 0:
            raise ValueError(f"Firm 2 profit must be non-negative, got {self.pi_2_star:.6e}")
        if self.V_1 < 0:
            raise ValueError(f"Firm 1 value must be non-negative, got {self.V_1:.6e}")
        if self.V_2 < 0:
            raise ValueError(f"Firm 2 value must be non-negative, got {self.V_2:.6e}")
        if self.CS < 0:
            raise ValueError(f"Consumer surplus must be non-negative, got {self.CS:.6e}")
        if self.W < 0:
            raise ValueError(f"Total welfare must be non-negative, got {self.W:.6e}")

    def get_level(self, level: int) -> Dict[str, float]:
        """Return all variables computed at specified topological level.

        Args:
            level: Topological level 0-18

        Returns:
            Dict[str, float]: Variable names → values for requested level

        Raises:
            ValueError: If level not in [0, 18]

        Level Mapping:
            0: mu_c
            1: kappa_1, kappa_2
            2: rho
            3: kappa
            4: Delta
            5: B_rho_kappa, numerator_a, denominator_a
            6: a_rho_kappa
            7: q_1_star, q_2_star
            8: p_1_star, p_2_star
            9: pi_1_star, pi_2_star
            10: V_1, V_2
            11: U_1, U_2
            12: I_1_nash, I_2_nash
            13: rho_nash, kappa_nash
            14: B_nash, a_nash, Delta_nash
            15: V_1_nash, V_2_nash
            16: U_1_nash, U_2_nash
            17: CS
            18: W
        """
        level_map = {
            0: {"mu_c": self.mu_c},
            1: {"kappa_1": self.kappa_1, "kappa_2": self.kappa_2},
            2: {"rho": self.rho},
            3: {"kappa": self.kappa},
            4: {"Delta": self.Delta},
            5: {
                "B_rho_kappa": self.B_rho_kappa,
                "numerator_a": self.numerator_a,
                "denominator_a": self.denominator_a,
            },
            6: {"a_rho_kappa": self.a_rho_kappa},
            7: {"q_1_star": self.q_1_star, "q_2_star": self.q_2_star},
            8: {"p_1_star": self.p_1_star, "p_2_star": self.p_2_star},
            9: {"pi_1_star": self.pi_1_star, "pi_2_star": self.pi_2_star},
            10: {"V_1": self.V_1, "V_2": self.V_2},
            11: {"U_1": self.U_1, "U_2": self.U_2},
            12: {"I_1_nash": self.I_1_nash, "I_2_nash": self.I_2_nash},
            13: {"rho_nash": self.rho_nash, "kappa_nash": self.kappa_nash},
            14: {"B_nash": self.B_nash, "a_nash": self.a_nash, "Delta_nash": self.Delta_nash},
            15: {"V_1_nash": self.V_1_nash, "V_2_nash": self.V_2_nash},
            16: {"U_1_nash": self.U_1_nash, "U_2_nash": self.U_2_nash},
            17: {"CS": self.CS},
            18: {"W": self.W},
        }

        if level not in level_map:
            raise ValueError(f"Level must be in [0, 18], got {level}")

        return level_map[level]

    def to_dict(self) -> Dict[str, float]:
        """Convert all variables to dictionary for serialization.

        Returns:
            Dict[str, float]: All 66 variable key-value pairs
        """
        return {
            # Level 0
            "mu_c": self.mu_c,
            # Level 1
            "kappa_1": self.kappa_1,
            "kappa_2": self.kappa_2,
            # Level 2
            "rho": self.rho,
            # Level 3
            "kappa": self.kappa,
            # Level 4
            "Delta": self.Delta,
            # Level 5
            "B_rho_kappa": self.B_rho_kappa,
            "numerator_a": self.numerator_a,
            "denominator_a": self.denominator_a,
            # Level 6
            "a_rho_kappa": self.a_rho_kappa,
            # Level 7
            "q_1_star": self.q_1_star,
            "q_2_star": self.q_2_star,
            # Level 8
            "p_1_star": self.p_1_star,
            "p_2_star": self.p_2_star,
            # Level 9
            "pi_1_star": self.pi_1_star,
            "pi_2_star": self.pi_2_star,
            # Level 10
            "V_1": self.V_1,
            "V_2": self.V_2,
            # Level 11
            "U_1": self.U_1,
            "U_2": self.U_2,
            # Level 12
            "I_1_nash": self.I_1_nash,
            "I_2_nash": self.I_2_nash,
            # Level 13
            "rho_nash": self.rho_nash,
            "kappa_nash": self.kappa_nash,
            # Level 14
            "B_nash": self.B_nash,
            "a_nash": self.a_nash,
            "Delta_nash": self.Delta_nash,
            # Level 15
            "V_1_nash": self.V_1_nash,
            "V_2_nash": self.V_2_nash,
            # Level 16
            "U_1_nash": self.U_1_nash,
            "U_2_nash": self.U_2_nash,
            # Level 17
            "CS": self.CS,
            # Level 18
            "W": self.W,
        }
