# 📕 PDF Derleme Kılavuzu

**Tarih**: 2025-10-05
**Durum**: ✅ LaTeX raporu hazır, PDF derleme için kılavuz

---

## 🎯 Durum

✅ **LaTeX raporu oluşturuldu**: `reports/nash_equilibrium_report.tex`
✅ **Tüm grafikler mevcut**:
- `figures_quick/` - 5 grafik
- `figures_advanced/` - 2 grafik

⚠️ **pdflatex kurulu değil** - PDF otomatik derlenemedi

---

## 🚀 PDF Oluşturma Seçenekleri

### Seçenek 1: LaTeX Kurulumu (MacOS)

#### Homebrew ile MacTeX (Önerilen):
```bash
# Homebrew kurulu değilse önce kur:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# MacTeX kur (~4 GB, tüm LaTeX paketleri):
brew install --cask mactex

# Yeni terminal aç (PATH güncellemesi için)

# PDF derle:
cd /Users/muratbeser/Desktop/Spy/reports
pdflatex nash_equilibrium_report.tex
pdflatex nash_equilibrium_report.tex  # 2. kez (references için)

# PDF aç:
open nash_equilibrium_report.pdf
```

**Süre**: İlk kurulum ~30 dakika, sonraki derlemeler ~10 saniye

---

#### BasicTeX ile (Hafif Versiyon, ~100 MB):
```bash
brew install --cask basictex

# PATH ekle (yeni terminal'de):
export PATH="/Library/TeX/texbin:$PATH"

# Eksik paketleri kur:
sudo tlmgr update --self
sudo tlmgr install collection-fontsrecommended
sudo tlmgr install collection-latexrecommended

# PDF derle:
cd /Users/muratbeser/Desktop/Spy/reports
pdflatex nash_equilibrium_report.tex
pdflatex nash_equilibrium_report.tex

# PDF aç:
open nash_equilibrium_report.pdf
```

**Süre**: İlk kurulum ~5-10 dakika

---

### Seçenek 2: Online LaTeX Derleyici (Kurulum Gerektirmez)

#### Overleaf (Ücretsiz):

1. **Adrese git**: https://www.overleaf.com/

2. **Yeni proje oluştur**: "New Project" → "Blank Project"

3. **Dosyaları yükle**:
   - `nash_equilibrium_report.tex` → Ana klasöre
   - `figures_quick/` klasörünü → Klasör olarak yükle
   - `figures_advanced/` klasörünü → Klasör olarak yükle

4. **Derle**: Otomatik derler (yeşil "Recompile" butonu)

5. **İndir**: PDF'i indir

**Avantajlar**:
- Kurulum gerektirmez
- Hemen kullanılabilir
- Bulut tabanlı

**Dezavantajlar**:
- İnternet gerekli
- Dosya yükleme gerekli

---

#### Papeeria (Alternatif):

https://papeeria.com/

---

#### ShareLaTeX (Alternatif):

https://www.sharelatex.com/

---

### Seçenek 3: VS Code ile (Geliştiriciler İçin)

```bash
# LaTeX Workshop extension kur:
code --install-extension james-yu.latex-workshop

# MacTeX veya BasicTeX kur (yukarıdaki adımlar)

# VS Code'da aç:
code /Users/muratbeser/Desktop/Spy/reports/nash_equilibrium_report.tex

# Build: Cmd+Alt+B (Mac) veya Ctrl+Alt+B (Linux)
```

---

## 🔧 Manuel Derleme (Terminal)

LaTeX kurulumu tamamlandıktan sonra:

```bash
cd /Users/muratbeser/Desktop/Spy/reports

# 1. Derleme (ilk geçiş):
pdflatex nash_equilibrium_report.tex

# 2. Derleme (references için):
pdflatex nash_equilibrium_report.tex

# PDF'i aç:
open nash_equilibrium_report.pdf

# Yardımcı dosyaları temizle (opsiyonel):
rm *.aux *.log *.out *.toc
```

