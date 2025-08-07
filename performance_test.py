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
    
    # Test görüntüsü oluştur
    test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
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

def run_all_tests():
    """Tüm performans testlerini çalıştırır"""
    logger = setup_logging()
    logger.info("Tüm performans testleri başlatılıyor...")
    
    results = {}
    
    # Tespit performans testi
    try:
        results['detection_time'] = test_detection_performance()
    except Exception as e:
        logger.error(f"Tespit testi başarısız: {e}")
        results['detection_time'] = None
    
    # Sayaç performans testi
    try:
        results['counter_time'] = test_counter_performance()
    except Exception as e:
        logger.error(f"Sayaç testi başarısız: {e}")
        results['counter_time'] = None
    
    # Bellek kullanım testi
    try:
        results['memory_usage'] = test_memory_usage()
    except Exception as e:
        logger.error(f"Bellek testi başarısız: {e}")
        results['memory_usage'] = None
    
    # Kamera performans testi
    try:
        results['camera_time'] = test_camera_performance()
    except Exception as e:
        logger.error(f"Kamera testi başarısız: {e}")
        results['camera_time'] = None
    
    # Sonuçları raporla
    logger.info("=== PERFORMANS TEST SONUÇLARI ===")
    for test_name, result in results.items():
        if result is not None:
            logger.info(f"{test_name}: {result}")
        else:
            logger.info(f"{test_name}: BAŞARISIZ")
    
    return results

if __name__ == "__main__":
    run_all_tests() 