# RTSP Kamera Entegrasyonu

Bu proje, `rtsp://192.168.1.100:554/H.264/media.smp` RTSP URL'i üzerinden kamera görüntüsünü okumak için düzenlenmiştir.

## 🎯 Hedef RTSP URL

```
rtsp://192.168.1.100:554/H.264/media.smp
```

- **IP Adresi**: 192.168.1.100
- **Port**: 554 (standart RTSP port)
- **Encoding**: H.264
- **Stream Path**: /H.264/media.smp

## 📁 Düzenlenen Dosyalar

### 1. `demo_sunaapi_camera.py`
- Belirtilen IP adresi (192.168.1.100) ile güncellendi
- H.264 encoding desteği eklendi
- Basic format testi eklendi

### 2. `network_camera.py`
- `custom_h264` formatı eklendi
- H.264/media.smp pattern'i için özel destek

### 3. `test_rtsp_camera.py` (YENİ)
- RTSP URL'i için özel test script'i
- 3 farklı yöntemle test

### 4. `rtsp_camera_example.py` (YENİ)
- Basit kamera uygulaması
- Stream gösterme ve frame yakalama

## 🚀 Kullanım

### 1. Basit Test

```bash
# RTSP URL'i ile doğrudan test
python test_rtsp_camera.py
```

### 2. Demo Uygulama

```bash
# SUNAPI kamera demo
python demo_sunaapi_camera.py
```

### 3. Tam Uygulama

```bash
# RTSP kamera uygulaması
python rtsp_camera_example.py
```

## 🔧 Kod Örnekleri

### SUNAPI Kamera ile

```python
from network_camera import SUNAPICamera

# SUNAPI kamera oluştur
camera = SUNAPICamera(
    ip_address="192.168.1.100",
    port=554,
    encoding="H.264"
)

# Custom H.264 formatında bağlan
if camera.connect('custom_h264'):
    ret, frame = camera.read_frame()
    if ret:
        print(f"Frame boyutu: {frame.shape}")
    
    camera.release()
```

### NetworkCamera ile

```python
from network_camera import NetworkCamera

# NetworkCamera ile RTSP
camera = NetworkCamera(
    camera_url="rtsp://192.168.1.100:554/H.264/media.smp",
    camera_type='rtsp'
)

if camera.connect():
    ret, frame = camera.read()
    if ret:
        print(f"Frame boyutu: {frame.shape}")
    
    camera.stop_capture()
```

### OpenCV ile Doğrudan

```python
import cv2

# Doğrudan RTSP URL ile
rtsp_url = "rtsp://192.168.1.100:554/H.264/media.smp"
cap = cv2.VideoCapture(rtsp_url)

if cap.isOpened():
    ret, frame = cap.read()
    if ret:
        print(f"Frame boyutu: {frame.shape}")
    
    cap.release()
```

## 📊 Test Sonuçları

Script'ler şu yöntemleri test eder:

1. **Doğrudan RTSP**: OpenCV ile doğrudan bağlantı
2. **SUNAPI Kamera**: SUNAPI format desteği ile
3. **NetworkCamera**: Gelişmiş özellikler ile

## ⚠️ Önemli Notlar

1. **Ağ Erişimi**: 192.168.1.100 IP adresine erişim gerekli
2. **Port Açık**: 554 portu açık olmalı
3. **Kamera Aktif**: Kamera çalışır durumda olmalı
4. **Codec Desteği**: H.264 codec desteği gerekli

## 🐛 Sorun Giderme

### Bağlantı Hatası
- IP adresini kontrol edin
- Port 554'ün açık olduğundan emin olun
- Ağ bağlantısını test edin

### Frame Okunamıyor
- Kamera ayarlarını kontrol edin
- Encoding formatını doğrulayın
- Kamera yeniden başlatın

### Performans Sorunları
- FPS ayarlarını düşürün
- Buffer boyutunu artırın
- Ağ bant genişliğini kontrol edin

## 📝 Gereksinimler

```bash
pip install opencv-python
pip install numpy
```

## 🔄 Güncellemeler

- ✅ RTSP URL desteği eklendi
- ✅ H.264 encoding desteği
- ✅ Custom format desteği
- ✅ Test script'leri eklendi
- ✅ Örnek uygulama eklendi

## 📞 Destek

Sorun yaşarsanız:
1. Test script'lerini çalıştırın
2. Hata mesajlarını kontrol edin
3. Ağ bağlantısını test edin
4. Kamera ayarlarını doğrulayın
