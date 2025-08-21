#!/usr/bin/env python3
"""
SUNAPI Kamera Demo Script'i
SUNAPI kamera desteğini gösterir
"""

import cv2
import time
from network_camera import SUNAPICamera, NetworkCamera

def demo_sunaapi_camera():
    """SUNAPI kamera demo"""
    print("🚀 SUNAPI Kamera Demo")
    print("=" * 50)
    
    # Kamera bilgileri
    ip_address = "192.168.1.121"  # Test için, gerçek IP ile değiştirin
    username = None  # Gerekirse kullanıcı adı
    password = None  # Gerekirse şifre
    
    print(f"📡 Kamera IP: {ip_address}")
    print(f"👤 Kullanıcı: {username or 'Yok'}")
    print(f"🔒 Şifre: {'***' if password else 'Yok'}")
    
    # 1. SUNAPICamera sınıfı demo
    print("\n1️⃣ SUNAPICamera Sınıfı Demo")
    print("-" * 30)
    
    camera = SUNAPICamera(
        ip_address=ip_address,
        username=username,
        password=password
    )
    
    # Tüm formatları listele
    print("📹 Mevcut SUNAPI Formatları:")
    for format_name, url_template in camera.sunaapi_formats.items():
        print(f"   {format_name}: {url_template}")
    
    # Test URL'leri oluştur
    print("\n🔗 Test URL'leri:")
    test_formats = ['profile', 'live_channel', 'multicast']
    for fmt in test_formats:
        url = camera.get_rtsp_url(fmt)
        print(f"   {fmt}: {url}")
    
    # 2. NetworkCamera SUNAPI mod demo
    print("\n2️⃣ NetworkCamera SUNAPI Mod Demo")
    print("-" * 30)
    
    network_camera = NetworkCamera(
        camera_url=ip_address,
        camera_type='sunaapi',
        username=username,
        password=password
    )
    
    print(f"Kamera türü: {network_camera.camera_type}")
    print(f"SUNAPI mod aktif: {network_camera.sunaapi_camera is not None}")
    
    # 3. Bağlantı testi (opsiyonel)
    print("\n3️⃣ Bağlantı Testi (Opsiyonel)")
    print("-" * 30)
    
    test_connection = input("Bağlantı testi yapmak istiyor musunuz? (y/n): ").strip().lower()
    
    if test_connection == 'y':
        print("🔗 Profile formatında bağlantı testi...")
        
        if camera.connect('profile'):
            print("✅ Bağlantı başarılı!")
            
            # Frame okuma testi
            print("📸 Frame okuma testi...")
            for i in range(3):
                ret, frame = camera.read_frame()
                if ret:
                    print(f"   Frame {i+1}: ✅ {frame.shape}")
                else:
                    print(f"   Frame {i+1}: ❌ Okunamadı")
                time.sleep(0.5)
            
            camera.release()
        else:
            print("❌ Bağlantı başarısız!")
            print("💡 Bu normal olabilir - kamera farklı bir port/format kullanıyor olabilir")
            camera.release()
    
    print("\n✅ Demo tamamlandı!")
    print("\n📋 Kullanım Örnekleri:")
    print("   # SUNAPI kamera oluştur")
    print("   camera = SUNAPICamera('192.168.1.121')")
    print("   ")
    print("   # Farklı formatlarda bağlan")
    print("   camera.connect('profile')      # rtsp://ip:554/profile1/media.smp")
    print("   camera.connect('live_channel') # rtsp://ip:558/LiveChannel/0/media.smp")
    print("   camera.connect('multicast')    # rtsp://ip:554/multicast/h264/media.smp")
    print("   ")
    print("   # NetworkCamera ile SUNAPI mod")
    print("   camera = NetworkCamera('192.168.1.121', camera_type='sunaapi')")

def main():
    """Ana fonksiyon"""
    try:
        demo_sunaapi_camera()
    except KeyboardInterrupt:
        print("\n\n⏹️ Demo kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n❌ Demo hatası: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