---

## 📋 Grafik Yolları (Doğrulama)

LaTeX dosyası şu grafikleri kullanıyor:

```latex
\includegraphics[width=0.8\textwidth]{../figures_quick/1_nash_heatmap.png}
\includegraphics[width=\textwidth]{../figures_advanced/advanced_welfare.png}
\includegraphics[width=\textwidth]{../figures_advanced/advanced_dashboard.png}
```

**Kontrol**:
```bash
cd /Users/muratbeser/Desktop/Spy/reports
ls -l ../figures_quick/1_nash_heatmap.png
ls -l ../figures_advanced/advanced_welfare.png
ls -l ../figures_advanced/advanced_dashboard.png
```

✅ **Tüm dosyalar mevcut ve erişilebilir**

---

## 🐛 Sorun Giderme

### Hata: "File not found"

**Sorun**: Grafik dosyaları bulunamıyor

**Çözüm**:
```bash
# Grafikleri tekrar oluştur:
cd /Users/muratbeser/Desktop/Spy
python quick_visualizations.py
python advanced_visualizations_fast.py
```

---

### Hata: "Undefined control sequence"

**Sorun**: LaTeX paketi eksik

**Çözüm**:
```bash
# Eksik paketi kur:
sudo tlmgr install <paket-adi>

# Örnek:
sudo tlmgr install amsmath
sudo tlmgr install booktabs
```

---

### Hata: "! LaTeX Error: File not found"

**Sorun**: .tex dosyası yanlış konumda

**Çözüm**:
```bash
# Doğru klasörde olduğundan emin ol:
cd /Users/muratbeser/Desktop/Spy/reports
pwd  # /Users/muratbeser/Desktop/Spy/reports olmalı
```

---

## 📊 Alternatif: Markdown → PDF

LaTeX istemiyorsanız, Markdown rapor da oluşturabiliriz:

```bash
# Pandoc kur:
brew install pandoc

# Markdown rapor oluştur (yeni script gerekli):
python generate_markdown_report.py

# PDF'e çevir:
pandoc nash_equilibrium_report.md -o nash_equilibrium_report.pdf
```

---

## 💡 Öneriler

### Hızlı Başlangıç (En Kolay):
1. **Overleaf** kullan (kurulum gerektirmez)
2. Dosyaları yükle
3. PDF'i indir

### Uzun Vadeli (En İyi):
1. **MacTeX** kur (bir kez)
2. Sonraki tüm raporları lokal derle
3. Hızlı ve güvenilir

### Geliştirici:
1. **VS Code + LaTeX Workshop**
2. Syntax highlighting + auto-compile
3. Profesyonel ortam

---

## ✅ Kontrol Listesi

Başarılı PDF derlemesi için:

- [ ] LaTeX kurulumu tamamlandı (MacTeX/BasicTeX/Overleaf)
- [ ] Grafikler oluşturuldu (`figures_quick/`, `figures_advanced/`)
- [ ] `reports/` klasöründeyim
- [ ] `pdflatex nash_equilibrium_report.tex` çalıştı
- [ ] 2. kez çalıştırdım (references için)
- [ ] `nash_equilibrium_report.pdf` oluştu
- [ ] PDF açılıyor ve grafikler görünüyor

---

## 🎉 Başarı!

PDF başarıyla oluşturulduktan sonra:

```bash
# PDF'i aç:
open reports/nash_equilibrium_report.pdf

# Paylaş:
cp reports/nash_equilibrium_report.pdf ~/Desktop/
```

---

## 📚 Ek Kaynaklar

- **MacTeX**: https://www.tug.org/mactex/
- **BasicTeX**: https://www.tug.org/mactex/morepackages.html
- **Overleaf**: https://www.overleaf.com/learn
- **LaTeX Tutorial**: https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes

---

**Son Güncelleme**: 2025-10-05
**Durum**: ✅ Grafikler hazır, PDF derleme kılavuzu tamamlandı
