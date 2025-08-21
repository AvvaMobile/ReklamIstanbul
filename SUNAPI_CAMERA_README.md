# SUNAPI Kamera Desteği

Bu proje, SUNAPI dokümantasyonuna göre RTSP stream formatlarını destekleyen kamera sistemi entegrasyonu sağlar.

## 🚀 Özellikler

- **SUNAPI RTSP Format Desteği**: SUNAPI dokümantasyonunda belirtilen tüm RTSP URL formatları
- **Otomatik Format Tespiti**: Farklı SUNAPI formatlarında otomatik bağlantı denemesi
- **Mevcut Sistem Entegrasyonu**: Network kamera sistemi ile tam uyumluluk
- **Çoklu Format Desteği**: Profile, Live Channel, Multicast ve daha fazlası

## 📋 Desteklenen SUNAPI Formatları

### 1. Temel Formatlar
- **Basic**: `rtsp://<IP>:<PORT>/<encoding>/media.smp`
- **Profile**: `rtsp://<IP>:<PORT>/profile<no>/media.smp`
- **Multicast**: `rtsp://<IP>:<PORT>/multicast/<encoding>/media.smp`

### 2. Kanal Bazlı Formatlar
- **Channel Basic**: `rtsp://<IP>:<PORT>/<chid>/<encoding>/media.smp`
- **Channel Profile**: `rtsp://<IP>:<PORT>/<chid>/profile<no>/media.smp`
- **Live Channel**: `rtsp://<IP>:558/LiveChannel/<chid>/media.smp`

### 3. Encoding Formatları
- H.264 (h264)
- H.265 (h265)
- MPEG4 (mpeg4)
- MJPEG (mjpeg)

## 🔧 Kurulum

### 1. Gereksinimler
```bash
pip install opencv-python numpy requests
```

### 2. Konfigürasyon
`config.py` dosyasında SUNAPI kamera ayarlarını yapın:

```python
# SUNAPI Kamera Desteği
USE_SUNAPI_CAMERAS = True
SUNAPI_CAMERAS = {
    'sunaapi_camera_1': {
        'ip': '192.168.1.121',
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

### 3. Environment Variables
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

## 📖 Kullanım

### 1. Basit SUNAPI Kamera Kullanımı

```python
from network_camera import SUNAPICamera

# SUNAPI kamera oluştur
camera = SUNAPICamera(
    ip_address="192.168.1.121",
    port=554,
    channel_id=0,
    profile_id=1,
    encoding="h264"
)

# Profile formatında bağlan
if camera.connect('profile'):
    print("✅ Bağlantı başarılı!")
    
    # Frame oku
    ret, frame = camera.read_frame()
    if ret:
        print(f"Frame boyutu: {frame.shape}")
    
    camera.release()
```

### 2. NetworkCamera ile SUNAPI Mod

```python
from network_camera import NetworkCamera

# SUNAPI modunda kamera oluştur
camera = NetworkCamera(
    camera_url="192.168.1.121",
    camera_type="sunaapi",
    username="admin",
    password="password123"
)

# Bağlan ve yakalamayı başlat
if camera.connect():
    camera.start_capture()
    
    # Frame oku
    ret, frame = camera.read()
    
    camera.stop_capture()
```

### 3. Farklı Formatlarda Bağlantı

```python
# Profile formatı
camera.connect('profile')

# Live Channel formatı
camera.connect('live_channel')

# Multicast formatı
camera.connect('multicast')

# Özel parametrelerle
camera.connect('channel_profile', chid=1, profile=2)
```

## 🧪 Test

### 1. Entegrasyon Testi
```bash
python3 test_sunaapi_integration.py
```

### 2. SUNAPI Kamera Testi
```bash
python3 test_sunaapi_camera.py
```

### 3. Demo
```bash
python3 demo_sunaapi_camera.py
```

## 🔍 Sorun Giderme

### 1. Bağlantı Başarısız
- **Port kontrolü**: Kamera port numarasını kontrol edin
- **Firewall**: Port'un açık olduğundan emin olun
- **Kimlik bilgileri**: Kullanıcı adı ve şifreyi kontrol edin

### 2. Frame Okunamıyor
- **Format kontrolü**: Doğru SUNAPI formatını kullandığınızdan emin olun
- **Kanal ID**: Kamera kanal numarasını kontrol edin
- **Profil ID**: Kamera profil numarasını kontrol edin

### 3. Performans Sorunları
- **Buffer boyutu**: `NETWORK_CAMERA_BUFFER_SIZE` ayarını optimize edin
- **FPS**: `NETWORK_CAMERA_FPS` ayarını düşürün
- **Encoding**: Daha düşük bitrate encoding kullanın

## 📁 Dosya Yapısı

```
AvvaImageAI/
├── network_camera.py          # SUNAPI kamera sınıfları
├── test_sunaapi_camera.py     # SUNAPI kamera test scripti
├── demo_sunaapi_camera.py     # SUNAPI kamera demo
├── test_sunaapi_integration.py # Entegrasyon testi
├── config.py                  # SUNAPI konfigürasyonu
├── main.py                    # Ana sistem entegrasyonu
└── SUNAPI_CAMERA_README.md   # Bu dosya
```

## 🔗 SUNAPI Dokümantasyon Referansı

Bu implementasyon, `SUNAPI_video_audio_2.6.6.html` dokümantasyonundaki şu bölümlere dayanır:

- **3. RTP/RTSP Streaming**
  - **3.1. Live URL/Authentication**
    - **3.1.1. Live URL for camera**

## 🚀 Ana Sistemde Kullanım

SUNAPI kamera desteği ana sisteme otomatik olarak entegre edilmiştir:

```bash
# SUNAPI kamera ile ana sistemi çalıştır
python3 main.py
```

Sistem otomatik olarak:
1. SUNAPI kamera konfigürasyonunu kontrol eder
2. Farklı formatları dener
3. Başarılı bağlantıyı kurar
4. İnsan tespiti ve sayımı yapar

## 📞 Destek

Herhangi bir sorun yaşarsanız:
1. Test scriptlerini çalıştırın
2. Log dosyalarını kontrol edin
3. Konfigürasyon ayarlarını doğrulayın
4. Kamera dokümantasyonunu kontrol edin

## 🔄 Güncellemeler

- **v1.0**: İlk SUNAPI kamera desteği
- **v1.1**: Çoklu format desteği
- **v1.2**: Ana sistem entegrasyonu
- **v1.3**: Otomatik format tespiti

---

**Not**: Bu sistem, mevcut network kamera desteğini korur ve SUNAPI desteğini alternatif olarak ekler.
