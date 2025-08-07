# Ekran Yakalama Kullanım Kılavuzu

## 🖥️ Ekran Yakalama Özelliği

İnsan sayma sisteminiz artık kamera yerine ekran görüntüsü kullanabilir. Bu özellik özellikle şu durumlarda kullanışlıdır:

- **Uzaktan izleme**: Başka bir bilgisayarın ekranını izlemek
- **Test amaçlı**: Kamera olmadan test yapmak
- **Belirli uygulama izleme**: Sadece belirli bir pencereyi/bölgeyi izlemek
- **Performans testi**: Sistem performansını test etmek

## ⚙️ Kurulum

### 1. Gereksinimler
```bash
pip install Pillow psutil
```

### 2. İzinler (macOS)
macOS'ta ekran yakalama için izin vermeniz gerekir:

1. **Sistem Tercihleri** > **Güvenlik ve Gizlilik** > **Ekran Kaydı**
2. Python/Terminal uygulamasına izin verin
3. Uygulamayı yeniden başlatın

## 🎯 Kullanım

### Temel Kullanım
```bash
# Ekran yakalama modunda çalıştır
python3 main.py
```

### Konfigürasyon
`config.py` dosyasında ayarları değiştirin:

```python
# Ekran yakalama ayarları
USE_SCREEN_CAPTURE = True  # Ekran yakalama modunu aktif et
SCREEN_CAPTURE_FPS = 10    # FPS ayarı (performans için düşük tutun)
SCREEN_REGION = None        # Tüm ekran
# SCREEN_REGION = (0, 0, 800, 600)  # Belirli bölge
```

## 📍 Bölge Seçimi

### 1. Tüm Ekran
```python
SCREEN_REGION = None
```

### 2. Belirli Bölge
```python
# Format: (x, y, width, height)
SCREEN_REGION = (0, 0, 800, 600)  # Sol üst köşeden 800x600
SCREEN_REGION = (400, 300, 800, 600)  # Merkez bölge
```

### 3. Önceden Tanımlanmış Bölgeler
```python
# screen_config.py kullanarak
from screen_config import ScreenConfig

# Tüm ekran
ScreenConfig.set_region('full_screen')

# Sol üst köşe
ScreenConfig.set_region('top_left')

# Merkez bölge
ScreenConfig.set_region('center')

# Küçük bölge
ScreenConfig.set_region('small_region')
```

## 🔧 Performans Optimizasyonları

### FPS Ayarları
```python
# Yüksek performans için
SCREEN_CAPTURE_FPS = 5

# Dengeli performans için
SCREEN_CAPTURE_FPS = 10

# Yüksek kalite için
SCREEN_CAPTURE_FPS = 15
```

### Frame İşleme
```python
# Ekran yakalama için optimize edilmiş
PROCESS_EVERY_N_FRAMES = 3  # Her 3 frame'de bir işle
```

## 📊 Test ve Doğrulama

### Ekran Yakalama Testi
```bash
python3 test_screen_capture.py
```

### Performans Testi
```bash
python3 performance_test.py
```

### Bölge Testi
```bash
python3 screen_config.py
```

## 🎮 Kullanım Senaryoları

### 1. Video Konferans İzleme
```python
# Zoom/Teams penceresini izle
SCREEN_REGION = (100, 100, 1280, 720)
```

### 2. Webcam Alanı İzleme
```python
# Webcam bölgesini izle
SCREEN_REGION = (200, 200, 640, 480)
```

### 3. Belirli Uygulama İzleme
```python
# Belirli bir uygulama penceresini izle
SCREEN_REGION = (0, 0, 1024, 768)
```

## ⚠️ Dikkat Edilecekler

### 1. Performans
- Ekran yakalama CPU yoğun bir işlemdir
- FPS'i düşük tutun (5-10 FPS)
- Büyük ekranlarda bölge kullanın

### 2. İzinler
- macOS'ta ekran kaydı izni gerekir
- Windows'ta ekran yakalama izni gerekebilir
- Linux'ta X11 izinleri gerekebilir

### 3. Gizlilik
- Ekran görüntüsü alırken dikkatli olun
- Hassas bilgileri içeren alanları izlemeyin
- Test amaçlı kullanın

## 🐛 Sorun Giderme

### Ekran Yakalama Çalışmıyor
1. İzinleri kontrol edin
2. `test_screen_capture.py` çalıştırın
3. Python sürümünü kontrol edin

### Düşük Performans
1. FPS'i düşürün
2. Bölge kullanın
3. `PROCESS_EVERY_N_FRAMES` değerini artırın

### Yanlış Bölge
1. Koordinatları kontrol edin
2. Ekran çözünürlüğünü kontrol edin
3. Test bölgesi kullanın

## 📈 Performans İpuçları

### 1. Bölge Kullanımı
```python
# Tüm ekran yerine bölge kullanın
SCREEN_REGION = (0, 0, 800, 600)  # %50 daha hızlı
```

### 2. FPS Optimizasyonu
```python
# Test için düşük FPS
SCREEN_CAPTURE_FPS = 5

# Üretim için orta FPS
SCREEN_CAPTURE_FPS = 10
```

### 3. Frame İşleme
```python
# Ekran yakalama için optimize
PROCESS_EVERY_N_FRAMES = 3
```

## 🎯 Örnek Kullanımlar

### Zoom Toplantısı İzleme
```python
# config.py
USE_SCREEN_CAPTURE = True
SCREEN_REGION = (100, 100, 1280, 720)  # Zoom penceresi
SCREEN_CAPTURE_FPS = 8
PROCESS_EVERY_N_FRAMES = 2
```

### Webcam Test
```python
# config.py
USE_SCREEN_CAPTURE = True
SCREEN_REGION = (200, 200, 640, 480)  # Webcam alanı
SCREEN_CAPTURE_FPS = 10
```

### Tam Ekran İzleme
```python
# config.py
USE_SCREEN_CAPTURE = True
SCREEN_REGION = None  # Tüm ekran
SCREEN_CAPTURE_FPS = 5  # Düşük FPS
PROCESS_EVERY_N_FRAMES = 3
```

Bu kılavuz ile ekran yakalama özelliğini etkili bir şekilde kullanabilirsiniz! 