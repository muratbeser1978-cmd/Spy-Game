# 📊 Grafik Görselleştirme Kullanım Kılavuzu

## ✅ Başarıyla Oluşturuldu!

5 profesyonel grafik başarıyla oluşturuldu. Grafikler `figures_quick/` klasöründe.

---

## 🚀 Hızlı Başlangıç

### Grafikleri Oluştur:
```bash
source venv/bin/activate
python quick_visualizations.py
```

**Süre**: ~30-60 saniye
**Çıktı**: `figures_quick/` klasöründe 5 PNG dosyası (300 DPI, yüksek kalite)

---

## 📁 Oluşturulan Grafikler

### 1. **1_nash_heatmap.png** - Nash Dengesi Haritası
**Ne Gösterir:**
- Toplam fayda (U₁ + U₂) haritası
- X ekseni: Lider yatırımı (I₁)
- Y ekseni: Takipçi yatırımı (I₂)
- Kırmızı yıldız: Nash dengesi noktası

**Nasıl Yorumlanır:**
- Yeşil bölgeler: Yüksek toplam fayda
- Kırmızı bölgeler: Düşük toplam fayda
- Nash noktası: Her iki firmanın da en iyi tepkisinin kesiştiği nokta

**Kullanım:**
- Optimal yatırım seviyelerini görsel olarak doğrula
- Parametre değişikliklerinin etkisini gör

---

### 2. **2_welfare.png** - Refah Bileşenleri
**Ne Gösterir:**
- **Sol**: Bar chart (Tüketici Artığı, Lider Karı, Takipçi Karı)
- **Sağ**: Pasta grafiği (refah dağılımı yüzde)

**Nasıl Yorumlanır:**
- Tüketici artığı genellikle en büyük bileşen
- Kırmızı çizgi: Toplam refah (W*)
- Pasta: Her bileşenin toplam refahtaki payı

**Kullanım:**
- Refah analizi için
- Politika önerilerinde kimin kazanıp kaybettiğini göster

---

### 3. **3_espionage_params.png** - Casusluk Parametreleri
**Ne Gösterir:**
- **Sol**: ρ (Casusluk başarı olasılığı) haritası
- **Sağ**: κ (Sinyal güvenilirliği) haritası

**Nasıl Yorumlanır:**
- **ρ haritası**:
  - Mavi koyulaştıkça casusluk daha başarılı
  - I₂ artınca ρ artar (daha fazla saldırı)
  - I₁ artınca ρ azalır (daha iyi savunma)

- **κ haritası**:
  - Turuncu koyulaştıkça sinyal daha güvenilir
  - Sadece I₂'ye bağlı (I₁'den bağımsız!)
  - I₂ artınca κ artar

**Kullanım:**
- Casusluk teknolojisinin etkinliğini analiz et
- Savunma vs saldırı yatırımlarının etkisini karşılaştır

---

### 4. **4_investment_analysis.png** - Yatırım Analizi (4 Panel)
**Ne Gösterir:**

**[Üst Sol]**: Nash Yatırımları
- Lider ve Takipçi'nin optimal yatırım seviyeleri

**[Üst Sağ]**: Yatırım Maliyetleri
- Her firmanın yatırım maliyeti (κᵢ·Iᵢ²/2)

**[Alt Sol]**: Brüt vs Net Kar
- Brüt (V): Yatırım öncesi kar
- Net (U): Yatırım sonrası kar
- Fark: Yatırım maliyeti

**[Alt Sağ]**: ROI (Kar/Maliyet Oranı)
- Yatırımın getirisi
- Kırmızı çizgi (1x): Başabaş noktası
- >1x: Karlı yatırım
- <1x: Zararlı yatırım

**Kullanım:**
- Yatırımların karlılığını değerlendir
- Hangi firmanın daha verimli yatırım yaptığını gör

---

### 5. **5_summary_dashboard.png** - Özet Dashboard
**Ne Gösterir:**
- **[Üst Sol]**: Anahtar metrikler (I*, ρ*, κ*, yakınsama)
- **[Üst Sağ]**: Kar detayları (brüt, net, maliyet)
- **[Alt]**: Refah bileşenleri bar chart

**Nasıl Yorumlanır:**
- Tüm önemli sonuçları tek sayfada görüntüle
- Sunum ve rapor için ideal
- Yakınsama durumunu kontrol et (✓/✗)

