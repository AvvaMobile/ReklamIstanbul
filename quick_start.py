#!/usr/bin/env python3
"""
RTSP Kamera ile İnsan Sayma Sistemi - Hızlı Başlangıç
"""

import cv2
import time
import signal
import sys
from datetime import datetime
from human_detector import HumanDetector
from counter import HumanCounter
from config import Config
from network_camera import RTSPCamera
import logging

# Global değişkenler
counter = None
running = True
rtsp_camera = None

def signal_handler(sig, frame):
    """Program kapatılırken verileri kaydet"""
    global running, rtsp_camera
    print('\nProgram kapatılıyor...')
    running = False
    
    if rtsp_camera:
        rtsp_camera.stop_capture()
        print("RTSP kamera durduruldu")
    
    if counter:
        counter.save_daily_count()
    sys.exit(0)

def setup_logging():
    """Logging ayarlarını yapılandırır"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def main():
    """Ana fonksiyon"""
    global counter, running, rtsp_camera
    
    # Sinyal handler'ı ayarla
    signal.signal(signal.SIGINT, signal_handler)
    
    # Logging ayarları
    logger = setup_logging()
    
    print("🚀 RTSP Kamera ile İnsan Sayma Sistemi")
    print("=" * 50)
    print(f"🎯 RTSP URL: {Config.RTSP_URL}")
    print(f"📡 IP: {Config.RTSP_IP}:{Config.RTSP_PORT}")
    print(f"🎬 Encoding: {Config.RTSP_ENCODING}")
    print("=" * 50)
    
    # RTSP kamera başlat
    logger.info("RTSP kamera başlatılıyor...")
    rtsp_camera = RTSPCamera()
    
    if not rtsp_camera.connect():
        logger.error("❌ RTSP kamera bağlantısı başarısız!")
        return
    
    logger.info("✅ RTSP kamera bağlantısı başarılı!")
    
    # Kamera yakalamayı başlat
    if not rtsp_camera.start_capture():
        logger.error("❌ RTSP kamera yakalama başlatılamadı!")
        return
    
    logger.info("✅ RTSP kamera yakalama başlatıldı")
    
    # Modülleri başlat
    detector = HumanDetector()
    counter = HumanCounter(
        device_id=Config.DEVICE_ID,
        location=Config.LOCATION
    )
    
    logger.info("✅ İnsan sayma sistemi başlatıldı")
    logger.info("Çıkmak için 'q' tuşuna basın veya Ctrl+C")
    
    frame_count = 0
    start_time = time.time()
    fps_start_time = time.time()
    fps_frame_count = 0
    current_fps = 0
    
    # Önceki tespitleri sakla (tracking için)
    previous_detections = []
    
    while running:
        # RTSP kamera'dan frame al
        ret, frame = rtsp_camera.read()
        if not ret:
            logger.warning("RTSP kamera'dan frame alınamıyor!")
            time.sleep(0.1)
            continue
        
        if frame is None:
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
        
        # İnsanları tespit et - Tracking ile
        detections = detector.detect_humans_with_tracking(frame, previous_detections)
        previous_detections = detections.copy()
        
        # Tespit edilen insanları çiz
        frame = detector.draw_detections(frame, detections)
        
        # İnsanları say
        frame, hourly_count, daily_count = counter.count_humans(detections, frame)
        
        # Bilgileri ekrana yaz
        cv2.putText(frame, f'Saatlik Sayim: {hourly_count}', 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.putText(frame, f'Gunluk Sayim: {daily_count}', 
                   (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        cv2.putText(frame, f'Toplam Sayim: {counter.total_count}', 
                   (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        # FPS bilgisi
        cv2.putText(frame, f'FPS: {current_fps:.1f}', 
                   (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # RTSP kamera bilgisi
        cv2.putText(frame, f'RTSP: {Config.RTSP_IP}:{Config.RTSP_PORT}', 
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
        window_title = 'Human Counter - RTSP Camera'
        cv2.imshow(window_title, frame)
        
        # 'q' tuşuna basılırsa çık
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # Kısa bir bekleme
        time.sleep(0.01)
    
    # Temizlik
    if rtsp_camera:
        rtsp_camera.stop_capture()
    
    cv2.destroyAllWindows()
    
    if counter:
        counter.save_daily_count()
        logger.info("Program kapatıldı ve veriler kaydedildi.")

if __name__ == "__main__":
    main()
