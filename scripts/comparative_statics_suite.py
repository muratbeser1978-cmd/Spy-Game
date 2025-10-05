#!/usr/bin/env python3
"""
Karşılaştırmalı Statikler Analiz Paketi
========================================

Tüm parametreler için sistematik karşılaştırmalı statikler analizi:
- Her parametre için dengede değişim grafikleri
- Elastiklik hesaplamaları
- Threshold (rejim değişimi) tespiti
- Otomatik LaTeX tablo oluşturma
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Tuple, Any
import pandas as pd
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

from src.models.parameters import Parameters
from src.solvers.nash_solver import solve_nash_equilibrium

# Görselleştirme ayarları
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 100

OUTPUT_DIR = Path("figures_comparative_statics")
OUTPUT_DIR.mkdir(exist_ok=True)

LATEX_DIR = Path("tables")
LATEX_DIR.mkdir(exist_ok=True)


class ComparativeStaticsAnalyzer:
    """Karşılaştırmalı statikler analiz sınıfı."""

    def __init__(self, baseline_params: Parameters, n_points: int = 15, seed: int = 42):
        """
        Parameters
        ----------
        baseline_params : Parameters
            Baseline parametre seti
        n_points : int
            Her parametre için kaç nokta hesaplanacak
        seed : int
            Random seed (tekrarlanabilirlik için)
        """
        self.baseline = baseline_params
        self.n_points = n_points
        self.seed = seed

        # Sonuçları sakla
        self.results: Dict[str, pd.DataFrame] = {}

    def analyze_parameter(
        self,
        param_name: str,
        param_range: Tuple[float, float],
        log_scale: bool = False
    ) -> pd.DataFrame:
        """
        Tek bir parametre için karşılaştırmalı statikler analizi.

        Parameters
        ----------
        param_name : str
            Analiz edilecek parametre adı (ör: 'gamma', 'alpha')
        param_range : Tuple[float, float]
            (min, max) aralığı
        log_scale : bool
            Logaritmik ölçek kullanılacak mı?

        Returns
        -------
        pd.DataFrame
            Sonuç tablosu
        """
        print(f"\n{'='*60}")
        print(f"Analyzing: {param_name}")
        print(f"Range: {param_range[0]:.2f} → {param_range[1]:.2f}")
        print(f"{'='*60}")

        # Parametre değerlerini oluştur
        if log_scale:
            param_values = np.logspace(
                np.log10(param_range[0]),
                np.log10(param_range[1]),
                self.n_points
            )
        else:
            param_values = np.linspace(param_range[0], param_range[1], self.n_points)

        # Sonuçları sakla
        results = {
            param_name: [],
            'I1_star': [], 'I2_star': [],
            'rho_star': [], 'kappa_star': [],
            'V1_star': [], 'V2_star': [],
            'U1_star': [], 'U2_star': [],
            'CS_star': [], 'W_star': [],
            'converged': []
        }

        # Her parametre değeri için Nash dengesi çöz
        for val in tqdm(param_values, desc=f"{param_name}"):
            # Parametreyi güncelle
            params_dict = self.baseline.to_dict()
            params_dict[param_name] = val
            params = Parameters(**params_dict)

            # Nash dengesi çöz
            try:
                solution = solve_nash_equilibrium(params, seed=self.seed)

                results[param_name].append(val)
                results['I1_star'].append(solution.investments[0])
                results['I2_star'].append(solution.investments[1])
                results['rho_star'].append(solution.contest_prob)
                results['kappa_star'].append(solution.signal_precision)
                results['V1_star'].append(solution.value_functions[0])
                results['V2_star'].append(solution.value_functions[1])
                results['U1_star'].append(solution.utilities[0])
                results['U2_star'].append(solution.utilities[1])
                results['CS_star'].append(solution.consumer_surplus)
                results['W_star'].append(solution.total_welfare)
                results['converged'].append(solution.converged)
            except Exception as e:
                print(f"  Warning: Failed at {param_name}={val:.3f}: {e}")
                continue

        df = pd.DataFrame(results)
        self.results[param_name] = df

        print(f"✓ Completed: {len(df)} successful solutions")
        return df

    def compute_elasticities(self, param_name: str) -> pd.DataFrame:
        """
        Elastiklik hesapla: ε_{Y,X} = (∂Y/∂X) × (X/Y)

        Parameters
        ----------
        param_name : str
            Parametre adı

        Returns
        -------
        pd.DataFrame
            Elastiklik tablosu
        """
        df = self.results[param_name]

        # Türevleri numerical olarak hesapla
        param_vals = df[param_name].values

        elasticities = {
            param_name: param_vals[:-1],  # Son nokta hariç
        }

        outcome_vars = ['I1_star', 'I2_star', 'rho_star', 'kappa_star',
                       'V1_star', 'V2_star', 'U1_star', 'U2_star',
                       'CS_star', 'W_star']

        for var in outcome_vars:
            Y = df[var].values
            dY = np.diff(Y)
            dX = np.diff(param_vals)

            # ε = (dY/dX) × (X/Y)
            # Orta noktalarda hesapla
            X_mid = (param_vals[:-1] + param_vals[1:]) / 2
            Y_mid = (Y[:-1] + Y[1:]) / 2

            with np.errstate(divide='ignore', invalid='ignore'):
                elasticity = (dY / dX) * (X_mid / Y_mid)
                elasticity = np.nan_to_num(elasticity, nan=0.0, posinf=0.0, neginf=0.0)

            elasticities[f'epsilon_{var}'] = elasticity

        return pd.DataFrame(elasticities)

    def plot_comparative_statics(self, param_name: str, save: bool = True):
        """
        Karşılaştırmalı statikler için kapsamlı grafik paketi oluştur.

        Parameters
        ----------
        param_name : str
            Parametre adı
        save : bool
            Grafikleri kaydet
        """
        df = self.results[param_name]
        param_vals = df[param_name].values

        fig = plt.figure(figsize=(20, 12))
        fig.suptitle(f'Comparative Statics: {param_name.upper()}',
                     fontsize=16, fontweight='bold', y=0.995)

        # 4x3 grid
        gs = fig.add_gridspec(4, 3, hspace=0.35, wspace=0.3)

        # ============================================================
        # Row 1: Investments
        # ============================================================
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.plot(param_vals, df['I1_star'], 'o-', label='$I_1^*$ (Leader)',
                color='#3498db', linewidth=2, markersize=6)
        ax1.plot(param_vals, df['I2_star'], 's-', label='$I_2^*$ (Follower)',
                color='#e74c3c', linewidth=2, markersize=6)
        ax1.set_xlabel(param_name, fontweight='bold')
        ax1.set_ylabel('Investment', fontweight='bold')
        ax1.set_title('Nash Investments', fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Espionage parameters
        ax2 = fig.add_subplot(gs[0, 1])
        ax2_twin = ax2.twinx()
        l1 = ax2.plot(param_vals, df['rho_star'], 'o-', label='$\\rho^*$ (Success)',
                     color='#3498db', linewidth=2, markersize=6)
        l2 = ax2_twin.plot(param_vals, df['kappa_star'], 's-', label='$\\kappa^*$ (Precision)',
                          color='#e74c3c', linewidth=2, markersize=6)
        ax2.set_xlabel(param_name, fontweight='bold')
        ax2.set_ylabel('$\\rho^*$', fontweight='bold', color='#3498db')
        ax2_twin.set_ylabel('$\\kappa^*$', fontweight='bold', color='#e74c3c')
        ax2.tick_params(axis='y', labelcolor='#3498db')
        ax2_twin.tick_params(axis='y', labelcolor='#e74c3c')
        ax2.set_title('Espionage Parameters', fontweight='bold')
        ax2.grid(True, alpha=0.3)

        # Investment ratio
        ax3 = fig.add_subplot(gs[0, 2])
        ratio = df['I1_star'] / df['I2_star']
        ax3.plot(param_vals, ratio, 'o-', color='#9b59b6', linewidth=2, markersize=6)
        ax3.axhline(y=1, color='red', linestyle='--', linewidth=2, alpha=0.5)
        ax3.set_xlabel(param_name, fontweight='bold')
        ax3.set_ylabel('$I_1^* / I_2^*$', fontweight='bold')
        ax3.set_title('Investment Ratio', fontweight='bold')
        ax3.grid(True, alpha=0.3)

        # ============================================================
        # Row 2: Profits
        # ============================================================
        ax4 = fig.add_subplot(gs[1, 0])
        ax4.plot(param_vals, df['V1_star'], 'o-', label='$V_1^*$ (Leader)',
                color='#3498db', linewidth=2, markersize=6)
        ax4.plot(param_vals, df['V2_star'], 's-', label='$V_2^*$ (Follower)',
                color='#e74c3c', linewidth=2, markersize=6)
        ax4.set_xlabel(param_name, fontweight='bold')
        ax4.set_ylabel('Gross Profit', fontweight='bold')
        ax4.set_title('Expected Profits (Gross)', fontweight='bold')
        ax4.legend()
        ax4.grid(True, alpha=0.3)

        ax5 = fig.add_subplot(gs[1, 1])
        ax5.plot(param_vals, df['U1_star'], 'o-', label='$U_1^*$ (Leader)',
                color='#3498db', linewidth=2, markersize=6)
        ax5.plot(param_vals, df['U2_star'], 's-', label='$U_2^*$ (Follower)',
                color='#e74c3c', linewidth=2, markersize=6)
        ax5.set_xlabel(param_name, fontweight='bold')
        ax5.set_ylabel('Net Utility', fontweight='bold')
        ax5.set_title('Net Utilities', fontweight='bold')
        ax5.legend()
        ax5.grid(True, alpha=0.3)

        ax6 = fig.add_subplot(gs[1, 2])
        profit_gap = df['V1_star'] - df['V2_star']
        ax6.plot(param_vals, profit_gap, 'o-', color='#9b59b6', linewidth=2, markersize=6)
        ax6.axhline(y=0, color='red', linestyle='--', linewidth=2, alpha=0.5)
        ax6.set_xlabel(param_name, fontweight='bold')
        ax6.set_ylabel('$V_1^* - V_2^*$', fontweight='bold')
        ax6.set_title('Profit Gap (Leader Advantage)', fontweight='bold')
        ax6.grid(True, alpha=0.3)

        # ============================================================
        # Row 3: Welfare
        # ============================================================
        ax7 = fig.add_subplot(gs[2, 0])
        ax7.plot(param_vals, df['CS_star'], 'o-', label='CS',
                color='#2ecc71', linewidth=2, markersize=6)
        ax7.set_xlabel(param_name, fontweight='bold')
        ax7.set_ylabel('Consumer Surplus', fontweight='bold')
        ax7.set_title('Consumer Surplus', fontweight='bold')
        ax7.grid(True, alpha=0.3)

        ax8 = fig.add_subplot(gs[2, 1])
        ax8.plot(param_vals, df['W_star'], 'o-', label='W',
                color='#f39c12', linewidth=2, markersize=6)
        ax8.set_xlabel(param_name, fontweight='bold')
        ax8.set_ylabel('Total Welfare', fontweight='bold')
        ax8.set_title('Total Welfare', fontweight='bold')
        ax8.grid(True, alpha=0.3)

        ax9 = fig.add_subplot(gs[2, 2])
        # Welfare shares
        cs_share = df['CS_star'] / df['W_star'] * 100
        u1_share = df['U1_star'] / df['W_star'] * 100
        u2_share = df['U2_star'] / df['W_star'] * 100
        ax9.plot(param_vals, cs_share, 'o-', label='CS %', color='#2ecc71', linewidth=2, markersize=5)
        ax9.plot(param_vals, u1_share, 's-', label='$U_1$ %', color='#3498db', linewidth=2, markersize=5)
        ax9.plot(param_vals, u2_share, '^-', label='$U_2$ %', color='#e74c3c', linewidth=2, markersize=5)
        ax9.set_xlabel(param_name, fontweight='bold')
        ax9.set_ylabel('Welfare Share (%)', fontweight='bold')
        ax9.set_title('Welfare Distribution', fontweight='bold')
        ax9.legend()
        ax9.grid(True, alpha=0.3)

        # ============================================================
        # Row 4: Derivatives and Elasticities
        # ============================================================
        # Numerical derivatives
        ax10 = fig.add_subplot(gs[3, 0])
        dI1 = np.gradient(df['I1_star'].values, param_vals)
        dI2 = np.gradient(df['I2_star'].values, param_vals)
        ax10.plot(param_vals, dI1, 'o-', label='$\\partial I_1^*/\\partial$' + param_name,
                 color='#3498db', linewidth=2, markersize=6)
        ax10.plot(param_vals, dI2, 's-', label='$\\partial I_2^*/\\partial$' + param_name,
                 color='#e74c3c', linewidth=2, markersize=6)
        ax10.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.3)
        ax10.set_xlabel(param_name, fontweight='bold')
        ax10.set_ylabel('Derivative', fontweight='bold')
        ax10.set_title('Investment Derivatives', fontweight='bold')
        ax10.legend()
        ax10.grid(True, alpha=0.3)

        ax11 = fig.add_subplot(gs[3, 1])
        dW = np.gradient(df['W_star'].values, param_vals)
        dCS = np.gradient(df['CS_star'].values, param_vals)
        ax11.plot(param_vals, dW, 'o-', label='$\\partial W^*/\\partial$' + param_name,
                 color='#f39c12', linewidth=2, markersize=6)
        ax11.plot(param_vals, dCS, 's-', label='$\\partial CS^*/\\partial$' + param_name,
                 color='#2ecc71', linewidth=2, markersize=6)
        ax11.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.3)
        ax11.set_xlabel(param_name, fontweight='bold')
        ax11.set_ylabel('Derivative', fontweight='bold')
        ax11.set_title('Welfare Derivatives', fontweight='bold')
        ax11.legend()
        ax11.grid(True, alpha=0.3)

        # Convergence status
        ax12 = fig.add_subplot(gs[3, 2])
        converged_pct = df['converged'].sum() / len(df) * 100
        ax12.bar(['Converged', 'Failed'],
                [df['converged'].sum(), (~df['converged']).sum()],
                color=['#2ecc71', '#e74c3c'], alpha=0.7, edgecolor='black', linewidth=2)
        ax12.set_ylabel('Count', fontweight='bold')
        ax12.set_title(f'Convergence Status ({converged_pct:.1f}%)', fontweight='bold')
        ax12.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()

        if save:
            filename = OUTPUT_DIR / f'comparative_statics_{param_name}.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"  ✓ Saved: {filename}")
        else:
            plt.show()

        plt.close()

    def generate_latex_table(self, param_names: List[str]) -> str:
        """
        Tüm parametreler için özet LaTeX tablosu oluştur.

        Parameters
        ----------
        param_names : List[str]
            Analiz edilmiş parametre adları

        Returns
        -------
        str
            LaTeX tablo kodu
        """
        # Baseline değerlerini al
        baseline_dict = self.baseline.to_dict()

        # Her parametre için özet istatistikleri topla
        summary_data = []

        for param in param_names:
            if param not in self.results:
                continue

            df = self.results[param]

            # Baseline değeri bul (en yakın nokta)
            baseline_val = baseline_dict[param]
            idx = (np.abs(df[param] - baseline_val)).argmin()

            # Elastiklik hesapla (baseline civarında)
            if idx > 0 and idx < len(df) - 1:
                # Forward difference
                dI1_dtheta = (df['I1_star'].iloc[idx+1] - df['I1_star'].iloc[idx]) / \
                            (df[param].iloc[idx+1] - df[param].iloc[idx])
                dI2_dtheta = (df['I2_star'].iloc[idx+1] - df['I2_star'].iloc[idx]) / \
                            (df[param].iloc[idx+1] - df[param].iloc[idx])
                dW_dtheta = (df['W_star'].iloc[idx+1] - df['W_star'].iloc[idx]) / \
                           (df[param].iloc[idx+1] - df[param].iloc[idx])
            else:
                dI1_dtheta = dI2_dtheta = dW_dtheta = np.nan

            summary_data.append({
                'Parameter': f'${param}$',
                'Baseline': f'{baseline_val:.3f}',
                'Range': f'[{df[param].min():.1f}, {df[param].max():.1f}]',
                r'$\partial I_1^*/\partial\theta$': f'{dI1_dtheta:.4f}' if not np.isnan(dI1_dtheta) else 'N/A',
                r'$\partial I_2^*/\partial\theta$': f'{dI2_dtheta:.4f}' if not np.isnan(dI2_dtheta) else 'N/A',
                r'$\partial W^*/\partial\theta$': f'{dW_dtheta:.2f}' if not np.isnan(dW_dtheta) else 'N/A',
            })

        # DataFrame oluştur
        summary_df = pd.DataFrame(summary_data)

        # LaTeX'e dönüştür
        latex_str = summary_df.to_latex(
            index=False,
            escape=False,
            column_format='l|c|c|c|c|c',
            caption='Comparative Statics Summary: Derivatives at Baseline',
            label='tab:comparative_statics'
        )

        return latex_str


def main():
    """Ana çalıştırma fonksiyonu."""

    print("="*70)
    print("KARŞILAŞTIRMALI STATİKLER ANALİZ PAKETİ")
    print("="*70)

    # Baseline parametreler
    baseline = Parameters.baseline()

    # Analyzer oluştur
    analyzer = ComparativeStaticsAnalyzer(
        baseline_params=baseline,
        n_points=15,  # Her parametre için 15 nokta
        seed=42
    )

    # Analiz edilecek parametreler ve aralıkları
    param_specs = {
        'gamma': (20.0, 80.0, False),      # Takipçi maliyeti
        'alpha': (50.0, 150.0, False),     # Piyasa büyüklüğü
        'beta': (0.5, 3.0, False),         # Kendi-fiyat elastikiyeti
        'delta': (0.1, 0.8, False),        # Çapraz-fiyat elastikiyeti
        'kappa_1': (0.1, 2.0, False),      # Lider yatırım maliyeti
        'kappa_2': (0.5, 4.0, False),      # Takipçi yatırım maliyeti
        'mu_c': (20.0, 60.0, False),       # Lider maliyet ortalaması
        'sigma_c': (2.0, 20.0, False),     # Lider maliyet std sapması
    }

    # Her parametre için analiz
    for param_name, (min_val, max_val, log_scale) in param_specs.items():
        # Analiz yap
        df = analyzer.analyze_parameter(
            param_name=param_name,
            param_range=(min_val, max_val),
            log_scale=log_scale
        )

        # CSV kaydet
        csv_file = OUTPUT_DIR / f'results_{param_name}.csv'
        df.to_csv(csv_file, index=False)
        print(f"  ✓ Saved CSV: {csv_file}")

        # Grafik oluştur
        analyzer.plot_comparative_statics(param_name, save=True)

        # Elastiklik hesapla
        elasticity_df = analyzer.compute_elasticities(param_name)
        elasticity_file = OUTPUT_DIR / f'elasticities_{param_name}.csv'
        elasticity_df.to_csv(elasticity_file, index=False)
        print(f"  ✓ Saved elasticities: {elasticity_file}")

    # LaTeX tablo oluştur
    print("\n" + "="*70)
    print("GENERATING LATEX SUMMARY TABLE")
    print("="*70)

    latex_table = analyzer.generate_latex_table(list(param_specs.keys()))

    latex_file = LATEX_DIR / 'comparative_statics_summary.tex'
    with open(latex_file, 'w') as f:
        f.write(latex_table)

    print(f"\n✓ LaTeX table saved: {latex_file}")
    print("\nPreview:")
    print(latex_table)

    # Final özet
    print("\n" + "="*70)
    print("✅ KARŞILAŞTIRMALI STATİKLER ANALİZİ TAMAMLANDI!")
    print("="*70)
    print(f"\n📁 Grafikler: {OUTPUT_DIR.absolute()}")
    print(f"📄 LaTeX tablo: {latex_file.absolute()}")
    print(f"\n📊 Toplam {len(param_specs)} parametre analiz edildi")
    print(f"📈 Her biri için {analyzer.n_points} nokta hesaplandı")
    print(f"🎨 {len(param_specs)} detaylı grafik oluşturuldu")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
