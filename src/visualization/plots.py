"""Publication-Quality Visualization Functions.

Implements: FR-015 (4 PNG visualizations, 300 DPI)
"""

from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure


def create_heatmap(
    I_1_grid: np.ndarray,
    I_2_grid: np.ndarray,
    values: np.ndarray,
    nash_marker: Tuple[float, float],
    title: str,
    colorbar_label: str,
    filepath: str | Path,
    cmap: str = "viridis",
) -> None:
    """Create heatmap with Nash equilibrium marker.

    Args:
        I_1_grid: 2D grid for I₁ values (from meshgrid)
        I_2_grid: 2D grid for I₂ values (from meshgrid)
        values: 2D array of function values (e.g., ρ, κ)
        nash_marker: (I₁*, I₂*) Nash equilibrium point
        title: Plot title
        colorbar_label: Colorbar label
        filepath: Output path (e.g., 'figures/rho_heatmap.png')
        cmap: Colormap name (default 'viridis', colorblind-friendly)

    Implements: FR-015 (300 DPI, colorblind palettes)
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6))

    # Create contour plot
    contour = ax.contourf(I_1_grid, I_2_grid, values, levels=20, cmap=cmap)

    # Add colorbar
    cbar = fig.colorbar(contour, ax=ax)
    cbar.set_label(colorbar_label, fontsize=11)

    # Mark Nash equilibrium
    ax.plot(
        nash_marker[0],
        nash_marker[1],
        "r*",
        markersize=20,
        markeredgecolor="white",
        markeredgewidth=1.5,
        label=f"Nash: ({nash_marker[0]:.2f}, {nash_marker[1]:.2f})",
    )

    # Labels and title
    ax.set_xlabel(r"Firm 1 Investment $I_1$", fontsize=12)
    ax.set_ylabel(r"Firm 2 Investment $I_2$", fontsize=12)
    ax.set_title(title, fontsize=13)
    ax.legend(loc="best", frameon=True, shadow=True)
    ax.grid(True, alpha=0.3, linestyle="--")

    fig.tight_layout()
    fig.savefig(filepath, dpi=300, bbox_inches="tight")
    plt.close(fig)


def create_line_plot(
    x_values: np.ndarray,
    y1_values: np.ndarray,
    y2_values: np.ndarray,
    title: str,
    xlabel: str,
    ylabel: str,
    legend: List[str],
    filepath: str | Path,
) -> None:
    """Create line plot with two series.

    Args:
        x_values: X-axis values
        y1_values: First series (e.g., I₁*)
        y2_values: Second series (e.g., I₂*)
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        legend: Legend labels [series1, series2]
        filepath: Output path

    Implements: FR-015
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.plot(x_values, y1_values, "o-", label=legend[0], linewidth=2, markersize=5)
    ax.plot(x_values, y2_values, "s-", label=legend[1], linewidth=2, markersize=5)

    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=13)
    ax.legend(frameon=True, shadow=True)
    ax.grid(True, alpha=0.3, linestyle="--")

    fig.tight_layout()
    fig.savefig(filepath, dpi=300, bbox_inches="tight")
    plt.close(fig)


def create_bar_chart(
    components: List[str],
    values: List[float],
    total: float,
    title: str,
    filepath: str | Path,
) -> None:
    """Create bar chart with total welfare line.

    Args:
        components: Component names (e.g., ['CS', 'V_1', 'V_2'])
        values: Component values
        total: Total welfare (horizontal line overlay)
        title: Plot title
        filepath: Output path

    Implements: FR-015
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6))

    # Bar chart
    x_pos = np.arange(len(components))
    bars = ax.bar(x_pos, values, color=["#1f77b4", "#ff7f0e", "#2ca02c"], alpha=0.8)

    # Total line
    ax.axhline(
        y=total, color="red", linestyle="--", linewidth=2, label=f"Total: {total:.2f}"
    )

    # Labels
    ax.set_xlabel("Welfare Component", fontsize=12)
    ax.set_ylabel("Value", fontsize=12)
    ax.set_title(title, fontsize=13)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(components)
    ax.legend(frameon=True, shadow=True)
    ax.grid(True, alpha=0.3, linestyle="--", axis="y")

    fig.tight_layout()
    fig.savefig(filepath, dpi=300, bbox_inches="tight")
    plt.close(fig)
