# 🎉 Yeni Özellikler Kılavuzu

**Tarih**: 2025-10-05
**Durum**: ✅ TAMAMLANDI

---

## 📊 1. Karşılaştırmalı Statikler Analiz Paketi

### Özet
Tüm model parametrelerinin Nash dengesi üzerindeki etkilerini sistematik olarak analiz eder.

### Çalıştırma

```bash
source venv/bin/activate
python comparative_statics_suite.py
```

**Süre**: ~10-15 dakika (8 parametre × 15 nokta = 120 Nash dengesi çözümü)

### Çıktılar

#### 📁 Klasör: `figures_comparative_statics/`

Her parametre için **1 kapsamlı grafik** (12 panel):

1. **Nash Yatırımları** - I₁* ve I₂* değişimi
2. **Casusluk Parametreleri** - ρ* ve κ* (dual axis)
3. **Yatırım Oranı** - I₁*/I₂*
4. **Brüt Karlar** - V₁* ve V₂*
5. **Net Fayda** - U₁* ve U₂*
6. **Kar Farkı** - V₁* - V₂* (Lider avantajı)
7. **Tüketici Artığı** - CS*
8. **Toplam Refah** - W*
9. **Refah Dağılımı** - CS%, U₁%, U₂% (yığılı)
10. **Yatırım Türevleri** - ∂I*/∂θ
11. **Refah Türevleri** - ∂W*/∂θ, ∂CS*/∂θ
12. **Yakınsama Durumu** - Başarı oranı

**Oluşturulan Dosyalar** (her parametre için):
- `comparative_statics_{param}.png` - 12 panelli grafik
- `results_{param}.csv` - Ham sonuçlar (15 satır × 11 sütun)
- `elasticities_{param}.csv` - Elastikiteler

#### 📄 Klasör: `tables/`

**`comparative_statics_summary.tex`** - LaTeX tablosu:
- Her parametrenin baseline değeri
- Analiz aralığı
- Türevler (∂I₁*/∂θ, ∂I₂*/∂θ, ∂W*/∂θ)

### Analiz Edilen Parametreler

| Parametre | İsim | Aralık | Anlamı |
|-----------|------|---------|--------|
| `gamma` | γ | [20, 80] | Takipçi maliyeti |
| `alpha` | α | [50, 150] | Piyasa büyüklüğü |
| `beta` | β | [0.5, 3.0] | Kendi-fiyat elastikiyeti |
| `delta` | δ | [0.1, 0.8] | Çapraz-fiyat elastikiyeti |
| `kappa_1` | κ₁ | [0.1, 2.0] | Lider yatırım maliyeti |
| `kappa_2` | κ₂ | [0.5, 4.0] | Takipçi yatırım maliyeti |
| `mu_c` | μ_c | [20, 60] | Lider maliyet ortalaması |
| `sigma_c` | σ_c | [2, 20] | Lider maliyet belirsizliği |

### Örnek Kullanım

```bash
# Tüm parametreler için analiz
python comparative_statics_suite.py

# Sonuçları incele
cd figures_comparative_statics/
open comparative_statics_gamma.png
open comparative_statics_alpha.png

# CSV verilerini yükle (Python)
import pandas as pd
df = pd.read_csv('figures_comparative_statics/results_gamma.csv')
print(df.head())
```

### Bulgular Ne Anlama Geliyor?

#### Pozitif Türev (∂X*/∂θ > 0)
- Parametre arttıkça X* da artar
- **Örnek**: ∂I₁*/∂α > 0 → Piyasa büyüdükçe Lider daha fazla yatırım yapar

#### Negatif Türev (∂X*/∂θ < 0)
- Parametre arttıkça X* azalır
- **Örnek**: ∂ρ*/∂I₁ < 0 → Lider savunması arttıkça casusluk başarısı azalır

#### Elastikite (ε)
- **ε > 1**: Yüksek elastik (parametreye çok duyarlı)
- **ε < 1**: Düşük elastik (parametreye az duyarlı)
- **ε ≈ 0**: Neredeyse bağımsız

---

## 📄 2. Otomatik LaTeX/PDF Rapor Oluşturucu

### Özet
Nash dengesi analizini profesyonel LaTeX/PDF raporuna dönüştürür.

### Çalıştırma

```bash
source venv/bin/activate
python generate_simple_report.py
```

**Süre**: ~30 saniye (Nash + LaTeX oluşturma)

### Çıktılar

#### 📁 Klasör: `reports/`

**`nash_equilibrium_report.tex`** - Tam LaTeX raporu:
- Model açıklaması
- Parametre tablosu
- Nash dengesi sonuçları
- Ekonomik yorumlama
- Tüm grafikler (otomatik eklenir)
- Ek bölümler (hesaplama detayları, kod)

