#!/usr/bin/env python3
"""
Windows Kamera Test Script'i
Windows'ta kamera görünmeme sorunlarını tespit eder
"""

import cv2
import sys
import os

def check_windows_camera_permissions():
    """Windows kamera izinlerini kontrol eder"""
    print("🔍 Windows Kamera İzinleri Kontrolü...")
    print("=" * 50)
    
    print("1. Windows Ayarlar > Gizlilik ve Güvenlik > Kamera")
    print("   - 'Kamera erişimine izin ver' açık olmalı")
    print("   - 'Uygulamaların kameraya erişmesine izin ver' açık olmalı")
    print()
    
    print("2. Python uygulamasına kamera izni verildi mi?")
    print("   - Windows kamera izinlerinde Python'u bulun")
    print("   - Kamera erişimine izin verin")
    print()

def test_camera_backends():
    """Farklı kamera backend'lerini test eder"""
    print("🔧 Kamera Backend Testi...")
    print("=" * 50)
    
    backends = [
        cv2.CAP_ANY,           # Otomatik
        cv2.CAP_DSHOW,         # DirectShow (Windows)
        cv2.CAP_MSMF,          # Media Foundation
        cv2.CAP_GSTREAMER,     # GStreamer
    ]
    
    backend_names = ["Otomatik", "DirectShow", "Media Foundation", "GStreamer"]
    
    for i, backend in enumerate(backends):
        print(f"Backend {i}: {backend_names[i]} ({backend})")
        try:
            cap = cv2.VideoCapture(0, backend)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    print(f"  ✅ Çalışıyor - Frame boyutu: {frame.shape}")
                else:
                    print(f"  ⚠️  Açılıyor ama frame okunamıyor")
                cap.release()
            else:
                print(f"  ❌ Açılamıyor")
        except Exception as e:
            print(f"  ❌ Hata: {e}")
        print()

def test_cameras():
    """Tüm kameraları test eder"""
    print("📹 Kamera Testi...")
    print("=" * 50)
    
    working_cameras = []
    
    for i in range(10):
        print(f"Kamera {i} test ediliyor...")
        
        # Farklı backend'lerle dene
        for backend in [cv2.CAP_ANY, cv2.CAP_DSHOW]:
            try:
                cap = cv2.VideoCapture(i, backend)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        fps = cap.get(cv2.CAP_PROP_FPS)
                        
                        print(f"  ✅ Kamera {i}: Çalışıyor")
                        print(f"     - Backend: {backend}")
                        print(f"     - Çözünürlük: {width}x{height}")
                        print(f"     - FPS: {fps:.1f}")
                        print(f"     - Frame boyutu: {frame.shape}")
                        
                        working_cameras.append({
                            'index': i,
                            'backend': backend,
                            'width': width,
                            'height': height,
                            'fps': fps
                        })
                        
                        cap.release()
                        break
                    else:
                        print(f"  ⚠️  Kamera {i}: Açılıyor ama frame okunamıyor")
                        cap.release()
                else:
                    if backend == cv2.CAP_DSHOW:
                        print(f"  ❌ Kamera {i}: Açılamıyor (DirectShow)")
            except Exception as e:
                if backend == cv2.CAP_DSHOW:
                    print(f"  ❌ Kamera {i}: Hata - {e}")
    
    return working_cameras

def test_specific_camera(camera_index):
    """Belirli bir kamerayı detaylı test eder"""
    print(f"🔍 Kamera {camera_index} Detaylı Test...")
    print("=" * 50)
    
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print(f"❌ Kamera {camera_index} açılamıyor!")
        return False
    
    # Kamera özelliklerini al
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"✅ Kamera {camera_index} özellikleri:")
    print(f"   - Çözünürlük: {width}x{height}")
    print(f"   - FPS: {fps:.1f}")
    
    # Birkaç frame oku
    for i in range(5):
        ret, frame = cap.read()
        if ret:
            print(f"   - Frame {i+1}: {frame.shape}")
        else:
            print(f"   - Frame {i+1}: Okunamıyor")
    
    cap.release()
    return True

def main():
    """Ana fonksiyon"""
    print("🚀 Windows Kamera Test Sistemi")
    print("=" * 60)
    print()
    
    # Windows kamera izinleri kontrolü
    check_windows_camera_permissions()
    
    # Backend testi
    test_camera_backends()
    
    # Kamera testi
    working_cameras = test_cameras()
    
    print("📊 TEST SONUÇLARI")
    print("=" * 30)
    
    if working_cameras:
        print(f"✅ {len(working_cameras)} kamera çalışıyor:")
        for cam in working_cameras:
            print(f"   - Kamera {cam['index']}: {cam['width']}x{cam['height']} @ {cam['fps']:.1f}fps")
        
        print()
        print("🎯 Sonraki adımlar:")
        print("1. Ana uygulamayı çalıştır: python main.py")
        print("2. Web arayüzünü aç: python app.py")
        
        # Çalışan bir kamerayı detaylı test et
        if working_cameras:
            print()
            choice = input(f"Kamera {working_cameras[0]['index']} detaylı test edilsin mi? (y/n): ")
            if choice.lower() == 'y':
                test_specific_camera(working_cameras[0]['index'])
    
    else:
        print("❌ Hiçbir kamera çalışmıyor!")
        print()
        print("🔧 Çözüm önerileri:")
        print("1. Windows kamera izinlerini kontrol edin")
        print("2. Kamera sürücülerini güncelleyin")
        print("3. Bilgisayarı yeniden başlatın")
        print("4. Bu script'i tekrar çalıştırın")
    
    print()
    print("Test tamamlandı!")

if __name__ == "__main__":
    main()
