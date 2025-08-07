# İnsan Sayma Sistemi - Web UI

Modern web arayüzü ile insan sayma sistemi.

## 🚀 Özellikler

### 🎨 Modern UI
- **Responsive Tasarım**: Mobil ve masaüstü uyumlu
- **Gradient Tasarım**: Modern görsel tasarım
- **Gerçek Zamanlı Güncelleme**: Canlı istatistikler
- **Animasyonlar**: Smooth geçişler ve efektler

### ⚙️ Konfigürasyon
- **Video Kaynağı Seçimi**: Kamera veya Ekran Yakalama
- **Kamera Listesi**: Otomatik kamera tespiti
- **Ekran Bölgesi**: Belirli alanları izleme
- **Model Seçimi**: Farklı YOLO modelleri
- **Tespit Eşiği**: Ayarlanabilir hassasiyet

### 📊 İstatistikler
- **Saatlik Sayım**: Saatlik insan sayısı
- **Günlük Sayım**: Günlük toplam sayım
- **Toplam Sayım**: Genel toplam
- **Aktif İnsanlar**: Şu anda görünen insanlar
- **FPS Göstergesi**: Performans bilgisi

### 🎮 Kontroller
- **Başlat/Durdur**: Tek tıkla kontrol
- **Durum Göstergesi**: Sistem durumu
- **Bildirimler**: Kullanıcı dostu mesajlar

## 📦 Kurulum

### 1. Gereksinimler
```bash
pip install -r requirements.txt
```

### 2. Web Uygulamasını Başlat
```bash
python3 app.py
```

### 3. Tarayıcıda Aç
```
http://localhost:5000
```

## 🎯 Kullanım

### 1. Konfigürasyon
- **Video Kaynağı**: Kamera veya Ekran Yakalama seçin
- **Kamera Seçimi**: Mevcut kameralar otomatik listelenir
- **Ekran Bölgesi**: Ekran yakalama için bölge seçin
- **Model**: Performans ihtiyacınıza göre model seçin
- **Tespit Eşiği**: Hassasiyeti ayarlayın (0.1-0.9)

### 2. Sistemi Başlat
- Konfigürasyonu tamamlayın
- "Başlat" düğmesine basın
- Sistem hazır olduğunda video akışı başlar

### 3. İzleme
- Sağ tarafta canlı video akışını görün
- Sol panelde istatistikleri takip edin
- Durum göstergesinden sistem durumunu kontrol edin

### 4. Durdurma
- "Durdur" düğmesine basın
- Sistem güvenli şekilde kapanır

## 🖥️ Ekran Görüntüleri

### Ana Sayfa
```
┌─────────────────────────────────────────────────────────┐
│ [İnsan Sayma Sistemi]                    [Kamera] [0 FPS] │
├─────────────────┬───────────────────────────────────────┤
│ Konfigürasyon   │                                       │
│ ├ Video Kaynağı │                                       │
│ ├ Kamera Seçimi │                                       │
│ ├ Model Seçimi  │                                       │
│ └ Tespit Eşiği  │                                       │
│                 │                                       │
│ Kontroller      │                                       │
│ ├ [Başlat]     │                                       │
│ └ [Durdur]     │                                       │
│                 │                                       │
│ İstatistikler   │                                       │
│ ├ Saatlik: 0   │                                       │
│ ├ Günlük: 0    │                                       │
│ ├ Toplam: 0    │                                       │
│ └ Aktif: 0     │                                       │
│                 │                                       │
│ Durum: Hazır    │                                       │
└─────────────────┴───────────────────────────────────────┘
```

## 🔧 API Endpoints

### GET /api/cameras
Mevcut kameraları listeler
```json
[
  {
    "index": 0,
    "name": "Kamera 0",
    "resolution": "640x480"
  }
]
```

### GET /api/config
Mevcut konfigürasyonu döndürür
```json
{
  "use_screen_capture": false,
  "camera_index": 0,
  "screen_region": null,
  "detection_threshold": 0.4,
  "model_path": "yolov8s.pt"
}
```

### POST /api/config
Konfigürasyonu günceller
```json
{
  "use_screen_capture": true,
  "camera_index": 0,
  "screen_region": [0, 0, 800, 600],
  "detection_threshold": 0.5,
  "model_path": "yolov8s.pt"
}
```

### POST /api/start
Sistemi başlatır
```json
{
  "status": "success",
  "message": "Sistem başlatıldı"
}
```

### POST /api/stop
Sistemi durdurur
```json
{
  "status": "success",
  "message": "Sistem durduruldu"
}
```

### GET /api/stats
İstatistikleri döndürür
```json
{
  "hourly_count": 5,
  "daily_count": 25,
  "total_count": 150,
  "active_people": 2,
  "is_running": true
}
```

### GET /video_feed
Video stream endpoint'i (MJPEG format)

## 🎨 Tasarım Özellikleri

### Renk Paleti
- **Ana Renk**: Gradient mavi-mor (#667eea → #764ba2)
- **Vurgu Renk**: Altın (#ffd700)
- **Başarı**: Yeşil (#28a745)
- **Hata**: Kırmızı (#dc3545)
- **Uyarı**: Turuncu (#fd7e14)

### Animasyonlar
- **Hover Efektleri**: Buton ve kart animasyonları
- **Pulse Animasyonu**: Çalışan durum göstergesi
- **Fade In**: Sayfa yükleme animasyonları
- **Slide In**: Panel geçiş animasyonları

### Responsive Tasarım
- **Masaüstü**: Tam ekran layout
- **Tablet**: Sidebar ve içerik yan yana
- **Mobil**: Dikey layout

## 🔧 Gelişmiş Ayarlar

### Performans Optimizasyonu
```python
# app.py'de ayarlayabilirsiniz
app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
```

### SSL Desteği
```python
# HTTPS için
app.run(ssl_context='adhoc', host='0.0.0.0', port=443)
```

### Proxy Desteği
```python
# Reverse proxy için
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
```

## 🐛 Sorun Giderme

### Video Akışı Görünmüyor
1. Kamera izinlerini kontrol edin
2. Tarayıcı konsolunu kontrol edin
3. Flask loglarını kontrol edin

### Kamera Listesi Boş
1. Kamera bağlantısını kontrol edin
2. Sistem izinlerini kontrol edin
3. OpenCV kurulumunu kontrol edin

### Sistem Başlatılamıyor
1. Model dosyasının varlığını kontrol edin
2. GPU bellek kullanımını kontrol edin
3. Python bağımlılıklarını kontrol edin

### Yavaş Performans
1. Model boyutunu küçültün
2. FPS'i düşürün
3. GPU kullanımını kontrol edin

## 📱 Mobil Kullanım

### PWA Desteği
```html
<!-- index.html'e ekleyin -->
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#667eea">
```

### Touch Gestures
- **Swipe**: Panel geçişleri
- **Pinch**: Zoom kontrolü
- **Tap**: Hızlı erişim

## 🔒 Güvenlik

### CORS Ayarları
```python
from flask_cors import CORS
CORS(app, origins=['http://localhost:3000'])
```

### Rate Limiting
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/start')
@limiter.limit("5 per minute")
def start_system():
    # ...
```

### Authentication
```python
from flask_login import LoginManager, login_required
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
@login_required
def index():
    # ...
```

## 🚀 Deployment

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Systemd Service
```ini
[Unit]
Description=Human Counter Web UI
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/human-counter
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Bu web UI ile insan sayma sisteminizi modern ve kullanıcı dostu bir arayüzle kullanabilirsiniz! 🎉 