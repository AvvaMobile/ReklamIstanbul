import os
from dotenv import load_dotenv
import torch

# .env dosyasını yükle
load_dotenv()

class Config:
    # Kamera ayarları - Frame boyutunu küçült (performans için)
    CAMERA_INDEX = 1  # Varsayılan kamera
    FRAME_WIDTH = 480  # 640'dan 480'e düşür (performans için)
    FRAME_HEIGHT = 360  # 480'den 360'a düşür (performans için)
    
    # Ekran yakalama ayarları - FPS'i artır
    USE_SCREEN_CAPTURE = True  # Ekran yakalama modunu aktif et
    SCREEN_CAPTURE_FPS = 25  # 10'dan 25'e çıkar (performans için)
    SCREEN_REGION = None  # Belirli bölge (x, y, width, height) veya None (tüm ekran)
    SCREEN_MONITOR = 0  # Monitör seçimi (0, 1, 2...)
    
    # İnsan tespit ayarları - Daha hızlı model
    DETECTION_THRESHOLD = 0.4  # Daha düşük eşik değeri
    MODEL_PATH = 'yolov8n.pt'  # yolov8s.pt yerine (daha hızlı)
    
    # Model performans ayarları - Daha hızlı
    MODEL_CONFIDENCE = 0.5  # 0.4'ten 0.5'e çıkar (daha az false positive)
    MODEL_IOU_THRESHOLD = 0.4  # 0.5'ten 0.4'e düşür (daha hızlı)
    MODEL_MAX_DET = 20  # 50'den 20'ye düşür (daha hızlı)
    
    # İnsan takip ayarları - İyileştirilmiş
    PERSON_TIMEOUT = 3.0  # saniye - daha kısa timeout
    MIN_CONFIDENCE = 0.3  # minimum güven skoru
    TRACKING_THRESHOLD = 30  # piksel - daha hassas takip
    SIZE_THRESHOLD = 0.4  # boyut farkı toleransı
    
    # Performans optimizasyonları - Frame işleme sıklığını artır
    PROCESS_EVERY_N_FRAMES = 1  # 3'ten 1'e düşür (her frame işlensin)
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
    
    # Debug ayarları - MVP için kapat
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    SAVE_FRAMES = False  # Debug için frame kaydetme (MVP için kapalı)
    
    # GPU kullanımı - macOS için CPU varsayılan
    USE_GPU = os.getenv('USE_GPU', 'False').lower() == 'true'  # macOS için False
    DEVICE = 'cuda' if USE_GPU and torch.cuda.is_available() else 'cpu'
    
    # Network Kamera Desteği - Switch üzerinden bağlı kameralar
    USE_NETWORK_CAMERAS = os.getenv('USE_NETWORK_CAMERAS', 'False').lower() == 'true'
    NETWORK_CAMERAS = {
        'camera_1': {
            'url': os.getenv('CAMERA_1_URL', '192.168.1.121'),  # Sizin kamera IP'niz
            'type': os.getenv('CAMERA_1_TYPE', 'sunaapi'),  # 'rtsp', 'http', 'ip', 'auto', 'sunaapi'
            'username': os.getenv('CAMERA_1_USERNAME', None),
            'password': os.getenv('CAMERA_1_PASSWORD', None),
            'enabled': True
        },
        'camera_2': {
            'url': os.getenv('CAMERA_2_URL', '192.168.1.101'),
            'type': os.getenv('CAMERA_2_TYPE', 'auto'),
            'username': os.getenv('CAMERA_2_USERNAME', None),
            'password': os.getenv('CAMERA_2_PASSWORD', None),
            'enabled': False
        }
    }
    
    # SUNAPI Kamera Desteği - SUNAPI dokümantasyonuna göre
    USE_SUNAPI_CAMERAS = os.getenv('USE_SUNAPI_CAMERAS', 'True').lower() == 'true'
    SUNAPI_CAMERAS = {
        'sunaapi_camera_1': {
            'ip': os.getenv('SUNAPI_CAMERA_1_IP', '192.168.1.121'),
            'port': int(os.getenv('SUNAPI_CAMERA_1_PORT', '554')),
            'channel_id': int(os.getenv('SUNAPI_CAMERA_1_CHANNEL', '0')),
            'profile_id': int(os.getenv('SUNAPI_CAMERA_1_PROFILE', '1')),
            'encoding': os.getenv('SUNAPI_CAMERA_1_ENCODING', 'h264'),
            'username': os.getenv('SUNAPI_CAMERA_1_USERNAME', None),
            'password': os.getenv('SUNAPI_CAMERA_1_PASSWORD', None),
            'enabled': True
        }
    }
    
    # Network kamera performans ayarları
    NETWORK_CAMERA_FPS = 30
    NETWORK_CAMERA_BUFFER_SIZE = 1
    NETWORK_CAMERA_TIMEOUT = 5000  # ms
    NETWORK_CAMERA_RECONNECT_INTERVAL = 5  # saniye 