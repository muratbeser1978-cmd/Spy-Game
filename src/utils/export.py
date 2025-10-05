"""Export Utilities for Results.

Implements: FR-013 (JSON export), FR-014 (CSV export)
"""

import json
from pathlib import Path
from typing import Any, Dict

import pandas as pd

from src.models.solution import EquilibriumSolution


def export_json(solution: EquilibriumSolution, filepath: str | Path) -> None:
    """Export equilibrium solution to JSON file.

    Args:
        solution: Equilibrium solution object
        filepath: Output path (e.g., 'results/baseline.json')

    Implements: FR-013
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Convert to dictionary
    data = solution.to_dict()

    # Write JSON with indentation
    with filepath.open("w") as f:
        json.dump(data, f, indent=2)


def export_csv(solution: EquilibriumSolution, filepath: str | Path) -> None:
    """Export equilibrium solution to CSV file.

    Args:
        solution: Equilibrium solution object
        filepath: Output path (e.g., 'results/baseline.csv')

    Implements: FR-014
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Create DataFrame
    data = solution.to_dict()

    # Flatten nested structure
    rows = []
    for category, values in data.items():
        if isinstance(values, dict):
            for var, val in values.items():
                rows.append({"Category": category, "Variable": var, "Value": val})
        else:
            rows.append({"Category": "meta", "Variable": category, "Value": values})

    df = pd.DataFrame(rows)

    # Save to CSV
    df.to_csv(filepath, index=False)


def export_latex_table(
    solution: EquilibriumSolution, filepath: str | Path, caption: str = "Nash Equilibrium"
) -> None:
    """Export equilibrium solution as LaTeX table.

    Args:
        solution: Equilibrium solution object
        filepath: Output path (e.g., 'results/baseline.tex')
        caption: Table caption
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    I_1, I_2 = solution.investments
    V_1, V_2 = solution.value_functions
    U_1, U_2 = solution.utilities

    latex_code = r"""\begin{table}[htbp]
\centering
\caption{""" + caption + r"""}
\label{tab:equilibrium}
\begin{tabular}{llr}
\toprule
Variable & Symbol & Value \\
\midrule
\multicolumn{3}{l}{\textit{Investments}} \\
Firm 1 espionage & $I_1^*$ & """ + f"{I_1:.4f}" + r""" \\
Firm 2 counter-espionage & $I_2^*$ & """ + f"{I_2:.4f}" + r""" \\
\midrule
\multicolumn{3}{l}{\textit{Information}} \\
Success probability & $\rho^*$ & """ + f"{solution.contest_prob:.4f}" + r""" \\
Signal precision & $\kappa^*$ & """ + f"{solution.signal_precision:.4f}" + r""" \\
\midrule
\multicolumn{3}{l}{\textit{Values}} \\
Firm 1 profit & $V_1^*$ & """ + f"{V_1:.2f}" + r""" \\
Firm 2 profit & $V_2^*$ & """ + f"{V_2:.2f}" + r""" \\
Firm 1 utility & $U_1^*$ & """ + f"{U_1:.2f}" + r""" \\
Firm 2 utility & $U_2^*$ & """ + f"{U_2:.2f}" + r""" \\
\midrule
\multicolumn{3}{l}{\textit{Welfare}} \\
Consumer surplus & $CS^*$ & """ + f"{solution.consumer_surplus:.2f}" + r""" \\
Total welfare & $W^*$ & """ + f"{solution.total_welfare:.2f}" + r""" \\
\bottomrule
\end{tabular}
\end{table}
"""

    filepath.write_text(latex_code)