**Kullanım:**
- Hızlı özet için
- Sunumlarda tek slide olarak kullan
- Sonuçları paylaşırken

---

## 🎨 Gelişmiş Görselleştirme

### Tam Paket (10 Grafik):
```bash
python create_rich_visualizations.py
```

**İçerik** (yaklaşık 5-10 dakika):
1. Nash Dengesi 2D Harita (gelişmiş)
2. En İyi Tepki Eğrileri
3. Kar Fonksiyonları 3D Yüzey
4. Refah Bileşenleri (detaylı)
5. Karşılaştırmalı Statikler (parametrelerin etkisi)
6. Casusluğun Etkisi (ρ ve κ analizi)
7. Yatırım Maliyetleri Analizi
8. Fiyat Dağılımı (Monte Carlo)
9. Stratejik Etkileşim Analizi
10. Özet Dashboard (detaylı)

**Çıktı**: `figures_rich/` klasörü

**Uyarı**: Bu script daha uzun sürer (5-10 dakika) ama çok daha kapsamlı grafikler üretir.

---

## 📖 Özelleştirme

### Farklı Parametrelerle Test:

```python
# quick_visualizations.py dosyasını düzenle:

# Örnek: Daha yüksek casusluk maliyeti
params = Parameters(
    alpha=100.0,
    beta=1.5,
    delta=0.3,
    gamma=45.0,
    kappa_1=0.5,
    kappa_2=2.0,  # Daha pahalı casusluk!
    epsilon=0.5,
    gamma_exponent=0.6,
    lambda_defense=1.5,
    iota=2.0,
    sigma_epsilon=10.0,
    sigma_c=8.0,
    I_bar=20.0,
    mu_c=40.0,
)
```

Sonra tekrar çalıştır:
```bash
python quick_visualizations.py
```

---

## 💡 İpuçları

### 1. **Hızlı Görüntüleme:**
```bash
# Mac:
open figures_quick/

# Linux:
xdg-open figures_quick/
```

### 2. **Grafikleri Karşılaştır:**
```bash
# Farklı parametre setleriyle birden fazla kez çalıştır
# Klasör adını değiştir:
# OUTPUT_DIR = Path("figures_scenario_1")
```

### 3. **Yüksek Kalite:**
- Tüm grafikler 300 DPI (baskı kalitesi)
- PNG formatı (şeffaf arka plan destekli)
- Vektörel metin (ölçeklenebilir)

### 4. **Renkler:**
- Colorblind-friendly palettes
- Yeşil-Kırmızı: Refah haritaları
- Mavi-Turuncu: Firma karşılaştırmaları
- Mavi-Kırmızı: İkame/Tamamlayıcı analizi

---

## 🔧 Sorun Giderme

### Grafik oluşturulmuyor:
```bash
# Matplotlib backend kontrolü:
python -c "import matplotlib; print(matplotlib.get_backend())"

# Sorun varsa:
export MPLBACKEND=Agg
python quick_visualizations.py
```

### Seaborn hatası:
```bash
pip install seaborn
```

### Grafik kalitesi düşük:
```python
# Script içinde DPI artır:
plt.savefig(..., dpi=600)  # Varsayılan: 300
```

---

## 📊 Örnek Kullanım Senaryoları

### Senaryo 1: Makale İçin Grafikler
```bash
python quick_visualizations.py
# Kullan: 1, 2, 3, 5
# Bunlar en temiz ve akademik görünümlü
```

### Senaryo 2: Sunum
```bash
python quick_visualizations.py
# Kullan: 1, 5
# Dashboard tek slide olarak mükemmel
```

### Senaryo 3: Detaylı Analiz
```bash
python create_rich_visualizations.py
# Tüm 10 grafik
# Appendix veya teknik rapor için
```

---

## ✅ Sonuç

**Oluşturulan grafikler:**
- ✅ Profesyonel kalite (300 DPI)
- ✅ Kolay yorumlanabilir
- ✅ Akademik standartlara uygun
- ✅ Renk körlüğü dostu
- ✅ Özelleştirilebilir

**Kodunuz artık hem sayısal sonuçlar hem de zengin görseller üretiyor!** 🎉

---

**Son Güncelleme**: 2025-10-05
