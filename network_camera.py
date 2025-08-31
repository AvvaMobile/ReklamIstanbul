#!/usr/bin/env python3
"""
RTSP Kamera Desteği
rtsp://192.168.1.100:554/H.264/media.smp URL'i ile kamera görüntüsü okuma
"""

import cv2
import time
import threading
import logging
from config import Config

class RTSPCamera:
    """
    RTSP Kamera sınıfı - Sabit URL ile
    """
    
    def __init__(self):
        """RTSP kamera başlatır"""
        self.rtsp_url = Config.RTSP_URL
        self.is_running = False
        self.current_frame = None
        self.frame_lock = threading.Lock()
        self.logger = logging.getLogger(__name__)
        
        # Kamera bağlantısı
        self.cap = None
        self.last_frame_time = 0
        self.frame_interval = 1.0 / Config.CAMERA_FPS
        
        self.logger.info(f"RTSP kamera başlatıldı: {self.rtsp_url}")
    
    def connect(self):
        """RTSP kameraya bağlanır"""
        try:
            self.logger.info(f"RTSP kameraya bağlanılıyor: {self.rtsp_url}")
            
            # RTSP stream için OpenCV
            self.cap = cv2.VideoCapture(self.rtsp_url)
            
            # RTSP buffer ayarları
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, Config.CAMERA_BUFFER_SIZE)
            self.cap.set(cv2.CAP_PROP_FPS, Config.CAMERA_FPS)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.FRAME_WIDTH)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.FRAME_HEIGHT)
            
            if self.cap and self.cap.isOpened():
                self.logger.info("✅ RTSP kamera bağlantısı başarılı!")
                return True
            else:
                self.logger.error("❌ RTSP kamera bağlantısı başarısız!")
                return False
                
        except Exception as e:
            self.logger.error(f"RTSP kamera bağlantı hatası: {e}")
            return False
    
    def start_capture(self):
        """Kamera yakalamayı başlatır"""
        if not self.connect():
            return False
        
        self.is_running = True
        self.capture_thread = threading.Thread(target=self._capture_loop)
        self.capture_thread.daemon = True
        self.capture_thread.start()
        
        self.logger.info("RTSP kamera yakalama başlatıldı")
        return True
    
    def stop_capture(self):
        """Kamera yakalamayı durdurur"""
        self.is_running = False
        
        if hasattr(self, 'capture_thread'):
            self.capture_thread.join()
        
        if self.cap:
            self.cap.release()
        
        self.logger.info("RTSP kamera yakalama durduruldu")
    
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
            
            time.sleep(Config.CAMERA_RECONNECT_INTERVAL)
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
                'url': self.rtsp_url,
                'type': 'rtsp',
                'width': width,
                'height': height,
                'fps': fps,
                'connected': True
            }
        else:
            return {
                'url': self.rtsp_url,
                'type': 'rtsp',
                'connected': False
            }
    
    def release(self):
        """Kamera bağlantısını kapatır"""
        self.stop_capture()

def test_rtsp_camera():
    """RTSP kamera testi"""
    print("🌐 RTSP Kamera Testi")
    print("=" * 40)
    
    rtsp_url = Config.RTSP_URL
    print(f"Test edilen URL: {rtsp_url}")
    
    camera = RTSPCamera()
    
    if camera.connect():
        print("✅ RTSP bağlantısı başarılı")
        
        # Frame okuma testi
        print("📸 Frame okuma testi...")
        for i in range(3):
            ret, frame = camera.read()
            if ret:
                print(f"   Frame {i+1}: ✅ {frame.shape}")
            else:
                print(f"   Frame {i+1}: ❌ Okunamadı")
            time.sleep(0.5)
        
        camera.release()
    else:
        print("❌ RTSP bağlantısı başarısız")
        camera.release()
    
    print("\nTest tamamlandı!")

if __name__ == "__main__":
    test_rtsp_camera()
