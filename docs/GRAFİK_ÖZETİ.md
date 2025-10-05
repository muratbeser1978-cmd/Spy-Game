# 📊 Grafik Görselleştirme Özet Kılavuzu

**Son Güncelleme**: 2025-10-05

---

## 🚀 Hızlı Başlangıç

Projenizde **iki farklı görselleştirme sistemi** bulunmaktadır:

### 1️⃣ **Basit Grafikler** (Hızlı Kontrol İçin)
```bash
source venv/bin/activate
python quick_visualizations.py
```
- **Süre**: ~30-60 saniye
- **Çıktı**: `figures_quick/` klasöründe **5 grafik**
- **Kullanım**: Hızlı kontrol, kod doğrulama, ilk analiz

### 2️⃣ **Gelişmiş Grafikler** (Sunum/Makale İçin)
```bash
source venv/bin/activate
python advanced_visualizations_fast.py
```
- **Süre**: ~30 saniye
- **Çıktı**: `figures_advanced/` klasöründe **2 gelişmiş grafik**
- **Kullanım**: Sunum, konferans, akademik makale, teknik rapor

---

## 📁 Oluşturulan Grafikler

### Basit Grafikler (`figures_quick/`)

| Dosya | İçerik | Kullanım |
|-------|--------|----------|
| `1_nash_heatmap.png` | Nash dengesi haritası (I₁ vs I₂) | Optimal yatırımları göster |
| `2_welfare.png` | Refah bileşenleri (bar + pie) | Refah analizi |
| `3_espionage_params.png` | ρ ve κ haritaları | Casusluk parametreleri |
| `4_investment_analysis.png` | Yatırım analizi (4 panel) | ROI, maliyetler |
| `5_summary_dashboard.png` | Özet dashboard | Hızlı özet |

### Gelişmiş Grafikler (`figures_advanced/`)

| Dosya | İçerik | Kullanım |
|-------|--------|----------|
| `advanced_welfare.png` | Gelişmiş refah analizi (6 panel) | Makale, detaylı analiz |
| `advanced_dashboard.png` | Gelişmiş özet dashboard (7 panel) | Sunum, konferans |

---

## 🎨 Grafik Teknikleri Karşılaştırması

| Teknik | Basit | Gelişmiş |
|--------|-------|----------|
| **Bar Chart** | ✅ | ✅ |
| **Pie Chart** | ✅ | ❌ |
| **Heatmap** | ✅ | ❌ |
| **Waterfall Chart** | ❌ | ✅ |
| **Donut Chart** | ❌ | ✅ |
| **3D-Style Bars** | ❌ | ✅ |
| **Gauge Chart** | ❌ | ✅ |
| **Sankey Flow** | ❌ | ✅ |
| **Fancy ASCII Boxes** | ❌ | ✅ |

---

## 📖 Kullanım Senaryoları

### Senaryo 1: **İlk Kez Kod Çalıştırıyorum**
```bash
python quick_visualizations.py
```
**Neden?** Kodun çalıştığını ve sonuçların mantıklı olduğunu hızlıca kontrol et.

### Senaryo 2: **Parametreleri Değiştirdim, Sonuçları Görmek İstiyorum**
```bash
python quick_visualizations.py
```
**Neden?** Hızlı feedback, 30-60 saniyede tüm önemli grafikler hazır.

### Senaryo 3: **Konferansa Sunum Hazırlıyorum**
```bash
python advanced_visualizations_fast.py
```
**Kullan**: `advanced_dashboard.png` - Tek slide'da tüm önemli metrikler.

### Senaryo 4: **Akademik Makale Yazıyorum**
```bash
python advanced_visualizations_fast.py
```
**Kullan**:
- Figure 1: `advanced_welfare.png` (waterfall + donut + 3D bars)
- Figure 2: `1_nash_heatmap.png` (basit grafiklerden)
- Figure 3: `3_espionage_params.png` (basit grafiklerden)

### Senaryo 5: **Teknik Rapor Yazıyorum**
```bash
# Her ikisini de oluştur:
python quick_visualizations.py
python advanced_visualizations_fast.py
```
**Kullan**:
- **Bölüm 4.1 (Nash Dengesi)**: `1_nash_heatmap.png`, `4_investment_analysis.png`
- **Bölüm 4.2 (Refah Analizi)**: `advanced_welfare.png`
- **Bölüm 4.3 (Özet)**: `advanced_dashboard.png`
- **Appendix A (Tüm Grafikler)**: `figures_quick/` + `figures_advanced/`

