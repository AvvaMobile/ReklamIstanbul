# AvvaImageAI - İnsan Sayma Sistemi

Gelişmiş performans optimizasyonları ve ekran yakalama desteği ile insan sayma sistemi.

## 🚀 Yeni Özellikler

### Performans İyileştirmeleri
- **GPU Desteği**: CUDA ile hızlandırılmış işlem
- **Model Optimizasyonu**: YOLOv8n modeli ile daha hızlı tespit
- **Frame Atlama**: Performans için akıllı frame işleme
- **Tracking**: Gelişmiş insan takip sistemi
- **Bellek Optimizasyonu**: Düşük bellek kullanımı
- **FPS Optimizasyonu**: 25 FPS ekran yakalama desteği
- **Frame Boyut Optimizasyonu**: 480x360 boyutunda hızlı işleme

### 🖥️ Ekran Yakalama Desteği
- **Kamera Alternatifi**: Ekran görüntüsü ile insan sayma
- **Bölge Seçimi**: Belirli alanları izleme
- **Çoklu Monitör**: Birden fazla ekran desteği
- **Performans Optimizasyonu**: Düşük CPU kullanımı
- **Yüksek FPS**: 25 FPS ekran yakalama
- **Thread Optimizasyonu**: Verimli frame yakalama

### Model Seçenekleri
- `yolov8n.pt`: Nano - Hızlı, küçük
- `yolov8s.pt`: Small - Dengeli (varsayılan)
- `yolov8m.pt`: Medium - Orta performans
- `yolov8l.pt`: Large - Yüksek doğruluk
- `yolov8x.pt`: XLarge - En yüksek doğruluk

## 📦 Kurulum

### Gereksinimler
```bash
pip install -r requirements.txt
```

### GPU Desteği (Opsiyonel)
```bash
# CUDA destekli PyTorch kurulumu
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Ekran Yakalama İzinleri (macOS)
1. **Sistem Tercihleri** > **Güvenlik ve Gizlilik** > **Ekran Kaydı**
2. Python/Terminal uygulamasına izin verin
3. Uygulamayı yeniden başlatın

## ⚙️ Konfigürasyon

### Çevre Değişkenleri
`.env` dosyası oluşturun:
```env
USE_GPU=True
USE_SCREEN_CAPTURE=True
DEBUG=False
ENDPOINT_URL=http://localhost:8000/api/count
ENDPOINT_API_KEY=your_api_key
```

### Performans Ayarları
`config.py` dosyasında performans parametrelerini ayarlayabilirsiniz:

```python
# Model performans ayarları - MVP için optimize edilmiş
MODEL_CONFIDENCE = 0.5  # Model güven eşiği (daha az false positive)
MODEL_IOU_THRESHOLD = 0.4  # IOU eşiği (daha hızlı)
MODEL_MAX_DET = 20  # Maksimum tespit sayısı (daha hızlı)

# Performans optimizasyonları - MVP için optimize edilmiş
PROCESS_EVERY_N_FRAMES = 1  # Her frame işlensin (performans için)
SKIP_FRAMES_FOR_TRACKING = 1  # Takip için frame atlama

# Ekran yakalama ayarları - MVP için optimize edilmiş
USE_SCREEN_CAPTURE = True  # Ekran yakalama modu
SCREEN_CAPTURE_FPS = 25    # Ekran yakalama FPS'i (yüksek performans)
SCREEN_REGION = None        # Tüm ekran veya belirli bölge

# Frame boyut ayarları - MVP için optimize edilmiş
FRAME_WIDTH = 480   # Daha küçük boyut (performans için)
FRAME_HEIGHT = 360  # Daha küçük boyut (performans için)
```

## 🎯 Kullanım

### Kamera Modu
```bash
# Kamera ile çalıştır
python3 main.py
```

### Ekran Yakalama Modu
```bash
# Ekran yakalama ile çalıştır
# config.py'de USE_SCREEN_CAPTURE = True yapın
python3 main.py
```

### Performans Testi
```bash
python3 performance_test.py
```

### Model Seçici
```bash
python3 model_selector.py
```

### Ekran Yakalama Testi
```bash
python3 test_screen_capture.py
```

## 📍 Ekran Yakalama Bölge Seçimi

### Tüm Ekran
```python
SCREEN_REGION = None
```

### Belirli Bölge
```python
# Format: (x, y, width, height)
SCREEN_REGION = (0, 0, 800, 600)  # Sol üst köşeden 800x600
SCREEN_REGION = (400, 300, 800, 600)  # Merkez bölge
```

### Önceden Tanımlanmış Bölgeler
```python
from screen_config import ScreenConfig