**`nash_equilibrium_report.pdf`** - PDF versiyonu (eğer pdflatex kuruluysa)

### Rapor İçeriği

#### Bölüm 1: Model Overview
- Oyun yapısı (4 aşama)
- Contest success function
- Signal precision
- Investment costs

#### Bölüm 2: Parameter Values
- Tablo: Tüm baseline parametreler
- Açıklamalar

#### Bölüm 3: Nash Equilibrium Results
- **Tablo**: Tüm denge değerleri
  - Yatırımlar (I₁*, I₂*, oran)
  - Casusluk (ρ*, κ*)
  - Karlar (V₁*, V₂*, fark)
  - Fayda (U₁*, U₂*)
  - Refah (CS*, W*, pay)
- **Yorumlama**:
  - Yatırım asimetrisi
  - Casusluk etkinliği
  - Sinyal kalitesi
  - Kar dağılımı
  - Tüketici refahı

#### Bölüm 4: Visualizations
Otomatik eklenen grafikler:
- Nash heatmap (`figures_quick/1_nash_heatmap.png`)
- Welfare analysis (`figures_advanced/advanced_welfare.png`)
- Dashboard (`figures_advanced/advanced_dashboard.png`)
- Espionage params (`figures_quick/3_espionage_params.png`)

#### Bölüm 5: Conclusion
- Ana bulgular özeti
- Politika çıkarımları
- Gelecek araştırma önerileri

#### Appendix
- Hesaplama yöntemleri
- Differential Evolution algoritması
- Monte Carlo detayları
- Kod erişim bilgisi

### PDF Oluşturma

#### MacOS/Linux (TeX Live):
```bash
# LaTeX kurulu değilse
brew install --cask mactex  # MacOS
sudo apt install texlive-full  # Ubuntu/Debian

# PDF oluştur
cd reports/
pdflatex nash_equilibrium_report.tex
pdflatex nash_equilibrium_report.tex  # 2. kez (references için)

# Aç
open nash_equilibrium_report.pdf
```

#### Windows (MikTeX):
```cmd
REM MikTeX indir: https://miktex.org/download
cd reports
pdflatex nash_equilibrium_report.tex
pdflatex nash_equilibrium_report.tex
start nash_equilibrium_report.pdf
```

### Özelleştirme

```python
# generate_simple_report.py içinde değiştir:

# Başlık
latex_content = r"""\title{\textbf{Kendi Başlığınız}}
\author{Adınız}
\date{Tarih}
"""

# Yeni bölüm ekle
latex_content += r"""
\section{Yeni Bölüm}
Buraya içerik...
"""

# Farklı grafikler ekle
latex_content += r"""
\begin{figure}[H]
    \includegraphics[width=\textwidth]{../figures_comparative_statics/comparative_statics_gamma.png}
    \caption{Gamma Sensitivity}
\end{figure}
"""
```

---

## 🎯 Kullanım Senaryoları

### Senaryo 1: **Akademik Makale Hazırlama**

```bash
# 1. Grafikler oluştur
python quick_visualizations.py
python advanced_visualizations_fast.py

# 2. Karşılaştırmalı statikler
python comparative_statics_suite.py  # ~15 dakika

# 3. LaTeX rapor
python generate_simple_report.py

# 4. PDF derle
cd reports/
pdflatex nash_equilibrium_report.tex
pdflatex nash_equilibrium_report.tex
```

**Kullan**:
- **Main text**: Rapordaki tablolar ve grafikler
- **Appendix**: Karşılaştırmalı statikler grafikleri
- **Supplementary**: CSV dosyaları

### Senaryo 2: **Parametre Sensitivitesi Analizi**

```bash
# Sadece karşılaştırmalı statikler
python comparative_statics_suite.py

# İncele
cd figures_comparative_statics/
open comparative_statics_gamma.png
open comparative_statics_kappa_2.png

# CSV analiz
import pandas as pd
df_gamma = pd.read_csv('results_gamma.csv')
df_kappa2 = pd.read_csv('results_kappa_2.csv')

# Elastikitleri karşılaştır
elast_gamma = pd.read_csv('elasticities_gamma.csv')
print(elast_gamma['epsilon_W_star'].mean())
```

### Senaryo 3: **Hızlı Rapor (Sunum İçin)**

```bash
# Sadece rapor oluştur (grafikleri kullanır)
python generate_simple_report.py

# PDF aç
open reports/nash_equilibrium_report.pdf
```

---

## 📊 Çıktı Özeti

### Toplam Oluşturulan Dosyalar

| Klasör | Dosya Sayısı | İçerik |
|--------|--------------|--------|
| `figures_comparative_statics/` | 24 dosya | 8 grafik + 8 CSV + 8 elastiklik CSV |
| `tables/` | 1 dosya | LaTeX tablo |
| `reports/` | 1-2 dosya | .tex + .pdf (opsiyonel) |
| **TOPLAM** | **26-27 dosya** | |

