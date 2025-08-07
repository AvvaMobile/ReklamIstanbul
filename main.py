import cv2
import time
import signal
import sys
import threading
from datetime import datetime
from human_detector import HumanDetector
from counter import HumanCounter
from config import Config
import logging

# Ekran yakalama modülünü import et
try:
    from screen_capture import ScreenCapture
    SCREEN_CAPTURE_AVAILABLE = True
except ImportError:
    SCREEN_CAPTURE_AVAILABLE = False
    print("Uyarı: screen_capture modülü bulunamadı. Ekran yakalama özelliği devre dışı.")

# Global değişkenler
counter = None
running = True
screen_capture = None

def signal_handler(sig, frame):
    """
    Program kapatılırken verileri kaydet
    """
    global running, screen_capture
    print('\nProgram kapatılıyor...')
    running = False
    
    # Ekran yakalamayı durdur
    if screen_capture:
        screen_capture.stop_capture()
    
    if counter:
        counter.save_daily_count()
    sys.exit(0)

def setup_logging():
    """
    Logging ayarlarını yapılandırır
    """
    os.makedirs(Config.LOG_DIR, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'{Config.LOG_DIR}/main.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def test_camera(camera_index):
    """
    Kameranın çalışıp çalışmadığını test eder
    """
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        return False
    
    ret, frame = cap.read()
    cap.release()
    return ret

def setup_video_source(logger):
    """
    Video kaynağını ayarlar (kamera veya ekran yakalama)
    """
    if Config.USE_SCREEN_CAPTURE and SCREEN_CAPTURE_AVAILABLE:
        # Ekran yakalama kullan
        global screen_capture
        screen_capture = ScreenCapture(
            monitor=Config.SCREEN_MONITOR,
            region=Config.SCREEN_REGION
        )
        screen_capture.start_capture()
        
        # İlk frame'i bekle
        time.sleep(1)
        
        logger.info("Ekran yakalama başlatıldı")
        return screen_capture
    else:
        # Kamera kullan
        if not test_camera(Config.CAMERA_INDEX):
            logger.error(f"Kamera {Config.CAMERA_INDEX} açılamadı!")
            return None
        
        cap = cv2.VideoCapture(Config.CAMERA_INDEX)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.FRAME_HEIGHT)
        cap.set(cv2.CAP_PROP_FPS, 30)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        if not cap.isOpened():
            logger.error("Kamera açılamadı!")
            return None
        
        logger.info("Kamera başlatıldı")
        return cap

def main():
    global counter, running, screen_capture
    
    # Sinyal handler'ı ayarla
    signal.signal(signal.SIGINT, signal_handler)
    
    # Logging ayarları
    logger = setup_logging()
    
    # Video kaynağını ayarla
    video_source = setup_video_source(logger)
    if video_source is None:
        logger.error("Video kaynağı başlatılamadı!")
        return
    
    # Modülleri başlat
    detector = HumanDetector()
    counter = HumanCounter(
        device_id=Config.DEVICE_ID if hasattr(Config, 'DEVICE_ID') else 'default',
        location=Config.LOCATION if hasattr(Config, 'LOCATION') else 'unknown'
    )
    
    # Endpoint bağlantısını test et
    if counter.endpoint_client.test_connection():
        logger.info("Endpoint bağlantısı başarılı")
    else:
        logger.warning("Endpoint bağlantısı başarısız - veriler sadece yerel olarak kaydedilecek")
    
    # Video kaynağı bilgilerini logla
    if Config.USE_SCREEN_CAPTURE:
        logger.info("İnsan sayma sistemi başlatıldı (Ekran yakalama modu)")
        screen_info = screen_capture.get_screen_info()
        logger.info(f"Ekran boyutu: {screen_info['width']}x{screen_info['height']}")
        logger.info(f"Ekran FPS: {screen_info['fps']}")
    else:
        logger.info("İnsan sayma sistemi başlatıldı (Kamera modu)")
    
    logger.info("Çıkmak için 'q' tuşuna basın.")
    logger.info(f"Saatlik sıfırlama: {'Aktif' if Config.HOURLY_RESET else 'Pasif'}")
    logger.info(f"GPU Kullanımı: {'Aktif' if Config.USE_GPU else 'Pasif'}")
    logger.info(f"Model: {Config.MODEL_PATH}")
    
    frame_count = 0
    start_time = time.time()
    fps_start_time = time.time()
    fps_frame_count = 0
    current_fps = 0
    
    # Önceki tespitleri sakla (tracking için)
    previous_detections = []
    
    while running:
        # Frame oku
        if Config.USE_SCREEN_CAPTURE:
            ret, frame = video_source.read()
        else:
            ret, frame = video_source.read()
        
        if not ret:
            logger.error("Frame okunamadı!")
            break
        
        frame_count += 1
        fps_frame_count += 1
        
        # FPS hesaplama
        if fps_frame_count % 30 == 0:
            current_time = time.time()
            elapsed_time = current_time - fps_start_time
            current_fps = fps_frame_count / elapsed_time
            fps_start_time = current_time
            fps_frame_count = 0
            logger.debug(f"FPS: {current_fps:.2f}")
        
        # İnsanları tespit et - Tracking ile
        detections = detector.detect_humans_with_tracking(frame, previous_detections)
        previous_detections = detections.copy()
        
        # Tespit edilen insanları çiz
        frame = detector.draw_detections(frame, detections)
        
        # İnsanları say
        frame, hourly_count, daily_count = counter.count_humans(detections, frame)
        
        # Bilgileri ekrana yaz - İyileştirilmiş
        cv2.putText(frame, f'Saatlik Sayim: {hourly_count}', 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.putText(frame, f'Gunluk Sayim: {daily_count}', 
                   (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        cv2.putText(frame, f'Toplam Sayim: {counter.total_count}', 
                   (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        # FPS bilgisi
        cv2.putText(frame, f'FPS: {current_fps:.1f}', 
                   (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Video kaynağı bilgisi
        source_info = "Ekran Yakalama" if Config.USE_SCREEN_CAPTURE else "Kamera"
        cv2.putText(frame, f'Kaynak: {source_info}', 
                   (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Tarih ve saat bilgisini ekle
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cv2.putText(frame, current_time, 
                   (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Debug bilgileri
        if Config.DEBUG:
            cv2.putText(frame, f'Detections: {len(detections)}', 
                       (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            cv2.putText(frame, f'Active People: {len(counter.active_people)}', 
                       (10, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        
        # Frame'i göster
        window_title = 'Human Counter - Screen Capture' if Config.USE_SCREEN_CAPTURE else 'Human Counter - Camera'
        cv2.imshow(window_title, frame)
        
        # 'q' tuşuna basılırsa çık
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # Kısa bir bekleme (CPU kullanımını azaltmak için)
        time.sleep(0.01)
    
    # Temizlik
    if Config.USE_SCREEN_CAPTURE and screen_capture:
        screen_capture.stop_capture()
    else:
        video_source.release()
    
    cv2.destroyAllWindows()
    
    if counter:
        counter.save_daily_count()
        logger.info("Program kapatıldı ve veriler kaydedildi.")

if __name__ == "__main__":
    import os
    main() 