#!/usr/bin/env python3
"""
SUNAPI Kamera Test Script'i
SUNAPI dokümantasyonuna göre RTSP stream formatlarını test eder
"""

import cv2
import time
import sys
from network_camera import SUNAPICamera, NetworkCamera

def test_sunaapi_formats(ip_address, username=None, password=None):
    """SUNAPI kamera formatlarını test eder"""
    print(f"🔍 SUNAPI Kamera Testi: {ip_address}")
    print("=" * 60)
    
    # SUNAPI kamera oluştur
    camera = SUNAPICamera(
        ip_address=ip_address,
        username=username,
        password=password
    )
    
    # Tüm formatları test et
    print("📹 SUNAPI Format Testleri:")
    print("-" * 40)
    
    results = camera.test_all_formats()
    
    for format_name, result in results.items():
        print(f"{format_name:20}: {result['status']}")
        if result['working']:
            print(f"{'':20}  URL: {result['url']}")
    
    return results

def test_sunaapi_connection(ip_address, format_type='profile', username=None, password=None):
    """Belirli bir SUNAPI formatında bağlantı testi"""
    print(f"\n🔗 SUNAPI Bağlantı Testi: {ip_address}")
    print(f"Format: {format_type}")
    print("=" * 50)
    
    camera = SUNAPICamera(
        ip_address=ip_address,
        username=username,
        password=password
    )
    
    # Bağlantı testi
    if camera.connect(format_type):
        print("✅ Bağlantı başarılı!")
        
        # Frame okuma testi
        print("📸 Frame okuma testi...")
        for i in range(5):  # 5 frame test et
            ret, frame = camera.read_frame()
            if ret:
                print(f"   Frame {i+1}: ✅ {frame.shape}")
            else:
                print(f"   Frame {i+1}: ❌ Okunamadı")
            time.sleep(0.5)
        
        camera.release()
        return True
    else:
        print("❌ Bağlantı başarısız!")
        camera.release()
        return False

def test_network_camera_sunaapi_mode(ip_address, username=None, password=None):
    """NetworkCamera sınıfının SUNAPI modunu test eder"""
    print(f"\n🌐 NetworkCamera SUNAPI Mod Testi: {ip_address}")
    print("=" * 60)
    
    # SUNAPI modunda kamera oluştur
    camera = NetworkCamera(
        camera_url=ip_address,
        camera_type='sunaapi',
        username=username,
        password=password
    )
    
    # Bağlantı testi
    if camera.connect():
        print("✅ SUNAPI mod bağlantısı başarılı!")
        
        # Kamera bilgileri
        info = camera.get_camera_info()
        print(f"   - Tür: {info['type']}")
        print(f"   - Bağlı: {info['connected']}")
        
        # Frame okuma testi
        print("📸 Frame okuma testi...")
        for i in range(3):
            ret, frame = camera.read()
            if ret:
                print(f"   Frame {i+1}: ✅ {frame.shape}")
            else:
                print(f"   Frame {i+1}: ❌ Okunamadı")
            time.sleep(0.5)
        
        camera.stop_capture()
        return True
    else:
        print("❌ SUNAPI mod bağlantısı başarısız!")
        camera.stop_capture()
        return False

def interactive_sunaapi_test(ip_address, username=None, password=None):
    """İnteraktif SUNAPI test"""
    print(f"\n🎮 İnteraktif SUNAPI Test: {ip_address}")
    print("=" * 50)
    
    while True:
        print("\nSeçenekler:")
        print("1. Tüm formatları test et")
        print("2. Profil formatında bağlan")
        print("3. Live Channel formatında bağlan")
        print("4. Multicast formatında bağlan")
        print("5. NetworkCamera SUNAPI mod testi")
        print("6. Çıkış")
        
        choice = input("\nSeçiminiz (1-6): ").strip()
        
        if choice == '1':
            test_sunaapi_formats(ip_address, username, password)
        
        elif choice == '2':
            test_sunaapi_connection(ip_address, 'profile', username, password)
        
        elif choice == '3':
            test_sunaapi_connection(ip_address, 'live_channel', username, password)
        
        elif choice == '4':
            test_sunaapi_connection(ip_address, 'multicast', username, password)
        
        elif choice == '5':
            test_network_camera_sunaapi_mode(ip_address, username, password)
        
        elif choice == '6':
            print("👋 Test sonlandırılıyor...")
            break
        
        else:
            print("❌ Geçersiz seçim!")

def main():
    """Ana fonksiyon"""
    print("🚀 SUNAPI Kamera Test Sistemi")
    print("=" * 60)
    
    # Kamera bilgileri
    ip_address = input("Kamera IP adresi (varsayılan: 192.168.1.121): ").strip()
    if not ip_address:
        ip_address = "192.168.1.121"
    
    username = input("Kullanıcı adı (opsiyonel): ").strip()
    if not username:
        username = None
    
    password = input("Şifre (opsiyonel): ").strip()
    if not password:
        password = None
    
    print(f"\n📡 Test edilecek kamera: {ip_address}")
    if username:
        print(f"👤 Kullanıcı: {username}")
    
    # Test seçenekleri
    print("\nTest türü:")
    print("1. Hızlı test (tüm formatlar)")
    print("2. İnteraktif test")
    
    test_choice = input("Seçiminiz (1-2): ").strip()
    
    if test_choice == '1':
        # Hızlı test
        test_sunaapi_formats(ip_address, username, password)
        test_network_camera_sunaapi_mode(ip_address, username, password)
    
    elif test_choice == '2':
        # İnteraktif test
        interactive_sunaapi_test(ip_address, username, password)
    
    else:
        print("❌ Geçersiz seçim! Hızlı test başlatılıyor...")
        test_sunaapi_formats(ip_address, username, password)
        test_network_camera_sunaapi_mode(ip_address, username, password)
    
    print("\n✅ Test tamamlandı!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Test kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n❌ Test hatası: {e}")
        import traceback
        traceback.print_exc()