### Dosya Boyutları (Tahmini)

- Grafik (.png): ~500 KB her biri
- CSV (.csv): ~5-10 KB her biri
- LaTeX (.tex): ~20 KB
- PDF (.pdf): ~2-5 MB (grafiklerle)

**Toplam**: ~15-20 MB

---

## 🔧 Sorun Giderme

### Karşılaştırmalı Statikler Çok Yavaş

```python
# comparative_statics_suite.py içinde:
analyzer = ComparativeStaticsAnalyzer(
    baseline_params=baseline,
    n_points=10,  # 15 yerine 10 (daha hızlı)
    seed=42
)
```

### LaTeX Derlenemiyor

```bash
# Hata mesajlarını gör
cd reports/
pdflatex nash_equilibrium_report.tex
# Son satırlara bak

# Yaygın sorunlar:
# 1. Grafik bulunamıyor → Önce grafikleri oluştur
# 2. Package eksik → tlmgr install <package>
# 3. Syntax hatası → .tex dosyasını düzenle
```

### Grafikler Raporda Görünmüyor

```python
# generate_simple_report.py içinde grafik yollarını kontrol et:
\includegraphics[width=\textwidth]{../figures_quick/1_nash_heatmap.png}
                                   ^^^^^^ Bu yol doğru mu?

# Mutlak yol kullan (gerekirse):
\includegraphics[width=\textwidth]{/Users/muratbeser/Desktop/Spy/figures_quick/1_nash_heatmap.png}
```

---

## 💡 İpuçları

### 1. **Belirli Parametreleri Analiz Et**

```python
# comparative_statics_suite.py'yi düzenle:
param_specs = {
    'gamma': (20.0, 80.0, False),
    'alpha': (50.0, 150.0, False),
    # Diğerlerini yoruma al
}
```

### 2. **Daha Fazla Nokta (Daha Smooth Eğriler)**

```python
analyzer = ComparativeStaticsAnalyzer(
    baseline_params=baseline,
    n_points=30,  # 15 yerine 30
    seed=42
)
```

### 3. **LaTeX Tablosunu Excel'e Aktar**

```bash
# LaTeX tablo → CSV dönüşüm
cd tables/
# Online araç kullan: https://tableconvert.com/
# Ya da pandas:
```

```python
import pandas as pd
# CSV'den tablo oluştur
df = pd.read_csv('figures_comparative_statics/results_gamma.csv')
df[['gamma', 'I1_star', 'I2_star', 'W_star']].to_latex('my_table.tex')
```

---

## ✅ Kontrol Listesi

İlk kez kullanıyorsanız:

- [ ] `tqdm` ve `pandas` kurulu mu? (`pip install tqdm pandas`)
- [ ] Grafikler oluşturulmuş mu? (`python quick_visualizations.py`)
- [ ] Karşılaştırmalı statikler çalışıyor mu? (`python comparative_statics_suite.py`)
- [ ] LaTeX rapor oluşturuldu mu? (`python generate_simple_report.py`)
- [ ] `figures_comparative_statics/` klasöründe 24 dosya var mı?
- [ ] `reports/nash_equilibrium_report.tex` var mı?
- [ ] PDF oluşturuldu mu? (opsiyonel, pdflatex gerekli)

---

## 🎉 Sonuç

Artık projenizde **2 güçlü yeni özellik** var:

### 1️⃣ Karşılaştırmalı Statikler Suite
- ✅ 8 parametre × 15 nokta = 120 Nash dengesi
- ✅ 8 kapsamlı grafik (12 panel her biri)
- ✅ 24 CSV dosyası (sonuçlar + elastikiteler)
- ✅ LaTeX özet tablosu
- ✅ Sistematik sensitivite analizi

### 2️⃣ Otomatik LaTeX/PDF Rapor
- ✅ Profesyonel akademik rapor
- ✅ Tüm sonuçlar tablolarla
- ✅ Tüm grafikler otomatik eklenir
- ✅ Ekonomik yorumlama
- ✅ PDF derleme (opsiyonel)

**Toplam**: 26-27 yeni dosya, ~15-20 MB çıktı

---

## 📚 İlgili Dosyalar

- `comparative_statics_suite.py` - Karşılaştırmalı statikler ana script
- `generate_simple_report.py` - LaTeX/PDF rapor oluşturucu
- `YENİ_ÖZELLİKLER_KILAVUZU.md` - Bu dosya
- `PROJE_TAMAMLANDI.md` - Genel proje özeti

---

**Son Güncelleme**: 2025-10-05
**Durum**: ✅ KULLANIMA HAZIR
