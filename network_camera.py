#!/usr/bin/env python3
"""
Network Kamera Desteği
Switch üzerinden bağlı kameralar için RTSP/HTTP stream desteği
"""

import cv2
import requests
import numpy as np
import time
import threading
from urllib.parse import urlparse
import logging
from config import Config

class NetworkCamera:
    def __init__(self, camera_url, camera_type='auto', username=None, password=None):
        """
        Network kamera sınıfı
        
        Args:
            camera_url: Kamera URL'i (rtsp://, http://, ip adresi)
            camera_type: Kamera türü ('rtsp', 'http', 'ip', 'auto')
            username: Kamera kullanıcı adı (opsiyonel)
            password: Kamera şifresi (opsiyonel)
        """
        self.camera_url = camera_url
        self.camera_type = camera_type
        self.username = username
        self.password = password
        self.is_running = False
        self.current_frame = None
        self.frame_lock = threading.Lock()
        self.logger = logging.getLogger(__name__)
        
        # Kamera türünü otomatik tespit et
        if camera_type == 'auto':
            self.camera_type = self._detect_camera_type(camera_url)
        
        # Kamera bağlantısı
        self.cap = None
        self.last_frame_time = 0
        self.frame_interval = 1.0 / 30  # 30 FPS
        
        self.logger.info(f"Network kamera başlatıldı: {camera_url} ({self.camera_type})")
    
    def _detect_camera_type(self, url):
        """Kamera türünü URL'den otomatik tespit eder"""
        parsed = urlparse(url)
        
        if parsed.scheme == 'rtsp':
            return 'rtsp'
        elif parsed.scheme in ['http', 'https']:
            return 'http'
        elif parsed.scheme == 'ip':
            return 'ip'
        else:
            # IP adresi olarak kabul et
            return 'ip'
    
    def _build_camera_url(self):
        """Kamera URL'ini oluşturur (kimlik doğrulama dahil)"""
        if self.camera_type == 'rtsp':
            if self.username and self.password:
                # RTSP with authentication: rtsp://user:pass@ip:port/stream
                parsed = urlparse(self.camera_url)
                return f"rtsp://{self.username}:{self.password}@{parsed.netloc}{parsed.path}"
            else:
                return self.camera_url
        
        elif self.camera_type == 'http':
            if self.username and self.password:
                # HTTP with authentication
                parsed = urlparse(self.camera_url)
                return f"http://{self.username}:{self.password}@{parsed.netloc}{parsed.path}"
            else:
                return self.camera_url
        
        elif self.camera_type == 'ip':
            # IP kamera için standart URL formatları
            if not self.camera_url.startswith(('http://', 'https://', 'rtsp://')):
                # IP adresi olarak verilmiş, standart formatlara çevir
                ip = self.camera_url
                return f"rtsp://{ip}:554/stream1"  # Varsayılan RTSP port
            
            return self.camera_url
        
        return self.camera_url
    
    def connect(self):
        """Kameraya bağlanır"""
        try:
            camera_url = self._build_camera_url()
            self.logger.info(f"Kameraya bağlanılıyor: {camera_url}")
            
            if self.camera_type == 'rtsp':
                # RTSP stream için OpenCV
                self.cap = cv2.VideoCapture(camera_url)
                
                # RTSP buffer ayarları
                self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                self.cap.set(cv2.CAP_PROP_FPS, 30)
                
            elif self.camera_type == 'http':
                # HTTP stream için OpenCV
                self.cap = cv2.VideoCapture(camera_url)
                
            elif self.camera_type == 'ip':
                # IP kamera için standart bağlantı
                self.cap = cv2.VideoCapture(camera_url)
            
            if self.cap and self.cap.isOpened():
                self.logger.info("Kamera bağlantısı başarılı!")
                return True
            else:
                self.logger.error("Kamera bağlantısı başarısız!")
                return False
                
        except Exception as e:
            self.logger.error(f"Kamera bağlantı hatası: {e}")
            return False
    
    def start_capture(self):
        """Kamera yakalamayı başlatır"""
        if not self.connect():
            return False
        
        self.is_running = True
        self.capture_thread = threading.Thread(target=self._capture_loop)
        self.capture_thread.daemon = True
        self.capture_thread.start()
        
        self.logger.info("Network kamera yakalama başlatıldı")
        return True
    
    def stop_capture(self):
        """Kamera yakalamayı durdurur"""
        self.is_running = False
        
        if hasattr(self, 'capture_thread'):
            self.capture_thread.join()
        
        if self.cap:
            self.cap.release()
        
        self.logger.info("Network kamera yakalama durduruldu")
    
    def _capture_loop(self):
        """Sürekli frame yakalama döngüsü"""
        while self.is_running:
            try:
                if self.cap and self.cap.isOpened():
                    ret, frame = self.cap.read()
                    
                    if ret:
                        # Frame'i güncelle
                        with self.frame_lock:
                            self.current_frame = frame
                            self.last_frame_time = time.time()
                    else:
                        # Frame okunamadı, yeniden bağlan
                        self.logger.warning("Frame okunamadı, yeniden bağlanılıyor...")
                        self._reconnect()
                
                # FPS kontrolü
                time.sleep(self.frame_interval)
                
            except Exception as e:
                self.logger.error(f"Frame yakalama hatası: {e}")
                time.sleep(1)
                self._reconnect()
    
    def _reconnect(self):
        """Kameraya yeniden bağlanır"""
        try:
            if self.cap:
                self.cap.release()
            
            time.sleep(2)  # 2 saniye bekle
            self.connect()
            
        except Exception as e:
            self.logger.error(f"Yeniden bağlanma hatası: {e}")
    
    def read(self):
        """
        En son frame'i döndürür (OpenCV VideoCapture uyumlu)
        
        Returns:
            tuple: (success, frame)
        """
        with self.frame_lock:
            if self.current_frame is not None:
                return True, self.current_frame.copy()
            else:
                return False, None
    
    def get_frame(self):
        """En son frame'i döndürür"""
        with self.frame_lock:
            return self.current_frame.copy() if self.current_frame is not None else None
    
    def get_camera_info(self):
        """Kamera bilgilerini döndürür"""
        if self.cap and self.cap.isOpened():
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            
            return {
                'url': self.camera_url,
                'type': self.camera_type,
                'width': width,
                'height': height,
                'fps': fps,
                'connected': True
            }
        else:
            return {
                'url': self.camera_url,
                'type': self.camera_type,
                'connected': False
            }

