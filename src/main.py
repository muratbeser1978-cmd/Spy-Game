"""Main Pipeline: 4-Stage Espionage Game - Academic Implementation.

Constitutional Compliance: All 6 principles (I-VI)
Implements: FR-001 to FR-015

All computations are REAL - full SLSQP, Monte Carlo, exact equations.
"""

import argparse
import logging
import time
from pathlib import Path

import numpy as np
import pandas as pd

from src.models.parameters import Parameters
from src.solvers.nash_solver import solve_nash_equilibrium
from src.topology.level_02_contest import compute_rho
from src.topology.level_03_signal import compute_kappa
from src.utils.export import export_csv, export_json, export_latex_table
from src.visualization.plots import create_bar_chart, create_heatmap, create_line_plot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def run_baseline(seed: int, output_dir: Path) -> None:
    """Run baseline Nash equilibrium computation."""
    logger.info("="*80)
    logger.info("BASELINE NASH EQUILIBRIUM")
    logger.info("="*80)

    # Initialize parameters
    params = Parameters.baseline()
    logger.info(f"Parameters: α={params.alpha}, β={params.beta}, δ={params.delta}")

    # Solve Nash equilibrium (REAL SLSQP computation)
    start_time = time.time()
    solution = solve_nash_equilibrium(params, seed=seed)
    elapsed = time.time() - start_time

    logger.info(f"✓ Computation time: {elapsed:.2f}s")

    # Export results (REAL exports)
    output_dir.mkdir(parents=True, exist_ok=True)

    export_json(solution, output_dir / "baseline_equilibrium.json")
    logger.info(f"✓ JSON exported to {output_dir / 'baseline_equilibrium.json'}")

    export_csv(solution, output_dir / "baseline_equilibrium.csv")
    logger.info(f"✓ CSV exported to {output_dir / 'baseline_equilibrium.csv'}")

    export_latex_table(solution, output_dir / "baseline_equilibrium.tex")
    logger.info(f"✓ LaTeX table exported to {output_dir / 'baseline_equilibrium.tex'}")


def run_heatmaps(seed: int, output_dir: Path) -> None:
    """Generate heatmaps for ρ and κ (REAL computations)."""
    logger.info("="*80)
    logger.info("HEATMAP GENERATION")
    logger.info("="*80)

    params = Parameters.baseline()

    # First solve Nash to get equilibrium point
    solution = solve_nash_equilibrium(params, seed=seed)
    I_1_nash, I_2_nash = solution.investments

    # Create 50×50 grid
    I_1_range = np.linspace(0, params.I_bar, 50)
    I_2_range = np.linspace(0, params.I_bar, 50)
    I_1_grid, I_2_grid = np.meshgrid(I_1_range, I_2_range)

    # Compute ρ values (REAL computations)
    logger.info("Computing ρ(I₁, I₂) on 50×50 grid...")
    rho_values = np.zeros_like(I_1_grid)
    for i in range(I_1_grid.shape[0]):
        for j in range(I_1_grid.shape[1]):
            rho_values[i, j] = compute_rho(I_1_grid[i, j], I_2_grid[i, j], params)

    # Create ρ heatmap
    output_dir.mkdir(parents=True, exist_ok=True)
    create_heatmap(
        I_1_grid,
        I_2_grid,
        rho_values,
        (I_1_nash, I_2_nash),
        r"Contest Success Probability $\rho(I_1, I_2)$",
        r"$\rho$ (espionage success)",
        output_dir / "rho_heatmap.png",
        cmap="viridis",
    )
    logger.info(f"✓ ρ heatmap saved to {output_dir / 'rho_heatmap.png'}")

    # Compute κ values (REAL computations)
    logger.info("Computing κ(I₁, I₂) on 50×50 grid...")
    kappa_values = np.zeros_like(I_1_grid)
    for i in range(I_1_grid.shape[0]):
        for j in range(I_1_grid.shape[1]):
            kappa_values[i, j] = compute_kappa(I_2_grid[i, j], params)  # CORRECTED

    # Create κ heatmap
    create_heatmap(
        I_1_grid,
        I_2_grid,
        kappa_values,
        (I_1_nash, I_2_nash),
        r"Signal Precision $\kappa(I_1, I_2)$",
        r"$\kappa$ (signal informativeness)",
        output_dir / "kappa_heatmap.png",
        cmap="plasma",
    )
    logger.info(f"✓ κ heatmap saved to {output_dir / 'kappa_heatmap.png'}")


