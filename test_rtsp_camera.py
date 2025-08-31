#!/usr/bin/env python3
"""
RTSP Kamera Test Script'i
rtsp://192.168.1.100:554/H.264/media.smp URL'i ile test
"""

import cv2
import time
import sys
from network_camera import SUNAPICamera, NetworkCamera

def test_rtsp_direct():
    """Doğrudan RTSP URL ile test"""
    print("🎯 Doğrudan RTSP URL Testi")
    print("=" * 40)
    
    rtsp_url = "rtsp://192.168.1.100:554/H.264/media.smp"
    print(f"Test edilen URL: {rtsp_url}")
    
    # OpenCV ile doğrudan test
    print("\n📹 OpenCV ile doğrudan test...")
    cap = cv2.VideoCapture(rtsp_url)
    
    if cap.isOpened():
        print("✅ RTSP bağlantısı başarılı!")
        
        # Kamera bilgileri
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        print(f"   📐 Çözünürlük: {width}x{height}")
        print(f"   🎬 FPS: {fps}")
        
        # Frame okuma testi
        print("\n📸 Frame okuma testi...")
        for i in range(5):
            ret, frame = cap.read()
            if ret:
                print(f"   Frame {i+1}: ✅ {frame.shape}")
                
                # İlk frame'i kaydet (opsiyonel)
                if i == 0:
                    cv2.imwrite(f"test_frame_{i+1}.jpg", frame)
                    print(f"   💾 Frame {i+1} kaydedildi: test_frame_{i+1}.jpg")
            else:
                print(f"   Frame {i+1}: ❌ Okunamadı")
            
            time.sleep(0.5)
        
        cap.release()
        print("✅ Test tamamlandı!")
        
    else:
        print("❌ RTSP bağlantısı başarısız!")
        cap.release()

def test_sunaapi_camera():
    """SUNAPI kamera ile test"""
    print("\n🔧 SUNAPI Kamera ile Test")
    print("=" * 40)
    
    # SUNAPI kamera oluştur
    camera = SUNAPICamera(
        ip_address="192.168.1.100",
        port=554,
        encoding="H.264"
    )
    
    print(f"📡 Kamera IP: {camera.ip_address}")
    print(f"🔌 Port: {camera.port}")
    print(f"🎬 Encoding: {camera.encoding}")
    
    # Custom H.264 formatını test et
    print("\n🔗 Custom H.264 formatı testi...")
    custom_url = camera.get_rtsp_url('custom_h264')
    print(f"   URL: {custom_url}")
    
    # Bağlantı testi
    if camera.connect('custom_h264'):
        print("✅ SUNAPI bağlantısı başarılı!")
        
        # Frame okuma testi
        print("\n📸 Frame okuma testi...")
        for i in range(3):
            ret, frame = camera.read_frame()
            if ret:
                print(f"   Frame {i+1}: ✅ {frame.shape}")
            else:
                print(f"   Frame {i+1}: ❌ Okunamadı")
            time.sleep(0.5)
        
        camera.release()
    else:
        print("❌ SUNAPI bağlantısı başarısız!")
        camera.release()

def test_network_camera():
    """NetworkCamera ile test"""
    print("\n🌐 NetworkCamera ile Test")
    print("=" * 40)
    
    # NetworkCamera ile test
    camera = NetworkCamera(
        camera_url="rtsp://192.168.1.100:554/H.264/media.smp",
        camera_type='rtsp'
    )
    
    print(f"📡 Kamera URL: {camera.camera_url}")
    print(f"🔧 Kamera Türü: {camera.camera_type}")
    
    # Bağlantı testi
    if camera.connect():
        print("✅ NetworkCamera bağlantısı başarılı!")
        
        # Frame okuma testi
        print("\n📸 Frame okuma testi...")
        for i in range(3):
            ret, frame = camera.read()
            if ret:
                print(f"   Frame {i+1}: ✅ {frame.shape}")
            else:
                print(f"   Frame {i+1}: ❌ Okunamadı")
            time.sleep(0.5)
        
        camera.stop_capture()
    else:
        print("❌ NetworkCamera bağlantısı başarısız!")
        camera.stop_capture()

def main():
    """Ana fonksiyon"""
    print("🚀 RTSP Kamera Test Script'i")
    print("🎯 Hedef: rtsp://192.168.1.100:554/H.264/media.smp")
    print("=" * 60)
    
    try:
        # 1. Doğrudan RTSP testi
        test_rtsp_direct()
        
        # 2. SUNAPI kamera testi
        test_sunaapi_camera()
        
        # 3. NetworkCamera testi
        test_network_camera()
        
        print("\n✅ Tüm testler tamamlandı!")
        print("\n📋 Sonuçlar:")
        print("   - Doğrudan RTSP: En basit yöntem")
        print("   - SUNAPI Kamera: SUNAPI format desteği")
        print("   - NetworkCamera: Gelişmiş özellikler")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Test kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n❌ Test hatası: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
