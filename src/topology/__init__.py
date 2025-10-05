"""Topological computation modules for 18-level dependency ordering.

Constitutional Compliance:
- Principle III: Topological Execution Order

Levels 0-18 must be computed in strict order.
"""

from src.topology.level_00_exogenous import compute_mu_c
from src.topology.level_01_costs import compute_kappa_1, compute_kappa_2
from src.topology.level_02_contest import compute_rho
from src.topology.level_03_signal import compute_kappa
from src.topology.level_04_demand import compute_Delta
from src.topology.level_05_intercept_components import (
    compute_B_rho_kappa,
    compute_denominator_a,
    compute_numerator_a,
)
from src.topology.level_06_fixed_point_intercept import compute_a_rho_kappa
from src.topology.level_07_quantities import compute_q_1_star, compute_q_2_star
from src.topology.level_08_prices import compute_p_1_star, compute_p_2_star
from src.topology.level_09_profits import compute_pi_1_star, compute_pi_2_star
from src.topology.level_10_value_functions import compute_V_1, compute_V_2
from src.topology.level_11_utilities import compute_U_1, compute_U_2

__all__ = [
    # Level 0
    "compute_mu_c",
    # Level 1
    "compute_kappa_1",
    "compute_kappa_2",
    # Level 2
    "compute_rho",
    # Level 3
    "compute_kappa",
    # Level 4
    "compute_Delta",
    # Level 5
    "compute_B_rho_kappa",
    "compute_numerator_a",
    "compute_denominator_a",
    # Level 6
    "compute_a_rho_kappa",
    # Level 7
    "compute_q_1_star",
    "compute_q_2_star",
    # Level 8
    "compute_p_1_star",
    "compute_p_2_star",
    # Level 9
    "compute_pi_1_star",
    "compute_pi_2_star",
    # Level 10
    "compute_V_1",
    "compute_V_2",
    # Level 11
    "compute_U_1",
    "compute_U_2",
]
