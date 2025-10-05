"""Fixed-Point Solver via Successive Approximation.

Constitutional Compliance:
- Principle IV: Reproducibility & Validation (convergence criteria)
- Principle V: Algorithm Transparency (iteration diagnostics)
- Principle VI: Documentation Standards

Implements: FR-008 (Fixed-point for a_{ρ,κ}, tolerance=1e-6, max_iter=100)
"""

import logging
from typing import Callable, Tuple

# Configure logger
logger = logging.getLogger(__name__)


def solve_fixed_point(
    f: Callable[[float], float],
    x0: float,
    tol: float = 1e-6,
    max_iter: int = 100,
) -> Tuple[float, int, bool]:
    """Solve x = f(x) via successive approximation (Banach iteration).

    Algorithm (research.md decision 4):
        Given mapping f: ℝ → ℝ and initial guess x₀
        Iterate: x^{n+1} = f(x^n)
        Until: |x^{n+1} - x^n| < tol or n == max_iter

    Convergence Guarantee:
        If f is a contraction mapping (|f'(x)| < 1), Banach Fixed-Point
        Theorem guarantees convergence to unique fixed-point.

    Args:
        f: Function defining fixed-point equation x = f(x)
           Typically for a_{ρ,κ}: f(a) = [numerator(a)] / [denominator(a)]
        x0: Initial guess (typically midpoint or analytical approximation)
        tol: Convergence tolerance |x^{n+1} - x^n| < tol (default 1e-6 per FR-008)
        max_iter: Maximum iterations (default 100 per FR-008)

    Returns:
        Tuple[float, int, bool]:
            - x_final: Converged value (or last iteration if not converged)
            - iter_count: Number of iterations performed
            - converged: True if |residual| < tol, False if max_iter reached

    Mathematical Source:
        Banach Fixed-Point Theorem: Kreyszig (1978), Section 2.5
        research.md decision 4: Successive approximation chosen for transparency

    Convergence Diagnostics (FR-012):
        - Iteration count logged
        - Final residual logged
        - Warning if max_iter reached without convergence

    Constitutional Principle:
        V. Algorithm Transparency - Simple one-line iteration, explicit diagnostics
    """
    x = x0

    for iter_count in range(max_iter):
        # Fixed-point iteration: x^{n+1} = f(x^n)
        x_new = f(x)

        # Compute residual for convergence check
        residual = abs(x_new - x)

        # Check convergence
        if residual < tol:
            logger.info(
                f"Fixed-point converged in {iter_count + 1} iterations, "
                f"residual={residual:.6e}"
            )
            return x_new, iter_count + 1, True

        # Update for next iteration
        x = x_new

    # Max iterations reached without convergence
    logger.warning(
        f"Fixed-point did not converge in {max_iter} iterations, "
        f"final residual={residual:.6e}"
    )
    return x, max_iter, False


def solve_fixed_point_with_relaxation(
    f: Callable[[float], float],
    x0: float,
    theta: float = 0.5,
    tol: float = 1e-6,
    max_iter: int = 100,
) -> Tuple[float, int, bool]:
    """Solve x = f(x) with relaxation parameter θ ∈ (0,1).

    Relaxation iteration: x^{n+1} = θ·f(x^n) + (1-θ)·x^n

    Use this variant if standard successive approximation oscillates.
    Smaller θ → more damping → slower but more stable convergence.

    Args:
        f: Fixed-point function
        x0: Initial guess
        theta: Relaxation parameter θ ∈ (0,1), default 0.5
               θ=1 → standard successive approximation
               θ→0 → heavy damping
        tol: Convergence tolerance
        max_iter: Maximum iterations

    Returns:
        Tuple[float, int, bool]: (solution, iterations, converged)

    Note:
        Typically not needed for well-behaved contractions, but available
        if numerical stability issues arise.
    """
    assert 0 < theta <= 1, f"Relaxation parameter must be in (0,1], got {theta}"

    x = x0

    for iter_count in range(max_iter):
        # Relaxed iteration
        x_new = theta * f(x) + (1 - theta) * x

        residual = abs(x_new - x)

        if residual < tol:
            logger.info(
                f"Relaxed fixed-point converged in {iter_count + 1} iterations "
                f"(θ={theta:.2f}), residual={residual:.6e}"
            )
            return x_new, iter_count + 1, True

        x = x_new

    logger.warning(
        f"Relaxed fixed-point did not converge in {max_iter} iterations "
        f"(θ={theta:.2f}), final residual={residual:.6e}"
    )
    return x, max_iter, False