ScreenConfig.set_region('full_screen')    # Tüm ekran
ScreenConfig.set_region('top_left')       # Sol üst köşe
ScreenConfig.set_region('center')         # Merkez bölge
ScreenConfig.set_region('small_region')   # Küçük bölge
ScreenConfig.set_region('webcam_area')    # Webcam alanı
```

## 📊 Performans Metrikleri

### Optimizasyon Öncesi
- FPS: ~15-20
- Bellek Kullanımı: ~800MB
- Tespit Doğruluğu: %75-80
- Ekran Yakalama: 10 FPS
- Frame İşleme: Her 3 frame'den 1'i

### Optimizasyon Sonrası (MVP)
- FPS: ~25-35 (Kamera)
- FPS: ~20-25 (Ekran Yakalama)
- Bellek Kullanımı: ~500MB
- Tespit Doğruluğu: %80-85
- Ekran Yakalama: 25 FPS
- Frame İşleme: Her frame işlenir
- Frame Boyutu: 480x360 (daha hızlı)

### MVP Performans Özellikleri
- **Yüksek FPS**: 25 FPS ekran yakalama
- **Hızlı Model**: YOLOv8n (nano) modeli
- **Optimize Frame**: 480x360 boyutunda işleme
- **GPU Desteği**: Varsayılan olarak aktif
- **Thread Optimizasyonu**: Verimli frame yakalama
- **Akıllı İşleme**: Her frame işlenir

## 🔧 Gelişmiş Ayarlar

### GPU Kullanımı
```python
# config.py
USE_GPU = True  # GPU kullanımını aktifleştir
DEVICE = 'cuda' if USE_GPU else 'cpu'
```

### Model Seçimi
```python
# config.py
MODEL_PATH = 'yolov8s.pt'  # Daha büyük model
```

### Tracking Parametreleri
```python
# config.py
TRACKING_THRESHOLD = 30  # piksel - daha hassas takip
SIZE_THRESHOLD = 0.4  # boyut farkı toleransı
```

### Ekran Yakalama Optimizasyonu
```python
# config.py
SCREEN_CAPTURE_FPS = 10  # Düşük FPS performans için
PROCESS_EVERY_N_FRAMES = 3  # Ekran yakalama için yavaş işleme
```

## 🎮 Kullanım Senaryoları

### Video Konferans İzleme
```python
# Zoom/Teams penceresini izle
SCREEN_REGION = (100, 100, 1280, 720)
SCREEN_CAPTURE_FPS = 8
```

### Webcam Alanı İzleme
```python
# Webcam bölgesini izle
SCREEN_REGION = (200, 200, 640, 480)
SCREEN_CAPTURE_FPS = 10
```

### Belirli Uygulama İzleme
```python
# Belirli bir uygulama penceresini izle
SCREEN_REGION = (0, 0, 1024, 768)
SCREEN_CAPTURE_FPS = 5
```

## 🐛 Sorun Giderme

### Düşük FPS
1. GPU kullanımını kontrol edin
2. Model boyutunu küçültün
3. Frame işleme sıklığını azaltın
4. Ekran yakalama için FPS'i düşürün

### Yüksek Bellek Kullanımı
1. `MODEL_MAX_DET` değerini düşürün
2. Frame boyutunu küçültün
3. Buffer boyutunu azaltın

### Yanlış Tespit
1. `DETECTION_THRESHOLD` değerini artırın
2. Daha büyük model kullanın
3. Işık koşullarını iyileştirin

### Ekran Yakalama Sorunları
1. İzinleri kontrol edin
2. `test_screen_capture.py` çalıştırın
3. FPS'i düşürün
4. Belirli bölge kullanın

## 📝 Log Dosyaları

Sistem logları `logs/` klasöründe saklanır:
- `main.log`: Ana sistem logları
- `counter.log`: Sayaç işlemleri
- `endpoint.log`: Endpoint bağlantıları

## 📚 Ek Dokümantasyon

- [Ekran Yakalama Kılavuzu](SCREEN_CAPTURE_GUIDE.md): Detaylı ekran yakalama kullanımı
- [Performans Testi](performance_test.py): Sistem performans testi
- [Model Seçici](model_selector.py): Model performans karşılaştırması

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📞 İletişim

Sorularınız için issue açabilir veya iletişime geçebilirsiniz. 