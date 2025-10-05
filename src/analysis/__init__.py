"""Analysis Module - Advanced theoretical components from the paper.

This module contains implementations of:
- Welfare decomposition (Theorem 6)
- Sequential vs information effect decomposition (Proposition 5)
- KKT verification (Theorem 5)
- Strategic interaction analysis (Lemma 2, Theorem 7)

These components go beyond the core game mechanics to provide
theoretical insights from the academic paper.
"""

from src.analysis.welfare_decomposition import (
    compute_welfare_decomposition,
    compute_chain_rule_decomposition,
    compute_dCS_dI2,
    compute_dV1_dI2,
    compute_dV2_dI2,
)

from src.analysis.effect_decomposition import (
    compute_effect_decomposition,
    compute_benchmark_nash_profits,
    compute_hybrid_stackelberg_profits,
    compute_full_game_profits,
    analyze_information_value,
)

from src.analysis.kkt_verification import (
    verify_kkt_conditions,
    format_kkt_report,
    KKTDiagnostics,
)

from src.analysis.strategic_interaction import (
    analyze_strategic_interaction,
    compute_cross_partial_rho,
    compute_threshold_I2,
    compute_strategic_interaction_map,
    format_strategic_interaction_report,
    StrategicInteractionDiagnostics,
)

__all__ = [
    # Welfare decomposition
    'compute_welfare_decomposition',
    'compute_chain_rule_decomposition',
    'compute_dCS_dI2',
    'compute_dV1_dI2',
    'compute_dV2_dI2',
    # Effect decomposition
    'compute_effect_decomposition',
    'compute_benchmark_nash_profits',
    'compute_hybrid_stackelberg_profits',
    'compute_full_game_profits',
    'analyze_information_value',
    # KKT verification
    'verify_kkt_conditions',
    'format_kkt_report',
    'KKTDiagnostics',
    # Strategic interaction
    'analyze_strategic_interaction',
    'compute_cross_partial_rho',
    'compute_threshold_I2',
    'compute_strategic_interaction_map',
    'format_strategic_interaction_report',
    'StrategicInteractionDiagnostics',
]
