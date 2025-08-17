#!/usr/bin/env python3
"""
Windows için özel konfigürasyon
Kamera backend ve DirectShow ayarları ile optimize edilmiş
"""

import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

class ConfigWindows:
    # Kamera ayarları - Windows için optimize edilmiş
    CAMERA_INDEX = 0  # Varsayılan kamera
    FRAME_WIDTH = 480  # Frame boyutu (performans için)
    FRAME_HEIGHT = 360  # Frame boyutu (performans için)
    
    # Windows kamera backend ayarları
    CAMERA_BACKEND = 'CAP_DSHOW'  # DirectShow (Windows için optimize)
    CAMERA_BUFFER_SIZE = 1  # Buffer boyutu (performans için)
    
    # Ekran yakalama ayarları
    USE_SCREEN_CAPTURE = False  # Windows'ta kamera kullan (önerilen)
    SCREEN_CAPTURE_FPS = 25
    SCREEN_REGION = None
    SCREEN_MONITOR = 0
    
    # İnsan tespit ayarları - Windows için optimize edilmiş
    DETECTION_THRESHOLD = 0.4
    MODEL_PATH = 'yolov8n.pt'  # Hızlı model (Windows için)
    
    # Model performans ayarları - Windows için optimize edilmiş
    MODEL_CONFIDENCE = 0.5
    MODEL_IOU_THRESHOLD = 0.4
    MODEL_MAX_DET = 20
    
    # İnsan takip ayarları
    PERSON_TIMEOUT = 3.0
    MIN_CONFIDENCE = 0.3
    TRACKING_THRESHOLD = 30
    SIZE_THRESHOLD = 0.4
    
    # Performans optimizasyonları - Windows için
    PROCESS_EVERY_N_FRAMES = 1
    SKIP_FRAMES_FOR_TRACKING = 1
    
    # Endpoint ayarları
    ENDPOINT_URL = os.getenv('ENDPOINT_URL', 'http://localhost:8000/api/count')
    ENDPOINT_API_KEY = os.getenv('ENDPOINT_API_KEY', '')
    ENDPOINT_TIMEOUT = 30
    
    # Zamanlama ayarları
    HOURLY_RESET = True
    RESET_HOUR = 0
    
    # Veri kaydetme ayarları
    DATA_DIR = 'data/daily_counts'
    LOG_DIR = 'logs'
    
    # Debug ayarları
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    SAVE_FRAMES = False
    
    # GPU kullanımı - Windows için
    USE_GPU = os.getenv('USE_GPU', 'False').lower() == 'true'
    DEVICE = 'cuda' if USE_GPU else 'cpu'
    
    # Windows özel ayarları
    WINDOWS_CAMERA_PERMISSIONS = True  # Kamera izinlerini kontrol et
    USE_DIRECTSHOW = True  # DirectShow backend kullan
    CAMERA_TIMEOUT = 5000  # Kamera açılma timeout (ms)
    
    @classmethod
    def get_camera_backend(cls):
        """Kamera backend'ini döndürür"""
        import cv2
        if cls.USE_DIRECTSHOW:
            return cv2.CAP_DSHOW
        else:
            return cv2.CAP_ANY
    
    @classmethod
    def check_windows_camera_permissions(cls):
        """Windows kamera izinlerini kontrol eder"""
        if not cls.WINDOWS_CAMERA_PERMISSIONS:
            return True
            
        print("🔍 Windows Kamera İzinleri Kontrol Ediliyor...")
        print("1. Windows Ayarlar > Gizlilik ve Güvenlik > Kamera")
        print("   - 'Kamera erişimine izin ver' açık olmalı")
        print("   - 'Uygulamaların kameraya erişmesine izin ver' açık olmalı")
        print("2. Python uygulamasına kamera izni verildi mi?")
        
        return True

# Windows için özel config instance'ı
Config = ConfigWindows
