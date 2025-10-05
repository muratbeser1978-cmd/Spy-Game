#!/usr/bin/env python3
"""Hızlı Görselleştirme - En önemli 5 grafik."""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from src.models.parameters import Parameters
from src.solvers.nash_solver import solve_nash_equilibrium
from src.topology.level_10_value_functions import compute_V_1, compute_V_2
from src.topology.level_11_utilities import compute_U_1, compute_U_2
from src.topology.level_02_contest import compute_rho
from src.topology.level_03_signal import compute_kappa

sns.set_style("whitegrid")
plt.rcParams['font.size'] = 10
OUTPUT_DIR = Path("figures_quick")
OUTPUT_DIR.mkdir(exist_ok=True)

print("🎨 Hızlı Görselleştirme Başlıyor...\n")

# Nash dengesini bul
params = Parameters.baseline()
solution = solve_nash_equilibrium(params, seed=42)
I1_nash, I2_nash = solution.investments

print(f"✓ Nash Dengesi: I₁={I1_nash:.3f}, I₂={I2_nash:.3f}\n")

# 1. Nash Dengesi Haritası
print("[1/5] Nash Dengesi Haritası...")
rng = np.random.default_rng(42)
I1_range = np.linspace(0, 2, 20)
I2_range = np.linspace(0, 2, 20)
I1_grid, I2_grid = np.meshgrid(I1_range, I2_range)
U_joint = np.zeros_like(I1_grid)

for i in range(len(I1_range)):
    for j in range(len(I2_range)):
        rng_local = np.random.default_rng(42)
        V1 = compute_V_1(I1_grid[j, i], I2_grid[j, i], params, rng_local)
        V2 = compute_V_2(I1_grid[j, i], I2_grid[j, i], params, rng_local)
        U1 = compute_U_1(V1, I1_grid[j, i], params.kappa_1)
        U2 = compute_U_2(V2, I2_grid[j, i], params.kappa_2)
        U_joint[j, i] = U1 + U2

