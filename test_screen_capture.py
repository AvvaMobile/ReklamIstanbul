#!/usr/bin/env python3
"""
Ekran yakalama test dosyası
"""

import cv2
import numpy as np
from PIL import ImageGrab
import time
import os

def test_basic_screen_capture():
    """Temel ekran yakalama testi"""
    print("Temel ekran yakalama testi başlatılıyor...")
    
    try:
        # Ekran görüntüsü al
        screenshot = ImageGrab.grab()
        print(f"Ekran boyutu: {screenshot.size}")
        
        # PIL'den OpenCV formatına dönüştür
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        print(f"Frame boyutu: {frame.shape}")
        print("Ekran yakalama başarılı!")
        
        # Frame'i göster
        cv2.imshow('Screen Capture Test', frame)
        cv2.waitKey(3000)  # 3 saniye bekle
        cv2.destroyAllWindows()
        
        return True
        
    except Exception as e:
        print(f"Ekran yakalama hatası: {e}")
        return False

def test_region_capture():
    """Belirli bölge yakalama testi"""
    print("Bölge yakalama testi başlatılıyor...")
    
    try:
        # Ekranın sol üst köşesinden 400x300 piksel al
        region = (0, 0, 400, 300)
        screenshot = ImageGrab.grab(bbox=region)
        
        # PIL'den OpenCV formatına dönüştür
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        print(f"Bölge boyutu: {frame.shape}")
        print("Bölge yakalama başarılı!")
        
        # Frame'i göster
        cv2.imshow('Region Capture Test', frame)
        cv2.waitKey(3000)  # 3 saniye bekle
        cv2.destroyAllWindows()
        
        return True
        
    except Exception as e:
        print(f"Bölge yakalama hatası: {e}")
        return False

def test_performance():
    """Performans testi"""
    print("Performans testi başlatılıyor...")
    
    num_frames = 10
    start_time = time.time()
    
    for i in range(num_frames):
        screenshot = ImageGrab.grab()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        if i % 2 == 0:
            print(f"Frame {i+1}/{num_frames}")
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / num_frames
    fps = 1 / avg_time if avg_time > 0 else 0
    
    print(f"Performans testi tamamlandı:")
    print(f"Toplam süre: {total_time:.2f} saniye")
    print(f"Ortalama süre: {avg_time:.4f} saniye/frame")
    print(f"FPS: {fps:.1f}")
    
    return fps

def check_permissions():
    """İzinleri kontrol et"""
    print("İzin kontrolü...")
    
    # macOS'ta ekran kaydı izni kontrolü
    if os.name == 'posix':  # macOS/Linux
        print("macOS/Linux sistem tespit edildi")
        print("Ekran yakalama için 'Sistem Tercihleri > Güvenlik ve Gizlilik > Ekran Kaydı' izni gerekebilir")
    
    return True

def main():
    """Ana test fonksiyonu"""
    print("=== EKRAN YAKALAMA TESTİ ===")
    
    # İzin kontrolü
    check_permissions()
    print()
    
    # Temel test
    print("1. Temel ekran yakalama testi:")
    basic_success = test_basic_screen_capture()
    print()
    
    # Bölge testi
    print("2. Bölge yakalama testi:")
    region_success = test_region_capture()
    print()
    
    # Performans testi
    print("3. Performans testi:")
    fps = test_performance()
    print()
    
    # Sonuçlar
    print("=== TEST SONUÇLARI ===")
    print(f"Temel yakalama: {'✓ Başarılı' if basic_success else '✗ Başarısız'}")
    print(f"Bölge yakalama: {'✓ Başarılı' if region_success else '✗ Başarısız'}")
    print(f"Performans FPS: {fps:.1f}")
    
    if basic_success and region_success:
        print("\n✓ Tüm testler başarılı! Ekran yakalama kullanılabilir.")
    else:
        print("\n✗ Bazı testler başarısız. İzinleri kontrol edin.")

if __name__ == "__main__":
    main() 