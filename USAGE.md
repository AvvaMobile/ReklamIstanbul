# İnsan Sayma Sistemi - Kullanım Talimatları

## 🚀 Hızlı Başlangıç

### 1. Kurulum

```bash
# Gerekli paketleri yükle
pip3 install -r requirements.txt

# Proje kurulumunu çalıştır
python3 setup.py
```

### 2. Konfigürasyon

`.env` dosyasını düzenleyin:

```env
# Endpoint ayarları
ENDPOINT_URL=http://your-server.com/api/count
ENDPOINT_API_KEY=your_api_key_here

# Debug ayarları
DEBUG=False

# Cihaz ayarları (opsiyonel)
DEVICE_ID=camera_001
LOCATION=main_entrance
```

### 3. Test Sunucusu (Geliştirme İçin)

```bash
# Test endpoint sunucusunu başlat
python3 test_server.py
```

### 4. Endpoint Testi

```bash
# Endpoint bağlantısını test et
python3 test_endpoint.py
```

### 5. Kamera Testi

```bash
# Kamera erişimini test et
python3 test_camera.py
```

### 6. Ana Program

```bash
# İnsan sayma sistemini başlat
python3 main.py
```

## 📋 Sistem Özellikleri

### Saatlik Endpoint Entegrasyonu
- Her saat başında sayım verilerini otomatik olarak endpoint'e gönderir
- Saatlik sayımı sıfırlar
- Başarısız gönderimler için hata yönetimi
- Retry mekanizması

### Veri Formatı
```json
{
  "timestamp": "2024-01-15T14:00:00.123456",
  "hourly_count": 25,
  "daily_count": 150,
  "total_count": 1250,
  "device_id": "camera_001",
  "location": "main_entrance"
}
```

### Log Dosyaları
- `logs/main.log`: Ana program logları
- `logs/counter.log`: Sayım işlemleri
- `logs/endpoint.log`: Endpoint iletişimi

## 🔧 Konfigürasyon Seçenekleri

`config.py` dosyasında aşağıdaki ayarları değiştirebilirsiniz:

```python
# Kamera ayarları
CAMERA_INDEX = 0  # Kamera indeksi
FRAME_WIDTH = 640  # Frame genişliği
FRAME_HEIGHT = 480  # Frame yüksekliği

# İnsan tespit ayarları
DETECTION_THRESHOLD = 0.5  # Güven eşiği
MODEL_PATH = 'yolov8n.pt'  # YOLO model yolu

# Sayım ayarları
COUNTING_LINE_Y_PERCENT = 0.6  # Sayım çizgisi pozisyonu

# Endpoint ayarları
ENDPOINT_URL = 'http://localhost:8000/api/count'
ENDPOINT_API_KEY = 'your_api_key'
ENDPOINT_TIMEOUT = 30  # saniye

# Zamanlama ayarları
HOURLY_RESET = True  # Saatlik sıfırlama aktif mi?
RESET_HOUR = 0  # Hangi saatte sıfırlanacak
```

## 🐛 Sorun Giderme

### Kamera Erişim Sorunu (macOS)
```bash
# Sistem Tercihleri > Güvenlik ve Gizlilik > Kamera
# Terminal uygulamasına kamera erişimi verin
```

### Endpoint Bağlantı Hatası
1. URL'nin doğru olduğunu kontrol edin
2. API anahtarını kontrol edin
3. Ağ bağlantısını kontrol edin
4. Test sunucusunu çalıştırın: `python3 test_server.py`

### Düşük Performans
1. `DETECTION_THRESHOLD` değerini artırın
2. Frame boyutlarını küçültün
3. Debug modunu kapatın

## 📊 Test Sunucusu Endpoint'leri

Test sunucusu çalıştığında şu endpoint'ler kullanılabilir:

- `GET /` - Ana sayfa
- `GET /health` - Health check
- `POST /api/count` - Sayım verisi al
- `GET /api/data` - Alınan verileri görüntüle
- `GET /api/stats` - İstatistikler

## 🔄 Geliştirme

### Yeni Özellik Ekleme
1. İlgili modülü düzenleyin
2. `config.py`'ye gerekli ayarları ekleyin
3. Test edin ve logları kontrol edin

### Endpoint Entegrasyonu
`endpoint_client.py` dosyasını düzenleyerek farklı endpoint formatları için uyarlayabilirsiniz.

## 📝 Örnek Kullanım Senaryoları

### Senaryo 1: Mağaza Giriş Sayımı
```python
# config.py
DEVICE_ID = "store_entrance_01"
LOCATION = "main_store_entrance"
COUNTING_LINE_Y_PERCENT = 0.7  # Giriş kapısının altında
```

### Senaryo 2: Ofis Katılım Sayımı
```python
# config.py
DEVICE_ID = "office_floor_2"
LOCATION = "floor_2_entrance"
HOURLY_RESET = True  # Saatlik raporlama
```

### Senaryo 3: Etkinlik Sayımı
```python
# config.py
DEVICE_ID = "event_hall_01"
LOCATION = "main_hall_entrance"
ENDPOINT_URL = "https://event-api.com/count"
```

## 🚨 Güvenlik Notları

1. API anahtarlarını `.env` dosyasında saklayın
2. `.env` dosyasını git'e commit etmeyin
3. Production'da HTTPS kullanın
4. Endpoint URL'lerini güvenli tutun

## 📞 Destek

Sorun yaşarsanız:
1. Log dosyalarını kontrol edin
2. Test scriptlerini çalıştırın
3. Konfigürasyon ayarlarını kontrol edin 