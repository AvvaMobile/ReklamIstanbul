import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

class Config:
    # Kamera ayarları
    CAMERA_INDEX = 1  # Varsayılan kamera
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    
    # Ekran yakalama ayarları
    USE_SCREEN_CAPTURE = True  # Ekran yakalama modunu aktif et
    SCREEN_CAPTURE_FPS = 10  # Ekran yakalama FPS'i (düşük tutuyoruz performans için)
    SCREEN_REGION = None  # Belirli bölge (x, y, width, height) veya None (tüm ekran)
    SCREEN_MONITOR = 0  # Monitör seçimi (0, 1, 2...)
    
    # İnsan tespit ayarları - İyileştirilmiş
    DETECTION_THRESHOLD = 0.4  # Daha düşük eşik değeri
    MODEL_PATH = 'yolov8s.pt'  # Daha büyük model (yolov8n.pt yerine)
    
    # Model performans ayarları
    MODEL_CONFIDENCE = 0.4  # Model güven eşiği
    MODEL_IOU_THRESHOLD = 0.5  # IOU eşiği
    MODEL_MAX_DET = 50  # Maksimum tespit sayısı
    
    # İnsan takip ayarları - İyileştirilmiş
    PERSON_TIMEOUT = 3.0  # saniye - daha kısa timeout
    MIN_CONFIDENCE = 0.3  # minimum güven skoru
    TRACKING_THRESHOLD = 30  # piksel - daha hassas takip
    SIZE_THRESHOLD = 0.4  # boyut farkı toleransı
    
    # Performans optimizasyonları
    PROCESS_EVERY_N_FRAMES = 3  # Ekran yakalama için daha yavaş işleme
    SKIP_FRAMES_FOR_TRACKING = 1  # Takip için frame atlama
    
    # Endpoint ayarları
    ENDPOINT_URL = os.getenv('ENDPOINT_URL', 'http://localhost:8000/api/count')
    ENDPOINT_API_KEY = os.getenv('ENDPOINT_API_KEY', '')
    ENDPOINT_TIMEOUT = 30  # saniye
    
    # Zamanlama ayarları
    HOURLY_RESET = True  # Saatlik sıfırlama aktif mi?
    RESET_HOUR = 0  # Hangi saatte sıfırlanacak (0-23)
    
    # Veri kaydetme ayarları
    DATA_DIR = 'data/daily_counts'
    LOG_DIR = 'logs'
    
    # Debug ayarları
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    SAVE_FRAMES = False  # Debug için frame kaydetme
    
    # GPU kullanımı
    USE_GPU = os.getenv('USE_GPU', 'False').lower() == 'true'
    DEVICE = 'cuda' if USE_GPU else 'cpu' 