class NetworkCameraManager:
    """Çoklu network kamera yöneticisi"""
    
    def __init__(self):
        self.cameras = {}
        self.logger = logging.getLogger(__name__)
    
    def add_camera(self, camera_id, camera_url, camera_type='auto', username=None, password=None):
        """Kamera ekler"""
        camera = NetworkCamera(camera_url, camera_type, username, password)
        self.cameras[camera_id] = camera
        self.logger.info(f"Kamera {camera_id} eklendi: {camera_url}")
        return camera
    
    def start_camera(self, camera_id):
        """Kamerayı başlatır"""
        if camera_id in self.cameras:
            return self.cameras[camera_id].start_capture()
        return False
    
    def stop_camera(self, camera_id):
        """Kamerayı durdurur"""
        if camera_id in self.cameras:
            self.cameras[camera_id].stop_capture()
    
    def start_all(self):
        """Tüm kameraları başlatır"""
        for camera_id in self.cameras:
            self.start_camera(camera_id)
    
    def stop_all(self):
        """Tüm kameraları durdurur"""
        for camera_id in self.cameras:
            self.stop_camera(camera_id)
    
    def get_camera(self, camera_id):
        """Belirli kamerayı döndürür"""
        return self.cameras.get(camera_id)
    
    def get_all_cameras(self):
        """Tüm kameraları döndürür"""
        return self.cameras

def test_network_camera():
    """Network kamera testi"""
    print("🌐 Network Kamera Testi")
    print("=" * 40)
    
    # Test kamera URL'leri
    test_urls = [
        "192.168.1.100",  # IP kamera
        "rtsp://192.168.1.100:554/stream1",  # RTSP
        "http://192.168.1.100:8080/video",  # HTTP
    ]
    
    for i, url in enumerate(test_urls):
        print(f"\nTest {i+1}: {url}")
        
        camera = NetworkCamera(url)
        if camera.connect():
            print(f"✅ Bağlantı başarılı")
            info = camera.get_camera_info()
            print(f"   - Tür: {info['type']}")
            print(f"   - Bağlı: {info['connected']}")
            camera.stop_capture()
        else:
            print(f"❌ Bağlantı başarısız")
    
    print("\nTest tamamlandı!")

if __name__ == "__main__":
    test_network_camera()
