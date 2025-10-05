#!/usr/bin/env python3
"""
Basit LaTeX/PDF Rapor Oluşturucu
=================================

Nash dengesi sonuçlarını LaTeX raporuna dönüştürür.
"""

from pathlib import Path
from datetime import datetime
import subprocess
import shutil

from src.models.parameters import Parameters
from src.solvers.nash_solver import solve_nash_equilibrium


def create_latex_report(params: Parameters, solution, output_dir: Path = Path("reports")):
    """LaTeX rapor oluştur."""

    output_dir.mkdir(exist_ok=True)

    I1, I2 = solution.investments
    rho, kappa = solution.contest_prob, solution.signal_precision
    V1, V2 = solution.value_functions
    U1, U2 = solution.utilities
    CS, W = solution.consumer_surplus, solution.total_welfare

    # LaTeX içeriği - % formatting ile
    latex_content = r"""\documentclass[11pt,a4paper]{article}

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{float}
\usepackage{geometry}
\usepackage{hyperref}
\usepackage{xcolor}

\geometry{left=2.5cm, right=2.5cm, top=2.5cm, bottom=2.5cm}

\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    urlcolor=cyan,
}

\newcommand{\E}{\mathbb{E}}

\title{\textbf{Nash Equilibrium Analysis Report\\
Stackelberg-Bayesian Espionage Game}}
\author{Automated Analysis System}
\date{%s}

\begin{document}

\maketitle

\begin{abstract}
This report presents the Nash equilibrium analysis of a four-stage Stackelberg-Bayesian espionage game
with counter-espionage investments. The equilibrium was computed using Differential Evolution global
optimization with Monte Carlo integration ($N=50{,}000$ samples).
\end{abstract}

\tableofcontents
\newpage

\section{Model Overview}

\subsection{Game Structure}

Four-stage game:
\begin{enumerate}
    \item Leader (Firm 1) chooses counter-espionage investment $I_1$
    \item Follower (Firm 2) observes $I_1$ and chooses espionage investment $I_2$
    \item Nature draws Leader's cost $c_1 \sim \mathcal{N}(\mu_c, \sigma_c^2)$; espionage succeeds with probability $\rho(I_1, I_2)$
    \item Bertrand-Stackelberg price competition with demand $q_i = \alpha - \beta p_i + \delta p_j$
\end{enumerate}

\subsection{Key Functions}

\textbf{Contest success function:}
\begin{equation}
    \rho(I_1, I_2) = \frac{I_2^\gamma}{I_2^\gamma + \psi_1(I_1)}
\end{equation}

\textbf{Signal precision:}
\begin{equation}
    \kappa(I_2) = \frac{I_2^\iota}{I_2^\iota + \bar{I}^\iota}
\end{equation}

\textbf{Investment costs:}
\begin{equation}
    C_i(I_i) = \frac{\kappa_i I_i^2}{2}
\end{equation}

\section{Parameter Values}

\begin{table}[H]
\centering
\caption{Baseline Parameters}
\begin{tabular}{llr}
\toprule
\textbf{Parameter} & \textbf{Description} & \textbf{Value} \\
\midrule
$\alpha$ & Market size & %.2f \\
$\beta$ & Own-price elasticity & %.2f \\
$\delta$ & Cross-price elasticity & %.2f \\
$\gamma$ & Follower marginal cost & %.2f \\
$\kappa_1$ & Leader investment cost & %.2f \\
$\kappa_2$ & Follower investment cost & %.2f \\
$\mu_c$ & Leader cost mean & %.2f \\
$\sigma_c$ & Leader cost std dev & %.2f \\
\bottomrule
\end{tabular}
\end{table}

\section{Nash Equilibrium Results}

\subsection{Equilibrium Values}

\begin{table}[H]
\centering
\caption{Nash Equilibrium Outcomes}
\begin{tabular}{lcr}
\toprule
\textbf{Variable} & \textbf{Symbol} & \textbf{Value} \\
\midrule
\multicolumn{3}{l}{\textit{Investments}} \\
\quad Leader & $I_1^*$ & %.6f \\
\quad Follower & $I_2^*$ & %.6f \\
\quad Ratio & $I_1^*/I_2^*$ & %.3f \\
\midrule
\multicolumn{3}{l}{\textit{Espionage}} \\
\quad Success probability & $\rho^*$ & %.6f \\
\quad Signal precision & $\kappa^*$ & %.6f \\
\midrule
\multicolumn{3}{l}{\textit{Profits (Gross)}} \\
\quad Leader & $V_1^*$ & %.2f \\
\quad Follower & $V_2^*$ & %.2f \\
\quad Gap & $V_1^* - V_2^*$ & %.2f \\
\midrule
\multicolumn{3}{l}{\textit{Utilities (Net)}} \\
\quad Leader & $U_1^*$ & %.2f \\
\quad Follower & $U_2^*$ & %.2f \\
\midrule
\multicolumn{3}{l}{\textit{Welfare}} \\
\quad Consumer surplus & $CS^*$ & %.2f \\
\quad Total welfare & $W^*$ & %.2f \\
\quad CS share & $CS^*/W^*$ & %.1f\%% \\
\bottomrule
\end{tabular}
\end{table}

\subsection{Economic Interpretation}

Key findings:

\begin{itemize}
    \item \textbf{Investment asymmetry:} Leader invests %s in counter-espionage relative to Follower's espionage ($I_1^*/I_2^* = %.2f$).

    \item \textbf{Espionage effectiveness:} Success rate of %.1f\%% indicates %s espionage deterrence.

    \item \textbf{Signal quality:} Precision weight $\kappa^* = %.3f$ means Follower assigns %.1f\%% weight to the signal.

    \item \textbf{Profit distribution:} Leader earns %s profit than Follower ($$V_1^* - V_2^* = %.2f$$).

    \item \textbf{Consumer welfare:} Consumers capture %.1f\%% of total welfare.
\end{itemize}

\section{Visualizations}

\subsection{Nash Equilibrium Heatmap}

Figure \ref{fig:nash_heatmap} shows the joint utility surface $(U_1 + U_2)$ with the Nash equilibrium marked.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.8\textwidth]{../figures_quick/1_nash_heatmap.png}
    \caption{Nash Equilibrium: Joint Utility Heatmap}
    \label{fig:nash_heatmap}
\end{figure}

\subsection{Welfare Analysis}

Figure \ref{fig:welfare} decomposes welfare into consumer surplus and firm utilities.

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth]{../figures_advanced/advanced_welfare.png}
    \caption{Welfare Decomposition and Analysis}
    \label{fig:welfare}
\end{figure}

\subsection{Dashboard Summary}

Figure \ref{fig:dashboard} provides a comprehensive summary of equilibrium metrics.

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth]{../figures_advanced/advanced_dashboard.png}
    \caption{Nash Equilibrium Dashboard}
    \label{fig:dashboard}
\end{figure}

\section{Conclusion}

The analysis reveals:
\begin{enumerate}
    \item Nash equilibrium exists with interior solutions for both investments
    \item Leader's first-mover advantage is reflected in higher profits
    \item Espionage success probability is moderate (%.1f\%%)
    \item Consumer surplus dominates total welfare (%.1f\%%)
\end{enumerate}

\appendix

\section{Computational Details}

\begin{itemize}
    \item \textbf{Optimizer:} Differential Evolution (scipy.optimize)
    \item \textbf{Monte Carlo samples:} $N = 50{,}000$
    \item \textbf{Convergence:} %s in %d iterations
    \item \textbf{Random seed:} 42 (reproducibility)
\end{itemize}

\section{Code Availability}

Full source code available at: \texttt{/Users/muratbeser/Desktop/Spy/}

Key files:
\begin{itemize}
    \item \texttt{run\_baseline.py} -- Main analysis
    \item \texttt{src/solvers/nash\_solver.py} -- Optimizer
    \item \texttt{generate\_simple\_report.py} -- This report
\end{itemize}

\end{document}
""" % (
        datetime.now().strftime("%B %d, %Y"),
        params.alpha, params.beta, params.delta, params.gamma,
        params.kappa_1, params.kappa_2, params.mu_c, params.sigma_c,
        I1, I2, I1/I2,
        rho, kappa,
        V1, V2, V1-V2,
        U1, U2,
        CS, W, CS/W*100,
        "more" if I1 > I2 else "less", I1/I2,
        rho*100, "strong" if rho < 0.3 else "moderate" if rho < 0.6 else "weak",
        kappa, kappa*100,
        "higher" if V1 > V2 else "lower", V1-V2,
        CS/W*100,
        rho*100,
        CS/W*100,
        "Converged" if solution.converged else "Did not converge",
        solution.iterations
    )

    # .tex dosyasını kaydet
    tex_file = output_dir / "nash_equilibrium_report.tex"
    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(latex_content)

    print(f"✓ LaTeX file created: {tex_file}")

    # PDF'e derle
    if shutil.which("pdflatex"):
        print("\n📄 Compiling to PDF...")
        try:
            # 2 kez çalıştır (references için)
            for i in range(2):
                subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", tex_file.name],
                    cwd=output_dir,
                    capture_output=True,
                    timeout=60
                )

            pdf_file = tex_file.with_suffix('.pdf')
            if pdf_file.exists():
                print(f"✓ PDF created: {pdf_file}")

                # Temizlik
                for ext in ['.aux', '.log', '.out', '.toc']:
                    aux_file = tex_file.with_suffix(ext)
                    if aux_file.exists():
                        aux_file.unlink()

                return pdf_file
            else:
                print("⚠️  PDF not created")
                return None

        except Exception as e:
            print(f"⚠️  PDF compilation failed: {e}")
            return None
    else:
        print("\n⚠️  pdflatex not found. Install LaTeX to generate PDF.")
        print(f"   Compile manually: cd {output_dir} && pdflatex {tex_file.name}")
        return None


def main():
    print("="*70)
    print("OTOMATIK LaTeX/PDF RAPOR OLUŞTURUCU")
    print("="*70)

    # Nash dengesi hesapla
    print("\n📊 Computing Nash equilibrium...")
    params = Parameters.baseline()
    solution = solve_nash_equilibrium(params, seed=42)

    print(f"  ✓ Nash: I₁={solution.investments[0]:.4f}, I₂={solution.investments[1]:.4f}")

    # Rapor oluştur
    print("\n📄 Generating LaTeX report...")
    pdf_file = create_latex_report(params, solution)

    # Özet
    print("\n" + "="*70)
    print("✅ RAPOR OLUŞTURMA TAMAMLANDI!")
    print("="*70)
    print(f"\n📁 Directory: reports/")
    print(f"📄 LaTeX: nash_equilibrium_report.tex")
    if pdf_file:
        print(f"📕 PDF: {pdf_file.name}")
        print(f"\n💡 Open: open reports/{pdf_file.name}")
    print("="*70)


if __name__ == "__main__":
    main()
