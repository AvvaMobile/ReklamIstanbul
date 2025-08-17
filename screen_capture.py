#!/usr/bin/env python3
"""
Ekran görüntüsü alma modülü - Kamera yerine ekran görüntüsü kullanmak için
"""

import cv2
import numpy as np
import time
import threading
from PIL import ImageGrab
import logging
from config import Config

class ScreenCapture:
    def __init__(self, monitor=None, region=None):
        """
        Ekran görüntüsü alma sınıfı
        
        Args:
            monitor: Monitör seçimi (0, 1, 2...)
            region: Belirli bölge (x, y, width, height)
        """
        self.monitor = monitor
        self.region = region
        self.is_running = False
        self.current_frame = None
        self.frame_lock = threading.Lock()
        self.logger = logging.getLogger(__name__)
        
        # Ekran boyutlarını al
        if region:
            self.width, self.height = region[2], region[3]
        else:
            # Tüm ekranı al
            screen = ImageGrab.grab()
            self.width, self.height = screen.size
        
        self.logger.info(f"Ekran yakalama başlatıldı: {self.width}x{self.height}")
    
    def start_capture(self):
        """Ekran yakalamayı başlatır"""
        self.is_running = True
        self.capture_thread = threading.Thread(target=self._capture_loop)
        self.capture_thread.daemon = True
        self.capture_thread.start()
        self.logger.info("Ekran yakalama başlatıldı")
    
    def stop_capture(self):
        """Ekran yakalamayı durdurur"""
        self.is_running = False
        if hasattr(self, 'capture_thread'):
            self.capture_thread.join()
        self.logger.info("Ekran yakalama durduruldu")
    
    def _capture_loop(self):
        """Sürekli ekran yakalama döngüsü - Optimize edilmiş"""
        last_capture_time = time.time()
        target_interval = 1.0 / Config.SCREEN_CAPTURE_FPS
        
        while self.is_running:
            current_time = time.time()
            
            # FPS kontrolü - time.sleep yerine daha verimli
            if current_time - last_capture_time >= target_interval:
                try:
                    # Ekran görüntüsü al
                    if self.region:
                        screenshot = ImageGrab.grab(bbox=self.region)
                    else:
                        screenshot = ImageGrab.grab()
                    
                    # PIL'den OpenCV formatına dönüştür
                    frame = np.array(screenshot)
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    
                    # Frame'i güncelle
                    with self.frame_lock:
                        self.current_frame = frame
                    
                    last_capture_time = current_time
                    
                except Exception as e:
                    self.logger.error(f"Ekran yakalama hatası: {e}")
            
            # CPU kullanımını azalt - 1ms sleep
            time.sleep(0.001)
    
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
    
    def get_screen_info(self):
        """Ekran bilgilerini döndürür"""
        return {
            'width': self.width,
            'height': self.height,
            'monitor': self.monitor,
            'region': self.region,
            'fps': Config.SCREEN_CAPTURE_FPS
        }

class MultiMonitorCapture:
    """Çoklu monitör desteği"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.captures = {}
    
    def add_monitor(self, monitor_id, region=None):
        """Monitör ekler"""
        capture = ScreenCapture(monitor=monitor_id, region=region)
        self.captures[monitor_id] = capture
        self.logger.info(f"Monitör {monitor_id} eklendi")
        return capture
    
    def start_all(self):
        """Tüm monitörleri başlatır"""
        for monitor_id, capture in self.captures.items():
            capture.start_capture()
        self.logger.info(f"{len(self.captures)} monitör başlatıldı")
    
    def stop_all(self):
        """Tüm monitörleri durdurur"""
        for capture in self.captures.values():
            capture.stop_capture()
        self.logger.info("Tüm monitörler durduruldu")
    
    def get_frame(self, monitor_id=0):
        """Belirli monitörün frame'ini alır"""
        if monitor_id in self.captures:
            return self.captures[monitor_id].get_frame()
        return None

def test_screen_capture():
    """Ekran yakalama testi"""
    import cv2
    
    print("Ekran yakalama testi başlatılıyor...")
    
    # Ekran yakalama başlat
    capture = ScreenCapture()
    capture.start_capture()
    
    # 5 saniye test et
    start_time = time.time()
    frame_count = 0
    
    while time.time() - start_time < 5:
        ret, frame = capture.read()
        if ret:
            frame_count += 1
            
            # Frame'i göster
            cv2.imshow('Screen Capture Test', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    capture.stop_capture()
    cv2.destroyAllWindows()
    
    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time
    
    print(f"Test tamamlandı:")
    print(f"Frame sayısı: {frame_count}")
    print(f"Süre: {elapsed_time:.2f} saniye")
    print(f"FPS: {fps:.1f}")

if __name__ == "__main__":
    test_screen_capture() 