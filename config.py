import os
from dotenv import load_dotenv
import torch

# .env dosyasını yükle
load_dotenv()

class Config:
    # RTSP Kamera Ayarları - Sabit URL
    RTSP_URL = "rtsp://192.168.1.100:554/H.264/media.smp"
    RTSP_IP = "192.168.1.100"
    RTSP_PORT = 554
    RTSP_ENCODING = "H.264"
    
    # Kamera performans ayarları
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    CAMERA_FPS = 30
    CAMERA_BUFFER_SIZE = 1
    CAMERA_TIMEOUT = 5000  # ms
    CAMERA_RECONNECT_INTERVAL = 5  # saniye
    
    # İnsan tespit ayarları
    DETECTION_THRESHOLD = 0.4
    MODEL_PATH = 'yolov8n.pt'
    
    # Model performans ayarları
    MODEL_CONFIDENCE = 0.5
    MODEL_IOU_THRESHOLD = 0.4
    MODEL_MAX_DET = 20
    
    # İnsan takip ayarları
    PERSON_TIMEOUT = 3.0  # saniye
    MIN_CONFIDENCE = 0.3
    TRACKING_THRESHOLD = 30  # piksel
    SIZE_THRESHOLD = 0.4
    
    # Performans optimizasyonları
    PROCESS_EVERY_N_FRAMES = 1
    SKIP_FRAMES_FOR_TRACKING = 1
    
    # Endpoint ayarları
    ENDPOINT_URL = os.getenv('ENDPOINT_URL', 'http://localhost:8000/api/count')
    ENDPOINT_API_KEY = os.getenv('ENDPOINT_API_KEY', '')
    ENDPOINT_TIMEOUT = 30  # saniye
    
    # Zamanlama ayarları
    HOURLY_RESET = True
    RESET_HOUR = 0  # Hangi saatte sıfırlanacak (0-23)
    
    # Veri kaydetme ayarları
    DATA_DIR = 'data/daily_counts'
    LOG_DIR = 'logs'
    
    # Debug ayarları
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    SAVE_FRAMES = False
    
    # GPU kullanımı
    USE_GPU = os.getenv('USE_GPU', 'False').lower() == 'true'
    DEVICE = 'cuda' if USE_GPU and torch.cuda.is_available() else 'cpu'
    
    # Cihaz bilgileri
    DEVICE_ID = os.getenv('DEVICE_ID', 'rtsp_camera_001')
    LOCATION = os.getenv('LOCATION', 'RTSP_Camera_Location') 