# 🚀 AvvaImageAI - Kurulum Rehberi

Bu rehber, AvvaImageAI projesini yeni bir bilgisayarda çalıştırmak için gerekli tüm adımları içerir.

## 📋 Sistem Gereksinimleri

### Minimum Gereksinimler
- **İşletim Sistemi**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **Python**: 3.9 veya üzeri
- **RAM**: En az 4GB (8GB önerilen)
- **Disk**: En az 2GB boş alan
- **CPU**: 2 çekirdek (4+ önerilen)

### Önerilen Gereksinimler
- **RAM**: 8GB+
- **CPU**: 4+ çekirdek
- **GPU**: CUDA destekli (opsiyonel)
- **SSD**: Hızlı disk erişimi

## 🔧 Kurulum Adımları

### 1. Python Kurulumu

#### Windows
```bash
# 1. Python 3.9+ indir
# https://www.python.org/downloads/

# 2. Kurulum sırasında "Add Python to PATH" seçeneğini işaretle

# 3. Kurulum sonrası test
python --version
pip --version
```

#### macOS
```bash
# Homebrew ile (önerilen)
brew install python@3.9

# Veya Python.org'dan indir
# https://www.python.org/downloads/macos/
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3.9 python3.9-pip python3.9-venv
```

### 2. Proje Kurulumu

```bash
# 1. Proje klasörüne git
cd /path/to/AvvaImageAI

# 2. Virtual environment oluştur (önerilen)
python3 -m venv venv

# 3. Virtual environment aktifleştir
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Dependencies kur
pip install -r requirements.txt
```

### 3. Environment Ayarları

```bash
# .env dosyası oluştur
cp env_example.txt .env

# .env dosyasını düzenle
# Gerekli ayarları yap
```

## 🧪 Sistem Testi

### Hızlı Test
```bash
# Tüm sistem kontrollerini çalıştır
python3 quick_start.py
```

### Manuel Test
```bash
# Python import testi
python3 -c "import cv2, ultralytics, torch; print('Tüm modüller yüklendi!')"

# Ekran yakalama testi
python3 test_screen_capture.py

# Performans testi
python3 performance_test.py
```

## 🚀 Uygulamayı Çalıştırma

### Kamera Modu
```bash
python3 main.py
```

### Web Arayüzü
```bash
python3 app.py
# Tarayıcıda: http://localhost:5000
```

### Test Modları
```bash
# Kamera testi
python3 test_camera.py

# Ekran yakalama testi
python3 test_screen_capture.py

# Endpoint testi
python3 test_endpoint.py
```

## ⚠️ Olası Sorunlar ve Çözümleri

### 1. Windows Zip Error Hatası
Windows'ta pip kurulum sırasında "zip error" hatası alırsanız:

#### **A) Otomatik Çözüm:**
```bash
# Zip error çözüm script'ini çalıştır
fix_windows_zip_error.bat
```

#### **B) Manuel Çözüm:**
```bash
# 1. Pip cache temizle
pip cache purge

# 2. Pip güncelle
python -m pip install --upgrade pip

# 3. Wheel kur
pip install wheel

# 4. Windows için özel requirements kullan
pip install -r requirements_windows.txt
```

#### **C) Alternatif Kurulum:**
```bash
# Her paketi tek tek kur
pip install opencv-python-headless
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install ultralytics
pip install numpy
pip install flask
# ... diğer paketler
```

#### **D) Visual C++ Redistributable:**
Windows'ta C++ paketleri eksik olabilir:
1. [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe) indir
2. Kur ve bilgisayarı yeniden başlat
3. Pip kurulumunu tekrar dene

### 2. OpenCV Hatası
```bash
# Windows'ta
pip uninstall opencv-python
pip install opencv-python-headless

# macOS'ta
brew install opencv
```

### 3. Torch Hatası
```bash
# CPU versiyonu kur
pip uninstall torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### 4. Permission Hatası (macOS)
1. **Sistem Tercihleri** > **Güvenlik ve Gizlilik** > **Ekran Kaydı**
2. Terminal/Python uygulamasına izin ver
3. Uygulamayı yeniden başlat

### 5. CUDA Hatası
```bash
# config.py'de GPU kullanımını kapat
USE_GPU = False
```

### 6. Model Dosyası Hatası
```bash
# Model dosyalarını kontrol et
ls -la *.pt

# Eksik dosyaları indir veya kopyala
# yolov8n.pt, yolov8s.pt, yolov8m.pt, yolov8l.pt
```

## 📁 Dosya Yapısı

```
AvvaImageAI/
├── app.py                 # Web arayüzü
├── main.py               # Ana uygulama
├── config.py             # Konfigürasyon
├── human_detector.py     # İnsan tespit
├── counter.py            # İnsan sayma
├── screen_capture.py     # Ekran yakalama
├── requirements.txt      # Python dependencies
├── quick_start.py        # Hızlı başlangıç testi
├── *.pt                  # YOLO model dosyaları
├── static/               # Web statik dosyaları
├── templates/            # Web şablonları
└── logs/                 # Log dosyaları
```

## 🔍 Sorun Giderme

### Log Dosyaları
```bash
# Log dosyalarını kontrol et
tail -f logs/main.log
tail -f logs/counter.log
```

### Debug Modu
```bash
# .env dosyasında
DEBUG=True
```

### Verbose Çıktı
```bash
# Detaylı çıktı için
python3 -v main.py
```

## 📞 Destek

Sorun yaşarsanız:
1. Log dosyalarını kontrol edin
2. `python3 quick_start.py` çalıştırın
3. Hata mesajlarını not edin
4. GitHub issue açın

## ✅ Kurulum Kontrol Listesi

- [ ] Python 3.9+ kurulu
- [ ] Virtual environment oluşturuldu
- [ ] Dependencies kuruldu
- [ ] .env dosyası oluşturuldu
- [ ] Model dosyaları mevcut
- [ ] `quick_start.py` başarılı
- [ ] Test uygulamaları çalışıyor
- [ ] Ana uygulama çalışıyor

---

**🎉 Kurulum tamamlandı!** Artık AvvaImageAI'yi kullanabilirsiniz.
