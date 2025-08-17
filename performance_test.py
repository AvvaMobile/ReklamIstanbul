#!/usr/bin/env python3
"""
Performans test dosyası - İnsan sayma sisteminin performansını test eder
"""

import cv2
import time
import numpy as np
from human_detector import HumanDetector
from counter import HumanCounter
from config import Config
import logging

def setup_logging():
    """Logging ayarlarını yapılandırır"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def test_detection_performance():
    """Tespit performansını test eder"""
    logger = setup_logging()
    logger.info("Tespit performans testi başlatılıyor...")
    
    # Test görüntüsü oluştur - Config'deki boyutları kullan
    test_frame = np.random.randint(0, 255, (Config.FRAME_HEIGHT, Config.FRAME_WIDTH, 3), dtype=np.uint8)
    
    # Detector'ı başlat
    detector = HumanDetector()
    
    # Performans testi
    num_tests = 100
    start_time = time.time()
    
    for i in range(num_tests):
        detections = detector.detect_humans(test_frame)
        if i % 10 == 0:
            logger.info(f"Test {i}/{num_tests} - Detections: {len(detections)}")
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / num_tests
    
    logger.info(f"Tespit performans testi tamamlandı:")
    logger.info(f"Toplam süre: {total_time:.2f} saniye")
    logger.info(f"Ortalama süre: {avg_time:.4f} saniye/frame")
    logger.info(f"FPS: {1/avg_time:.1f}")
    logger.info(f"Model: {Config.MODEL_PATH}")
    logger.info(f"Frame boyutu: {Config.FRAME_WIDTH}x{Config.FRAME_HEIGHT}")
    
    return avg_time

def test_counter_performance():
    """Sayaç performansını test eder"""
    logger = setup_logging()
    logger.info("Sayaç performans testi başlatılıyor...")
    
    # Test görüntüsü oluştur
    test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    # Counter'ı başlat
    counter = HumanCounter()
    
    # Test detections
    test_detections = [
        {'bbox': (100, 100, 200, 300), 'confidence': 0.8},
        {'bbox': (300, 150, 400, 350), 'confidence': 0.7},
        {'bbox': (500, 200, 600, 400), 'confidence': 0.9}
    ]
    
    # Performans testi
    num_tests = 1000
    start_time = time.time()
    
    for i in range(num_tests):
        frame, hourly, daily = counter.count_humans(test_detections, test_frame.copy())
        if i % 100 == 0:
            logger.info(f"Test {i}/{num_tests} - Hourly: {hourly}, Daily: {daily}")
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / num_tests
    
    logger.info(f"Sayaç performans testi tamamlandı:")
    logger.info(f"Toplam süre: {total_time:.2f} saniye")
    logger.info(f"Ortalama süre: {avg_time:.6f} saniye/frame")
    logger.info(f"FPS: {1/avg_time:.1f}")
    
    return avg_time

def test_memory_usage():
    """Bellek kullanımını test eder"""
    logger = setup_logging()
    logger.info("Bellek kullanım testi başlatılıyor...")
    
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Test nesneleri oluştur
    detector = HumanDetector()
    counter = HumanCounter()
    
    # Bellek kullanımını ölç
    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_usage = final_memory - initial_memory
    
    logger.info(f"Bellek kullanım testi tamamlandı:")
    logger.info(f"Başlangıç bellek: {initial_memory:.1f} MB")
    logger.info(f"Son bellek: {final_memory:.1f} MB")
    logger.info(f"Kullanılan bellek: {memory_usage:.1f} MB")
    
    return memory_usage

def test_camera_performance():
    """Kamera performansını test eder"""
    logger = setup_logging()
    logger.info("Kamera performans testi başlatılıyor...")
    
    # Kamera başlat
    cap = cv2.VideoCapture(Config.CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.FRAME_HEIGHT)
    
    if not cap.isOpened():
        logger.error("Kamera açılamadı!")
        return None
    
    # Performans testi
    num_frames = 100
    start_time = time.time()
    
    for i in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            logger.error(f"Frame {i} okunamadı!")
            break
        
        if i % 10 == 0:
            logger.info(f"Frame {i}/{num_frames}")
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / num_frames
    
    cap.release()
    
    logger.info(f"Kamera performans testi tamamlandı:")
    logger.info(f"Toplam süre: {total_time:.2f} saniye")
    logger.info(f"Ortalama süre: {avg_time:.4f} saniye/frame")
    logger.info(f"FPS: {1/avg_time:.1f}")
    
    return avg_time

def test_screen_capture_performance():
    """Ekran yakalama performansını test eder"""
    logger = setup_logging()
    logger.info("Ekran yakalama performans testi başlatılıyor...")
    
    try:
        from screen_capture import ScreenCapture
        
        # Ekran yakalama başlat
        capture = ScreenCapture()
        capture.start_capture()
        
        # Test süresi
        test_duration = 10  # 10 saniye
        frame_count = 0
        start_time = time.time()
        
        while time.time() - start_time < test_duration:
            ret, frame = capture.read()
            if ret:
                frame_count += 1
            time.sleep(0.001)  # 1ms sleep
        
        capture.stop_capture()
        
        actual_fps = frame_count / test_duration
        target_fps = Config.SCREEN_CAPTURE_FPS
        
        logger.info(f"Ekran yakalama performans testi tamamlandı:")
        logger.info(f"Hedef FPS: {target_fps}")
        logger.info(f"Gerçek FPS: {actual_fps:.1f}")
        logger.info(f"Frame sayısı: {frame_count}")
        logger.info(f"Test süresi: {test_duration} saniye")
        
        return actual_fps
        
    except ImportError:
        logger.warning("Screen capture modülü bulunamadı, test atlandı")
        return 0

def compare_performance():
    """Farklı konfigürasyonlarda performans karşılaştırması"""
    logger = setup_logging()
    logger.info("Performans karşılaştırma testi başlatılıyor...")
    
    # Mevcut konfigürasyon
    logger.info("=== MEVCUT KONFİGÜRASYON ===")
    logger.info(f"Model: {Config.MODEL_PATH}")
    logger.info(f"Frame boyutu: {Config.FRAME_WIDTH}x{Config.FRAME_HEIGHT}")
    logger.info(f"Ekran yakalama FPS: {Config.SCREEN_CAPTURE_FPS}")
    logger.info(f"Frame işleme: Her {Config.PROCESS_EVERY_N_FRAMES} frame'den 1'i")
    
    # Tespit performansı
    detection_time = test_detection_performance()
    
    # Ekran yakalama performansı
    capture_fps = test_screen_capture_performance()
    
    # Toplam performans hesaplama
    if Config.USE_SCREEN_CAPTURE:
        effective_fps = capture_fps / Config.PROCESS_EVERY_N_FRAMES
        logger.info(f"=== PERFORMANS SONUÇLARI ===")
        logger.info(f"Ekran yakalama FPS: {capture_fps:.1f}")
        logger.info(f"İşlenen frame FPS: {effective_fps:.1f}")
        logger.info(f"Tespit süresi: {detection_time:.4f} saniye/frame")
        logger.info(f"Toplam gecikme: {detection_time + (1/effective_fps):.4f} saniye")
    else:
        logger.info("Kamera modu - ekran yakalama testi atlandı")
    
    return {
        'detection_time': detection_time,
        'capture_fps': capture_fps,
        'effective_fps': capture_fps / Config.PROCESS_EVERY_N_FRAMES if Config.USE_SCREEN_CAPTURE else 0
    }

if __name__ == "__main__":
    # Ana performans testi
    print("🚀 AvvaImageAI Performans Testi Başlatılıyor...")
    print("=" * 50)
    
    results = compare_performance()
    
    print("\n" + "=" * 50)
    print("📊 TEST SONUÇLARI:")
    print(f"Tespit süresi: {results['detection_time']:.4f} saniye/frame")
    print(f"Ekran yakalama FPS: {results['capture_fps']:.1f}")
    if results['effective_fps'] > 0:
        print(f"Etkili FPS: {results['effective_fps']:.1f}")
    
    print("\n✅ Test tamamlandı!") 