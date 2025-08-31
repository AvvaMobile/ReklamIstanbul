#!/usr/bin/env python3
"""
RTSP Kamera Basit Test Script'i
rtsp://192.168.1.100:554/H.264/media.smp URL'i ile test
"""

import cv2
import time
from network_camera import RTSPCamera
from config import Config

def test_rtsp_camera():
    """RTSP kamera testi"""
    print("🎯 RTSP Kamera Testi")
    print("=" * 40)
    print(f"📡 URL: {Config.RTSP_URL}")
    print(f"🔌 IP: {Config.RTSP_IP}:{Config.RTSP_PORT}")
    print(f"🎬 Encoding: {Config.RTSP_ENCODING}")
    print("=" * 40)
    
    # RTSP kamera oluştur
    camera = RTSPCamera()
    
    print("\n🔗 Bağlantı testi...")
    if camera.connect():
        print("✅ RTSP bağlantısı başarılı!")
        
        # Frame okuma testi
        print("\n📸 Frame okuma testi...")
        for i in range(5):
            ret, frame = camera.read()
            if ret and frame is not None:
                print(f"   Frame {i+1}: ✅ {frame.shape}")
                
                # İlk frame'i kaydet
                if i == 0:
                    cv2.imwrite("test_frame.jpg", frame)
                    print("   💾 İlk frame kaydedildi: test_frame.jpg")
            else:
                print(f"   Frame {i+1}: ❌ Okunamadı")
            
            time.sleep(0.5)
        
        # Kamera bilgileri
        info = camera.get_camera_info()
        print(f"\n📊 Kamera Bilgileri:")
        print(f"   - Bağlı: {info['connected']}")
        print(f"   - Tür: {info['type']}")
        if info['connected']:
            print(f"   - Çözünürlük: {info['width']}x{info['height']}")
            print(f"   - FPS: {info['fps']}")
        
        camera.release()
        print("\n✅ Test tamamlandı!")
        
    else:
        print("❌ RTSP bağlantısı başarısız!")
        camera.release()
        print("\n💡 Kontrol edilecek noktalar:")
        print("   - IP adresi doğru mu? (192.168.1.100)")
        print("   - Port 554 açık mı?")
        print("   - Kamera çalışıyor mu?")
        print("   - Ağ bağlantısı var mı?")

if __name__ == "__main__":
    test_rtsp_camera()
