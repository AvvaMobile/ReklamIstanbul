# Windows Kurulum ve Kullanım Kılavuzu

Bu kılavuz, Windows sistemlerinde AvvaImageAI SUNAPI kamera desteğini kurmak ve kullanmak için hazırlanmıştır.

## 🚀 Hızlı Kurulum

### 1. Otomatik Kurulum (Önerilen)
```batch
# Çift tıklayarak çalıştırın
quick_install_windows.bat
```

### 2. Detaylı Kurulum
```batch
# Çift tıklayarak çalıştırın
install_windows.bat
```

## 📋 Gereksinimler

- **Windows 10/11** (64-bit)
- **Python 3.9+** ([Python.org](https://www.python.org/downloads/))
- **Git** (opsiyonel, [Git-scm.com](https://git-scm.com/))

## 🔧 Kurulum Adımları

### Adım 1: Python Kurulumu
1. [Python.org](https://www.python.org/downloads/) adresinden Python 3.9+ indirin
2. Kurulum sırasında **"Add Python to PATH"** seçeneğini işaretleyin
3. Kurulumu tamamlayın

### Adım 2: Proje İndirme
```batch
# Komut satırında
git clone https://github.com/your-repo/AvvaImageAI.git
cd AvvaImageAI
```

### Adım 3: Otomatik Kurulum
```batch
# Çift tıklayarak çalıştırın
install_windows.bat
```

## 📦 Kurulan Paketler

### Temel Paketler
- **OpenCV**: Görüntü işleme
- **Torch**: Yapay zeka modeli
- **Ultralytics**: YOLO modeli
- **Flask**: Web arayüzü

### SUNAPI Kamera Desteği
- **urllib3**: HTTP/HTTPS istekleri
- **av**: Video/audio işleme
- **websockets**: Gerçek zamanlı iletişim
- **pysrt**: Subtitle desteği

### Test ve Geliştirme
- **pytest**: Test framework
- **black**: Kod formatı
- **flake8**: Kod kalitesi

## 🧪 Test ve Doğrulama

### 1. Hızlı Test
```batch
# Çift tıklayarak çalıştırın
test_windows_sunaapi.bat
```

### 2. Manuel Test
```batch
# Virtual environment aktifleştir
venv\Scripts\activate.bat

# Test scriptlerini çalıştır
python test_sunaapi_integration.py
python test_sunaapi_camera.py
python demo_sunaapi_camera.py
```

## ⚙️ Konfigürasyon

### 1. Environment Variables
`.env` dosyasında kamera bilgilerini ayarlayın:

```bash
# SUNAPI Kamera Ayarları
USE_SUNAPI_CAMERAS=True
SUNAPI_CAMERA_1_IP=192.168.1.121
SUNAPI_CAMERA_1_PORT=554
SUNAPI_CAMERA_1_CHANNEL=0
SUNAPI_CAMERA_1_PROFILE=1
SUNAPI_CAMERA_1_ENCODING=h264
SUNAPI_CAMERA_1_USERNAME=admin
SUNAPI_CAMERA_1_PASSWORD=password123
```

### 2. Config.py Güncelleme
`config.py` dosyasında kamera IP adresini güncelleyin:

```python
SUNAPI_CAMERAS = {
    'sunaapi_camera_1': {
        'ip': 'YOUR_CAMERA_IP',  # Gerçek IP adresi
        'port': 554,
        'channel_id': 0,
        'profile_id': 1,
        'encoding': 'h264',
        'username': 'admin',
        'password': 'password123',
        'enabled': True
    }
}
```

## 🎯 Kullanım

### 1. Ana Sistem
```batch
# Virtual environment aktifleştir
venv\Scripts\activate.bat

# Ana sistemi çalıştır
python main.py
```

### 2. Web Arayüzü
```batch
# Virtual environment aktifleştir
venv\Scripts\activate.bat

# Web arayüzünü çalıştır
python app.py
```

### 3. Test Scriptleri
```batch
# SUNAPI kamera testi
python test_sunaapi_camera.py

# Entegrasyon testi
python test_sunaapi_integration.py

# Demo
python demo_sunaapi_camera.py
```

## 🔍 Sorun Giderme

### 1. Python Bulunamadı
```batch
# PATH kontrolü
echo %PATH%

# Python yeniden kurulumu
# "Add Python to PATH" seçeneğini işaretleyin
```

### 2. Paket Kurulum Hatası
```batch
# Pip güncelleme
pip install --upgrade pip

# Cache temizleme
pip cache purge

# Manuel kurulum
pip install package_name
```

### 3. Virtual Environment Hatası
```batch
# Virtual environment yeniden oluştur
rmdir /s venv
python -m venv venv
venv\Scripts\activate.bat
```

### 4. OpenCV Hatası
```batch
# Alternatif OpenCV kurulumu
pip uninstall opencv-python
pip install opencv-python-headless
```

### 5. Torch Hatası
```batch
# CPU versiyonu kur
pip uninstall torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

## 📁 Dosya Yapısı

```
AvvaImageAI/
├── install_windows.bat          # Detaylı kurulum
├── quick_install_windows.bat    # Hızlı kurulum
├── test_windows_sunaapi.bat     # Windows test scripti
├── requirements_windows.txt      # Windows paket listesi
├── WINDOWS_INSTALL_README.md    # Bu dosya
├── SUNAPI_CAMERA_README.md      # SUNAPI dokümantasyonu
└── ...                          # Diğer proje dosyaları
```

## 🚀 Performans Optimizasyonları

### 1. Windows Özel Ayarlar
- **GPU desteği**: CUDA kurulumu (opsiyonel)
- **Memory optimizasyonu**: Virtual memory ayarları
- **Process priority**: Yüksek öncelik

### 2. Kamera Ayarları
- **Buffer boyutu**: `NETWORK_CAMERA_BUFFER_SIZE = 1`
- **FPS**: `NETWORK_CAMERA_FPS = 30`
- **Timeout**: `NETWORK_CAMERA_TIMEOUT = 5000`

## 📞 Destek

### 1. Hata Raporlama
- Log dosyalarını kontrol edin: `logs/main.log`
- Hata mesajlarını kopyalayın
- Sistem bilgilerini paylaşın

### 2. Yaygın Sorunlar
- **Port 554 kapalı**: Firewall ayarlarını kontrol edin
- **Kimlik doğrulama**: Kullanıcı adı/şifre doğruluğunu kontrol edin
- **Network erişimi**: IP adresi ve subnet mask ayarlarını kontrol edin

### 3. Yardım Kaynakları
- `SUNAPI_CAMERA_README.md`: Detaylı SUNAPI dokümantasyonu
- `INSTALLATION_GUIDE.md`: Genel kurulum kılavuzu
- GitHub Issues: Hata raporlama ve destek

## 🔄 Güncellemeler

### 1. Sistem Güncellemesi
```batch
# Virtual environment aktifleştir
venv\Scripts\activate.bat

# Paketleri güncelle
pip install --upgrade -r requirements_windows.txt
```

### 2. Proje Güncellemesi
```batch
# Git ile güncelle
git pull origin main

# Kurulum scriptlerini yeniden çalıştır
install_windows.bat
```

---

**Not**: Bu kılavuz Windows 10/11 sistemleri için optimize edilmiştir. Farklı Windows sürümlerinde ek ayarlar gerekebilir.