---

## 🎯 Hangi Grafiği Ne Zaman Kullanmalı?

### **Nash Dengesi Göstermek İçin:**
- ✅ `1_nash_heatmap.png` - Isı haritası, Nash noktası işaretli

### **Refah Analizi İçin:**
- 🟢 **Basit**: `2_welfare.png` - Bar + pie chart
- 🔵 **Gelişmiş**: `advanced_welfare.png` - Waterfall + donut + 3D + ROI

### **Casusluk Parametreleri İçin:**
- ✅ `3_espionage_params.png` - ρ ve κ haritaları

### **Yatırım Getirisi (ROI) İçin:**
- ✅ `4_investment_analysis.png` - 4 panel (Nash, maliyetler, brüt/net, ROI)

### **Hızlı Özet İçin:**
- 🟢 **Basit**: `5_summary_dashboard.png` - Metin kutuları + bar chart
- 🔵 **Gelişmiş**: `advanced_dashboard.png` - Fancy boxes + gauge + Sankey + bar

---

## ⚙️ Teknik Detaylar

### Kalite Ayarları:
```python
# Her iki script de:
dpi=300  # Baskı kalitesi (academic journal standardı)
bbox_inches='tight'  # Kenarları kırp
```

### Font ve Stil:
```python
# Basit grafikler:
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 10

# Gelişmiş grafikler:
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 11
```

### Renk Paleti:
```python
# Refah bileşenleri (her iki script):
'#2ecc71'  # Yeşil - Tüketici Artığı (CS)
'#3498db'  # Mavi - Lider Karı (U₁)
'#e74c3c'  # Kırmızı - Takipçi Karı (U₂)
'#f39c12'  # Turuncu - Toplam Refah (W)
```

---

## 🔧 Özelleştirme

### Parametreleri Değiştir:
```python
# Her iki script'in başında:
params = Parameters.baseline()

# Kendi parametrelerin:
params = Parameters(
    alpha=100.0,
    beta=1.5,
    gamma=50.0,  # Farklı gamma değeri dene
    # ...
)
```

### DPI Artır (Ultra Yüksek Kalite):
```python
# Script içinde bul:
plt.savefig(..., dpi=300, ...)

# Değiştir:
plt.savefig(..., dpi=600, ...)  # Poster kalitesi
```

### Grafikler Açılmıyor?
```bash
# Mac:
open figures_quick/
open figures_advanced/

# Linux:
xdg-open figures_quick/
xdg-open figures_advanced/
```

---

## 📚 Detaylı Kılavuzlar

### Basit Grafikler Detayları:
👉 **`GRAFİK_KULLANIM_KILAVUZU.md`**
- Her grafiğin detaylı açıklaması
- Nasıl yorumlanır
- Kullanım örnekleri

### Gelişmiş Grafikler Detayları:
👉 **`GELİŞMİŞ_GRAFİKLER_KILAVUZU.md`**
- Waterfall, donut, gauge chart teknikleri
- Kod örnekleri
- Özelleştirme detayları

---

## ✅ Kontrol Listesi

İlk kez kullanıyorsanız:

- [ ] Python sanal ortamı aktif mi? (`source venv/bin/activate`)
- [ ] Seaborn kurulu mu? (`pip install seaborn`)
- [ ] Basit grafikleri oluştur (`python quick_visualizations.py`)
- [ ] Gelişmiş grafikleri oluştur (`python advanced_visualizations_fast.py`)
- [ ] `figures_quick/` klasöründe 5 dosya var mı?
- [ ] `figures_advanced/` klasöründe 2 dosya var mı?
- [ ] Grafikler açılıyor mu?

---

## 🎉 Sonuç

Artık **7 farklı grafik türü** ile toplamda **7 profesyonel grafik** oluşturabiliyorsunuz:

### Basit (5 grafik):
1. Nash haritası
2. Refah bileşenleri
3. Casusluk parametreleri
4. Yatırım analizi
5. Özet dashboard

### Gelişmiş (2 grafik):
1. Gelişmiş refah (6 panel)
2. Gelişmiş dashboard (7 panel)

**Toplam**: 13 panel / 7 dosya / 2 klasör

---

**İhtiyacınıza göre seçin:**
- 🟢 **Hızlı kontrol** → `quick_visualizations.py`
- 🔵 **Sunum/Makale** → `advanced_visualizations_fast.py`
- 🟣 **Tam rapor** → Her ikisi

---

**Son Güncelleme**: 2025-10-05
**Durum**: ✅ Kullanıma Hazır
