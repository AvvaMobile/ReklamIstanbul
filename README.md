# RTSP Kamera ile İnsan Sayma Sistemi

Bu proje, `rtsp://192.168.1.100:554/H.264/media.smp` RTSP URL'i üzerinden kamera görüntüsünü okuyarak insan sayma işlevi gerçekleştirir.

## 🎯 Özellikler

- ✅ **RTSP Kamera Desteği**: Sabit URL ile kamera bağlantısı
- ✅ **İnsan Tespiti**: YOLOv8 modeli ile gerçek zamanlı tespit
- ✅ **İnsan Sayma**: Saatlik, günlük ve toplam sayım
- ✅ **Tracking**: İnsan takibi ile doğru sayım
- ✅ **Web Arayüzü**: Flask tabanlı web UI
- ✅ **Veri Kaydetme**: Günlük sayım verilerini kaydetme

## 🚀 Hızlı Başlangıç

### 1. Gereksinimler

```bash
pip install -r requirements.txt
```

### 2. RTSP Kamera Testi

```bash
python test_rtsp_simple.py
```

### 3. Ana Uygulama

```bash
python main.py
```

### 4. Web Arayüzü

```bash
python app.py
```

## 📁 Proje Yapısı

```
AvvaImageAI/
├── main.py                 # Ana uygulama (RTSP kamera)
├── app.py                  # Web arayüzü (Flask)
├── quick_start.py          # Hızlı başlangıç
├── test_rtsp_simple.py    # RTSP kamera testi
├── network_camera.py       # RTSP kamera sınıfı
├── human_detector.py       # İnsan tespit modülü
├── counter.py              # İnsan sayma modülü
├── config.py               # Konfigürasyon
├── requirements.txt        # Python bağımlılıkları
└── README.md               # Bu dosya
```

## ⚙️ Konfigürasyon

`config.py` dosyasında RTSP kamera ayarları:

```python
# RTSP Kamera Ayarları
RTSP_URL = "rtsp://192.168.1.100:554/H.264/media.smp"
RTSP_IP = "192.168.1.100"
RTSP_PORT = 554
RTSP_ENCODING = "H.264"

# Kamera performans ayarları
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CAMERA_FPS = 30
```

## 🔧 Kullanım

### Komut Satırı

```bash
# RTSP kamera testi
python test_rtsp_simple.py

# Ana uygulama
python main.py

# Web arayüzü
python app.py
```

### Python API

```python
from network_camera import RTSPCamera
from human_detector import HumanDetector
from counter import HumanCounter

# RTSP kamera başlat
camera = RTSPCamera()
camera.connect()
camera.start_capture()

# İnsan tespit ve sayma
detector = HumanDetector()
counter = HumanCounter()

while True:
    ret, frame = camera.read()
    if ret:
        detections = detector.detect_humans(frame)
        frame, hourly, daily = counter.count_humans(detections, frame)
        
        # Frame'i göster
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

camera.stop_capture()
```

## 📊 Çıktılar

- **Saatlik Sayım**: Saat başına insan sayısı
- **Günlük Sayım**: Günlük toplam insan sayısı
- **Toplam Sayım**: Program başından beri toplam
- **Aktif İnsanlar**: Şu anda görüntüde olan insanlar

## 🌐 Web Arayüzü

Web arayüzü `http://localhost:5000` adresinde çalışır:

- **Ana Sayfa**: Canlı video stream
- **API Endpoints**: JSON formatında veri
- **Sistem Durumu**: RTSP bağlantı bilgileri
- **Sayım Verileri**: Gerçek zamanlı istatistikler

## ⚠️ Önemli Notlar

1. **Ağ Erişimi**: 192.168.1.100 IP adresine erişim gerekli
2. **Port Açık**: 554 portu açık olmalı
3. **Kamera Aktif**: Kamera çalışır durumda olmalı
4. **Codec Desteği**: H.264 codec desteği gerekli

## 🐛 Sorun Giderme

### Bağlantı Hatası
```bash
# RTSP bağlantısını test et
python test_rtsp_simple.py
```

### Frame Okunamıyor
- Kamera ayarlarını kontrol edin
- Ağ bağlantısını test edin
- Port 554'ün açık olduğundan emin olun

### Performans Sorunları
- FPS ayarlarını düşürün (`config.py`)
- Frame boyutunu küçültün
- Model güven eşiğini artırın

## 📝 Gereksinimler

- Python 3.9+
- OpenCV
- PyTorch
- Ultralytics (YOLOv8)
- Flask (web arayüzü için)

## 🔄 Güncellemeler

- ✅ RTSP kamera desteği eklendi
- ✅ Sabit URL konfigürasyonu
- ✅ Gereksiz modüller kaldırıldı
- ✅ Basitleştirilmiş kod yapısı
- ✅ Web arayüzü güncellendi

## 📞 Destek

Sorun yaşarsanız:

1. `python test_rtsp_simple.py` ile test edin
2. Hata mesajlarını kontrol edin
3. Ağ bağlantısını test edin
4. Kamera ayarlarını doğrulayın
5. Port 554'ün açık olduğundan emin olun 