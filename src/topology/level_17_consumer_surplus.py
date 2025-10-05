"""Level 17: Consumer Surplus - CORRECTED.

Now uses correct game sequence with prices→quantities.
"""

import numpy as np

from src.models.parameters import Parameters
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


def compute_CS(
    I_1_nash: float, I_2_nash: float, params: Parameters, rng: np.random.Generator
) -> float:
    """Compute expected consumer surplus - CORRECTED.

    CS(θ) = ½(β·q₁*² + 2δ·q₁*·q₂* + β·q₂*²)

    Now uses correct game sequence:
        prices → quantities → consumer surplus

    Args:
        I_1_nash: Nash equilibrium I₁*
        I_2_nash: Nash equilibrium I₂*
        params: Model parameters
        rng: Random number generator

    Returns:
        float: Expected consumer surplus E[CS]
    """
    N = 10_000

    # Compute equilibrium parameters
    rho = compute_rho(I_1_nash, I_2_nash, params)
    kappa = compute_kappa(I_2_nash, params)
    Delta = compute_Delta(params)
    B_rho_kappa = compute_B_rho_kappa(rho, kappa, params)
    numerator = compute_numerator_a(rho, kappa, Delta, params)
    denominator = compute_denominator_a(rho, kappa, Delta, B_rho_kappa, params)
    a_rho_kappa, _, _ = compute_a_rho_kappa(
        rho, kappa, B_rho_kappa, numerator, denominator, params
    )

    # Leader's cost is RANDOM ~ N(mu_c, sigma_c^2), so E[p_1] = a + 0.5*mu_c
    p_1_bar = a_rho_kappa + 0.5 * params.mu_c

    consumer_surpluses = np.zeros(N)

    for i in range(N):
        # Same game sequence
        # CORRECTED: Leader (Firm 1) has RANDOM private cost, Follower (Firm 2) has FIXED public cost
        c_1 = rng.normal(params.mu_c, params.sigma_c)  # Leader's cost is RANDOM (private info - target of espionage!)
        c_2 = params.gamma  # Follower's cost is FIXED (public knowledge)

        p_1 = compute_p_1_star(a_rho_kappa, c_1)

        espionage_succeeds = rng.random() < rho

        if espionage_succeeds:
            noise_std = params.sigma_epsilon / np.sqrt(I_2_nash + params.iota)
            noise = rng.normal(0, noise_std)
            signal = p_1 + noise
        else:
            signal = 0.0

        p_2 = compute_p_2_star(
            rho, kappa, p_1_bar, c_2, params,
            espionage_success=espionage_succeeds,
            signal=signal
        )

        q_1 = compute_q_1_star(p_1, p_2, params)
        q_2 = compute_q_2_star(p_1, p_2, params)

        # Consumer surplus (equation 51): CS = ½(β·q₁² + 2δ·q₁·q₂ + β·q₂²)
        CS = 0.5 * (params.beta * q_1**2 + 2 * params.delta * q_1 * q_2 + params.beta * q_2**2)
        consumer_surpluses[i] = CS

    CS_expected = float(np.mean(consumer_surpluses))
    return CS_expected