fig, ax = plt.subplots(figsize=(10, 8))
contour = ax.contourf(I1_grid, I2_grid, U_joint, levels=20, cmap='RdYlGn')
ax.plot(I1_nash, I2_nash, 'r*', markersize=20, markeredgecolor='white', markeredgewidth=2)
plt.colorbar(contour, ax=ax, label='Toplam Fayda')
ax.set_xlabel('Lider Yatırımı $I_1$', fontweight='bold')
ax.set_ylabel('Takipçi Yatırımı $I_2$', fontweight='bold')
ax.set_title('Nash Dengesi: Toplam Fayda Haritası', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / '1_nash_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Kaydedildi\n")

# 2. Refah Bileşenleri
print("[2/5] Refah Bileşenleri...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Bar chart
components = ['Tüketici\nArtığı', 'Lider\nKarı', 'Takipçi\nKarı']
values = [solution.consumer_surplus, solution.utilities[0], solution.utilities[1]]
colors = ['#2ca02c', '#1f77b4', '#ff7f0e']
bars = ax1.bar(components, values, color=colors, alpha=0.8, edgecolor='black')
for bar, val in zip(bars, values):
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
            f'{val:.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax1.axhline(y=solution.total_welfare, color='red', linestyle='--', linewidth=2,
            label=f'Toplam: {solution.total_welfare:.0f}')
ax1.set_ylabel('Değer', fontweight='bold')
ax1.set_title('Refah Bileşenleri', fontsize=13, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

# Pie chart
ax2.pie(values, labels=components, autopct='%1.1f%%', colors=colors, shadow=True, startangle=90)
ax2.set_title('Refah Dağılımı', fontsize=13, fontweight='bold')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '2_welfare.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Kaydedildi\n")

# 3. Casusluk Parametreleri
print("[3/5] Casusluk Parametreleri...")
I1_range = np.linspace(0, 3, 25)
I2_range = np.linspace(0, 3, 25)
I1_grid, I2_grid = np.meshgrid(I1_range, I2_range)
rho_grid = np.zeros_like(I1_grid)
kappa_grid = np.zeros_like(I1_grid)

for i in range(len(I1_range)):
    for j in range(len(I2_range)):
        rho_grid[j, i] = compute_rho(I1_grid[j, i], I2_grid[j, i], params)
        kappa_grid[j, i] = compute_kappa(I2_grid[j, i], params)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Rho
contour1 = ax1.contourf(I1_grid, I2_grid, rho_grid, levels=20, cmap='Blues')
plt.colorbar(contour1, ax=ax1, label='$\\rho$')
ax1.plot(I1_nash, I2_nash, 'r*', markersize=15, markeredgecolor='white')
ax1.set_xlabel('$I_1$ (Savunma)', fontweight='bold')
ax1.set_ylabel('$I_2$ (Saldırı)', fontweight='bold')
ax1.set_title('Casusluk Başarı Olasılığı $\\rho$', fontsize=13, fontweight='bold')
ax1.grid(True, alpha=0.2)

# Kappa
contour2 = ax2.contourf(I1_grid, I2_grid, kappa_grid, levels=20, cmap='Oranges')
plt.colorbar(contour2, ax=ax2, label='$\\kappa$')
ax2.plot(I1_nash, I2_nash, 'r*', markersize=15, markeredgecolor='white')
ax2.set_xlabel('$I_1$ (Savunma)', fontweight='bold')
ax2.set_ylabel('$I_2$ (Saldırı)', fontweight='bold')
ax2.set_title('Sinyal Güvenilirliği $\\kappa$', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '3_espionage_params.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Kaydedildi\n")

# 4. Yatırımlar ve Maliyetler
print("[4/5] Yatırım Analizi...")
I1_cost = 0.5 * params.kappa_1 * I1_nash**2
I2_cost = 0.5 * params.kappa_2 * I2_nash**2

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Yatırımlar
ax = axes[0, 0]
bars = ax.bar(['Lider\n$I_1^*$', 'Takipçi\n$I_2^*$'], [I1_nash, I2_nash],
              color=['#1f77b4', '#ff7f0e'], alpha=0.8, edgecolor='black')
for bar, val in zip(bars, [I1_nash, I2_nash]):
    ax.text(bar.get_x() + bar.get_width()/2., val, f'{val:.3f}',
            ha='center', va='bottom', fontweight='bold')
ax.set_ylabel('Yatırım', fontweight='bold')
ax.set_title('Nash Yatırımları', fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')

# Maliyetler
ax = axes[0, 1]
bars = ax.bar(['Lider', 'Takipçi'], [I1_cost, I2_cost],
              color=['#1f77b4', '#ff7f0e'], alpha=0.8, edgecolor='black')
for bar, val in zip(bars, [I1_cost, I2_cost]):
    ax.text(bar.get_x() + bar.get_width()/2., val, f'{val:.2f}',
            ha='center', va='bottom', fontweight='bold')
ax.set_ylabel('Maliyet', fontweight='bold')
ax.set_title('Yatırım Maliyetleri', fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')

# Brüt vs Net
ax = axes[1, 0]
x = np.arange(2)
width = 0.35
ax.bar(x - width/2, solution.value_functions, width, label='Brüt (V)', alpha=0.6,
       color=['#1f77b4', '#ff7f0e'])
ax.bar(x + width/2, solution.utilities, width, label='Net (U)', alpha=0.9,
       color=['#1f77b4', '#ff7f0e'], edgecolor='black')
ax.set_ylabel('Kar', fontweight='bold')
ax.set_title('Brüt vs Net Kar', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(['Lider', 'Takipçi'])
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

# ROI
ax = axes[1, 1]
roi = [solution.value_functions[0]/I1_cost if I1_cost > 0 else 0,
       solution.value_functions[1]/I2_cost if I2_cost > 0 else 0]
bars = ax.bar(['Lider', 'Takipçi'], roi, color=['#1f77b4', '#ff7f0e'],
              alpha=0.8, edgecolor='black')
for bar, val in zip(bars, roi):
    ax.text(bar.get_x() + bar.get_width()/2., val, f'{val:.1f}x',
            ha='center', va='bottom', fontweight='bold')
ax.axhline(y=1, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Başabaş')
ax.set_ylabel('Kar/Maliyet Oranı', fontweight='bold')
ax.set_title('Yatırım Getirisi (ROI)', fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '4_investment_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Kaydedildi\n")

# 5. Özet Dashboard
print("[5/5] Özet Dashboard...")
fig = plt.figure(figsize=(14, 10))
gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
fig.suptitle('NASH DENGESİ: ÖZET', fontsize=16, fontweight='bold', y=0.98)

# Anahtar Metrikler
ax1 = fig.add_subplot(gs[0, 0])
ax1.axis('off')
text1 = f"""
YATIRIMLAR:
  Lider:    I₁* = {I1_nash:.4f}
  Takipçi:  I₂* = {I2_nash:.4f}

CASUSLUK:
  Başarı:   ρ* = {solution.contest_prob:.4f}
  Sinyal:   κ* = {solution.signal_precision:.4f}

YAKINSAMA:
  Durum:    {'✓ Başarılı' if solution.converged else '✗ Başarısız'}
  İterasyon: {solution.iterations}
"""
ax1.text(0.1, 0.5, text1, fontsize=11, verticalalignment='center',
         fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Karlar
ax2 = fig.add_subplot(gs[0, 1])
ax2.axis('off')
text2 = f"""
KARLAR:

Lider:
  Brüt:  V₁* = {solution.value_functions[0]:.1f}
  Net:   U₁* = {solution.utilities[0]:.1f}

Takipçi:
  Brüt:  V₂* = {solution.value_functions[1]:.1f}
  Net:   U₂* = {solution.utilities[1]:.1f}
"""
ax2.text(0.1, 0.5, text2, fontsize=11, verticalalignment='center',
         fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

# Refah Bar Chart
ax3 = fig.add_subplot(gs[1, :])
components = ['Tüketici\nArtığı', 'Lider\nKarı', 'Takipçi\nKarı', 'TOPLAM\nREFAH']
values = [solution.consumer_surplus, solution.utilities[0],
          solution.utilities[1], solution.total_welfare]
colors = ['#2ca02c', '#1f77b4', '#ff7f0e', '#d62728']
bars = ax3.bar(components, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
for bar, val in zip(bars, values):
    ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
            f'{val:.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
ax3.set_ylabel('Değer', fontsize=12, fontweight='bold')
ax3.set_title('Refah Bileşenleri', fontsize=13, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')

plt.savefig(OUTPUT_DIR / '5_summary_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Kaydedildi\n")

print("=" * 60)
print("✅ TÜM GRAFİKLER OLUŞTURULDU!")
print(f"📁 Konum: {OUTPUT_DIR.absolute()}")
print("=" * 60)
print("\nOluşturulan Dosyalar:")
for f in sorted(OUTPUT_DIR.glob("*.png")):
    print(f"  • {f.name}")