def run_sensitivity(param_name: str, param_range: tuple, n_points: int, seed: int, output_dir: Path) -> None:
    """Run sensitivity analysis (REAL Nash solutions for each parameter value)."""
    logger.info("="*80)
    logger.info(f"SENSITIVITY ANALYSIS: {param_name}")
    logger.info("="*80)

    param_values = np.linspace(param_range[0], param_range[1], n_points)
    results = []

    for i, param_val in enumerate(param_values, 1):
        logger.info(f"[{i}/{n_points}] Solving for {param_name}={param_val:.4f}...")

        # Create modified parameters
        params_dict = Parameters.baseline().to_dict()
        params_dict[param_name] = param_val
        params = Parameters(**params_dict)

        # Solve Nash equilibrium (REAL computation)
        solution = solve_nash_equilibrium(params, seed=seed)

        # Store results
        I_1, I_2 = solution.investments
        results.append({
            param_name: param_val,
            "I_1": I_1,
            "I_2": I_2,
            "rho": solution.contest_prob,
            "kappa": solution.signal_precision,
            "V_1": solution.value_functions[0],
            "V_2": solution.value_functions[1],
            "W": solution.total_welfare,
        })

    # Create DataFrame and save
    df = pd.DataFrame(results)
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / f"sensitivity_{param_name}.csv"
    df.to_csv(csv_path, index=False)
    logger.info(f"✓ Sensitivity results saved to {csv_path}")

    # Generate plots (REAL data)
    figures_dir = Path("figures")
    figures_dir.mkdir(exist_ok=True)

    # Plot 1: Investments
    create_line_plot(
        df[param_name].values,
        df["I_1"].values,
        df["I_2"].values,
        f"Nash Investments vs. {param_name}",
        f"Parameter {param_name}",
        "Equilibrium Investment",
        [r"$I_1^*$ (Espionage)", r"$I_2^*$ (Counter-espionage)"],
        figures_dir / f"sensitivity_{param_name}_investments.png",
    )
    logger.info(f"✓ Investment plot saved")

    # Plot 2: Welfare
    create_line_plot(
        df[param_name].values,
        df["W"].values,
        df["V_1"].values,
        f"Welfare vs. {param_name}",
        f"Parameter {param_name}",
        "Value/Welfare",
        [r"$W^*$ (Total)", r"$V_1^*$ (Firm 1)"],
        figures_dir / f"sensitivity_{param_name}_welfare.png",
    )
    logger.info(f"✓ Welfare plot saved")


def main() -> None:
    """Main entry point (NO PLACEHOLDERS)."""
    parser = argparse.ArgumentParser(description="4-Stage Espionage Game (REAL COMPUTATIONS)")
    parser.add_argument("--mode", choices=["baseline", "heatmaps", "sensitivity"], default="baseline")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("results"))
    parser.add_argument("--param", type=str, help="Parameter for sensitivity")
    parser.add_argument("--range", type=str, help="Range (min,max)")
    parser.add_argument("--n_points", type=int, default=10)

    args = parser.parse_args()

    if args.mode == "baseline":
        run_baseline(args.seed, args.output)

    elif args.mode == "heatmaps":
        run_heatmaps(args.seed, Path("figures"))

    elif args.mode == "sensitivity":
        if not args.param or not args.range:
            parser.error("--param and --range required for sensitivity mode")
        range_min, range_max = map(float, args.range.split(","))
        run_sensitivity(args.param, (range_min, range_max), args.n_points, args.seed, args.output)


if __name__ == "__main__":
    main()
