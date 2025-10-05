#!/usr/bin/env python3
"""Gelişmiş Profesyonel Görselleştirme - Welfare ve Dashboard (Hızlı Versiyon).

Teknik, detaylı ve akademik standartlarda grafikler - Optimize edilmiş.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Circle
import seaborn as sns
from pathlib import Path

from src.models.parameters import Parameters
from src.solvers.nash_solver import solve_nash_equilibrium

# Profesyonel stil
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['font.size'] = 11
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['grid.alpha'] = 0.3

OUTPUT_DIR = Path("figures_advanced")
OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("GELİŞMİŞ PROFESYONEL GÖRSELLEŞTİRME (HIZLI VERSİYON)")
print("=" * 80)

# Nash dengesini hesapla
params = Parameters.baseline()
solution = solve_nash_equilibrium(params, seed=42)
I1_nash, I2_nash = solution.investments
rho_nash, kappa_nash = solution.contest_prob, solution.signal_precision
V1, V2 = solution.value_functions
U1, U2 = solution.utilities
CS, W = solution.consumer_surplus, solution.total_welfare

print(f"\n✓ Nash Dengesi: I₁={I1_nash:.4f}, I₂={I2_nash:.4f}")

# Yatırım maliyetleri
cost1 = 0.5 * params.kappa_1 * I1_nash**2
cost2 = 0.5 * params.kappa_2 * I2_nash**2

# ==================================================================
# GELİŞMİŞ REFAH GRAFİĞİ
# ==================================================================
print("\n📊 [1/2] Gelişmiş Refah Analizi oluşturuluyor...")

fig1 = plt.figure(figsize=(18, 12))
gs1 = gridspec.GridSpec(2, 3, figure=fig1, hspace=0.3, wspace=0.3)
fig1.suptitle('REFAH ANALİZİ: Detaylı Ayrıştırma ve Görselleştirme',
             fontsize=16, fontweight='bold', y=0.98)

# ---- [0,0]: Waterfall Chart ----
ax1 = fig1.add_subplot(gs1[0, 0])
categories = ['Başlangıç', 'CS', 'U₁', 'U₂', 'Toplam']
values = [0, CS, U1, U2, 0]
cumsum = np.cumsum([0, CS, U1, U2])
colors = ['white', '#2ecc71', '#3498db', '#e74c3c', '#f39c12']

for i, (cat, val) in enumerate(zip(categories[:-1], values[:-1])):
    if i == 0:
        continue
    ax1.bar(i, val, bottom=cumsum[i-1], color=colors[i],
            edgecolor='black', linewidth=2, alpha=0.85)
    ax1.text(i, cumsum[i-1] + val/2, f'{val:.0f}',
            ha='center', va='center', fontsize=10, fontweight='bold', color='white')

# Toplam bar
ax1.bar(4, W, color=colors[4], edgecolor='black', linewidth=2.5, alpha=0.9)
ax1.text(4, W/2, f'{W:.0f}', ha='center', va='center',
        fontsize=11, fontweight='bold', color='white')

# Bağlantı çizgileri
for i in range(len(cumsum)-1):
    ax1.plot([i+0.4, i+1-0.4], [cumsum[i+1], cumsum[i+1]],
            'k--', linewidth=1.5, alpha=0.5)

ax1.set_xticks(range(5))
ax1.set_xticklabels(categories, fontsize=9, fontweight='bold')
ax1.set_ylabel('Refah Değeri', fontsize=11, fontweight='bold')
ax1.set_title('Refah Bileşenleri: Waterfall', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3, axis='y')
ax1.set_ylim([0, W * 1.15])

# ---- [0,1]: Donut Chart ----
ax2 = fig1.add_subplot(gs1[0, 1])
sizes = [CS, U1, U2]
labels = ['Tüketici Artığı\n(CS)', 'Lider Net Karı\n(U₁)', 'Takipçi Net Karı\n(U₂)']
colors_donut = ['#2ecc71', '#3498db', '#e74c3c']
explode = (0.08, 0.04, 0.04)

wedges, texts, autotexts = ax2.pie(sizes, labels=labels, autopct='%1.1f%%',
                                    explode=explode, colors=colors_donut,
                                    shadow=True, startangle=90,
                                    wedgeprops={'edgecolor': 'white', 'linewidth': 3},
                                    textprops={'fontsize': 9, 'fontweight': 'bold'})

# Donut efekti
centre_circle = Circle((0, 0), 0.70, fc='white', linewidth=2, edgecolor='black')
ax2.add_artist(centre_circle)

# Merkez metin
ax2.text(0, 0, f'Toplam\nRefah\n\n{W:.0f}',
        ha='center', va='center', fontsize=13, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow',
                 edgecolor='black', linewidth=2))

ax2.set_title('Refah Dağılımı: Oransal Katkılar', fontsize=12, fontweight='bold')

# ---- [0,2]: 3D-style Bars ----
ax3 = fig1.add_subplot(gs1[0, 2])
components_3d = ['CS', 'U₁', 'U₂', 'Toplam\nMaliyet', 'Net\nRefah']
total_cost = cost1 + cost2
values_3d = [CS, U1, U2, -total_cost, W - total_cost]
colors_3d = ['#2ecc71', '#3498db', '#e74c3c', '#95a5a6', '#f39c12']

x_pos = np.arange(len(components_3d))

for i, (val, col) in enumerate(zip(values_3d, colors_3d)):
    # Ana bar
    bar = ax3.bar(i, abs(val), color=col, edgecolor='black',
                 linewidth=1.5, alpha=0.85, width=0.6)

    # 3D gölge efekti
    offset = 0.05
    ax3.bar(i + offset, abs(val) * 0.97, color=col, alpha=0.3,
           width=0.6, zorder=0)

    # Değer etiketi
    y_pos = abs(val) + 30 if val > 0 else -30
    ax3.text(i, y_pos, f'{val:.1f}', ha='center', va='bottom' if val > 0 else 'top',
            fontsize=9, fontweight='bold')

ax3.axhline(y=0, color='black', linewidth=2, linestyle='-')
ax3.set_xticks(x_pos)
ax3.set_xticklabels(components_3d, fontsize=8, fontweight='bold')
ax3.set_ylabel('Değer', fontsize=11, fontweight='bold')
ax3.set_title('Maliyet Düşülmüş Refah', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')

# ---- [1,0]: Yatırım Analizi ----
ax4 = fig1.add_subplot(gs1[1, 0])
inv_labels = ['Lider\nI₁', 'Takipçi\nI₂']
inv_values = [I1_nash, I2_nash]
inv_colors = ['#3498db', '#e74c3c']

bars = ax4.bar(inv_labels, inv_values, color=inv_colors, alpha=0.8,
               edgecolor='black', linewidth=2)
for bar, val in zip(bars, inv_values):
    ax4.text(bar.get_x() + bar.get_width()/2., val, f'{val:.3f}',
            ha='center', va='bottom', fontweight='bold', fontsize=10)

ax4.set_ylabel('Yatırım Seviyesi', fontsize=11, fontweight='bold')
ax4.set_title('Nash Yatırımları', fontsize=12, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')

# ---- [1,1]: Yatırım Maliyetleri ----
ax5 = fig1.add_subplot(gs1[1, 1])
cost_labels = ['Lider\nMaliyet', 'Takipçi\nMaliyet']
cost_values = [cost1, cost2]

bars = ax5.bar(cost_labels, cost_values, color=inv_colors, alpha=0.8,
               edgecolor='black', linewidth=2)
for bar, val in zip(bars, cost_values):
    ax5.text(bar.get_x() + bar.get_width()/2., val, f'{val:.2f}',
            ha='center', va='bottom', fontweight='bold', fontsize=10)

ax5.set_ylabel('Maliyet', fontsize=11, fontweight='bold')
ax5.set_title('Yatırım Maliyetleri', fontsize=12, fontweight='bold')
ax5.grid(True, alpha=0.3, axis='y')

# ---- [1,2]: ROI ----
ax6 = fig1.add_subplot(gs1[1, 2])
roi_values = [V1/cost1 if cost1 > 0 else 0, V2/cost2 if cost2 > 0 else 0]
roi_labels = ['Lider\nROI', 'Takipçi\nROI']

bars = ax6.bar(roi_labels, roi_values, color=inv_colors, alpha=0.8,
               edgecolor='black', linewidth=2)
for bar, val in zip(bars, roi_values):
    ax6.text(bar.get_x() + bar.get_width()/2., val, f'{val:.1f}x',
            ha='center', va='bottom', fontweight='bold', fontsize=10)

ax6.axhline(y=1, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Başabaş')
ax6.set_ylabel('Kar/Maliyet Oranı', fontsize=11, fontweight='bold')
ax6.set_title('Yatırım Getirisi (ROI)', fontsize=12, fontweight='bold')
ax6.legend(fontsize=9)
ax6.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'advanced_welfare.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Kaydedildi: advanced_welfare.png")

# ==================================================================
# GELİŞMİŞ DASHBOARD
# ==================================================================
print("\n📊 [2/2] Gelişmiş Dashboard oluşturuluyor...")

fig2 = plt.figure(figsize=(18, 14))
gs2 = gridspec.GridSpec(3, 4, figure=fig2, hspace=0.35, wspace=0.35)
fig2.suptitle('NASH DENGESİ: Gelişmiş Özet Dashboard',
             fontsize=16, fontweight='bold', y=0.98)

# ---- [0, 0:2]: Anahtar Metrikler (Fancy Boxes) ----
ax1 = fig2.add_subplot(gs2[0, 0:2])
ax1.axis('off')

metrics_text = f"""
╔═══════════════════════════════════════╗
║         YATIRIM METRİKLERİ           ║
╠═══════════════════════════════════════╣
║ Lider Yatırımı:      I₁* = {I1_nash:7.4f} ║
║ Takipçi Yatırımı:    I₂* = {I2_nash:7.4f} ║
║                                       ║
║ Lider Maliyeti:          = {cost1:7.3f} ║
║ Takipçi Maliyeti:        = {cost2:7.3f} ║
╚═══════════════════════════════════════╝
"""

ax1.text(0.05, 0.5, metrics_text, fontsize=10, verticalalignment='center',
         fontfamily='monospace',
         bbox=dict(boxstyle='round,pad=1', facecolor='lightblue',
                  edgecolor='navy', linewidth=2, alpha=0.8))

# ---- [0, 2:]: Casusluk Metrikleri ----
ax2 = fig2.add_subplot(gs2[0, 2:])
ax2.axis('off')

espionage_text = f"""
╔═══════════════════════════════════════╗
║       CASUSLUK PARAMETRELERİ         ║
╠═══════════════════════════════════════╣
║ Başarı Olasılığı:  ρ* = {rho_nash:7.4f} ║
║ Sinyal Güvenilirliği: κ* = {kappa_nash:7.4f} ║
║                                       ║
║ Yakınsama:          {'✓ Başarılı' if solution.converged else '✗ Başarısız':>12} ║
║ İterasyon:              {solution.iterations:>3} kez ║
╚═══════════════════════════════════════╝
"""

ax2.text(0.05, 0.5, espionage_text, fontsize=10, verticalalignment='center',
         fontfamily='monospace',
         bbox=dict(boxstyle='round,pad=1', facecolor='lightyellow',
                  edgecolor='orange', linewidth=2, alpha=0.8))

# ---- [1, :2]: Kar Akışı (Sankey-style) ----
ax3 = fig2.add_subplot(gs2[1, :2])
ax3.axis('off')
ax3.set_xlim([0, 10])
ax3.set_ylim([0, 10])

# Lider akışı
ax3.barh([7.5], [V1], left=[0], height=1.5, color='#3498db', alpha=0.6,
         edgecolor='black', linewidth=2, label='Brüt Kar')
ax3.barh([7.5], [U1], left=[0], height=1.5, color='#3498db', alpha=0.9,
         edgecolor='black', linewidth=2, label='Net Kar')
ax3.text(V1/2, 7.5, f'V₁={V1:.1f}', ha='center', va='center',
         fontsize=10, fontweight='bold', color='white')
ax3.text(U1/2, 7.5, f'U₁={U1:.1f}', ha='center', va='center',
         fontsize=9, fontweight='bold')
ax3.text(V1 + 0.3, 7.5, f'-{cost1:.1f}', ha='left', va='center',
         fontsize=8, color='red', fontweight='bold')

# Takipçi akışı
ax3.barh([5], [V2], left=[0], height=1.5, color='#e74c3c', alpha=0.6,
         edgecolor='black', linewidth=2)
ax3.barh([5], [U2], left=[0], height=1.5, color='#e74c3c', alpha=0.9,
         edgecolor='black', linewidth=2)
ax3.text(V2/2, 5, f'V₂={V2:.1f}', ha='center', va='center',
         fontsize=10, fontweight='bold', color='white')
ax3.text(U2/2, 5, f'U₂={U2:.1f}', ha='center', va='center',
         fontsize=9, fontweight='bold')
ax3.text(V2 + 0.3, 5, f'-{cost2:.1f}', ha='left', va='center',
         fontsize=8, color='red', fontweight='bold')

ax3.text(0, 9.5, 'BRÜT → NET KAR AKIŞI', fontsize=11, fontweight='bold')
ax3.text(0, 8.8, 'Lider:', fontsize=9, fontweight='bold', color='#3498db')
ax3.text(0, 6.3, 'Takipçi:', fontsize=9, fontweight='bold', color='#e74c3c')

# ---- [1, 2:]: Gauge Charts için ρ ve κ ----
ax4 = fig2.add_subplot(gs2[1, 2], projection='polar')
ax5 = fig2.add_subplot(gs2[1, 3], projection='polar')

def create_gauge(ax, value, title, color):
    """Gauge chart (speedometer-style)."""
    theta = np.linspace(0, np.pi, 100)
    ax.plot(theta, np.ones_like(theta), 'lightgray', linewidth=15, alpha=0.3)

    value_theta = np.linspace(0, np.pi * value, 100)
    ax.plot(value_theta, np.ones_like(value_theta), color, linewidth=15, alpha=0.9)

    # Needle
    needle_angle = np.pi * value
    ax.plot([needle_angle, needle_angle], [0, 1.1], 'black', linewidth=3)
    ax.plot(needle_angle, 1.1, 'o', color='black', markersize=10)

    # Labels
    ax.set_ylim([0, 1.3])
    ax.set_xticks([0, np.pi/2, np.pi])
    ax.set_xticklabels(['0', '0.5', '1.0'], fontsize=8)
    ax.set_yticks([])
    ax.set_title(f'{title}\n{value:.3f}', fontsize=11, fontweight='bold', pad=20)
    ax.grid(False)

create_gauge(ax4, rho_nash, 'ρ (Başarı)', '#3498db')
create_gauge(ax5, kappa_nash, 'κ (Güvenilirlik)', '#e74c3c')

# ---- [2, :]: Refah Bar Chart (Tüm Bileşenler) ----
ax6 = fig2.add_subplot(gs2[2, :])

welfare_components = ['Tüketici\nArtığı', 'Lider\nNet Karı', 'Takipçi\nNet Karı',
                      'TOPLAM\nREFAH']
welfare_values = [CS, U1, U2, W]
welfare_colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']

bars = ax6.bar(welfare_components, welfare_values, color=welfare_colors,
               alpha=0.8, edgecolor='black', linewidth=2)

for bar, val in zip(bars, welfare_values):
    ax6.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
            f'{val:.0f}', ha='center', va='bottom',
            fontsize=11, fontweight='bold')

ax6.set_ylabel('Değer', fontsize=12, fontweight='bold')
ax6.set_title('Refah Bileşenleri: Detaylı Görünüm', fontsize=13, fontweight='bold')
ax6.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'advanced_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Kaydedildi: advanced_dashboard.png")

# ==================================================================
print("\n" + "=" * 80)
print("✅ TÜM GELİŞMİŞ GRAFİKLER OLUŞTURULDU!")
print(f"📁 Konum: {OUTPUT_DIR.absolute()}")
print("=" * 80)
print("\nOluşturulan Dosyalar:")
for f in sorted(OUTPUT_DIR.glob("*.png")):
    print(f"  • {f.name}")
print("\n")
