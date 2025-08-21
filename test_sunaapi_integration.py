#!/usr/bin/env python3
"""
SUNAPI Kamera Entegrasyon Testi
Ana sisteme SUNAPI kamera desteğinin entegrasyonunu test eder
"""

import sys
import os
import time
from config import Config
from network_camera import SUNAPICamera, NetworkCamera

def test_sunaapi_config():
    """SUNAPI konfigürasyon testi"""
    print("🔧 SUNAPI Konfigürasyon Testi")
    print("=" * 50)
    
    print(f"USE_SUNAPI_CAMERAS: {Config.USE_SUNAPI_CAMERAS}")
    
    if hasattr(Config, 'SUNAPI_CAMERAS'):
        print(f"SUNAPI Kamera Sayısı: {len(Config.SUNAPI_CAMERAS)}")
        
        for camera_id, camera_config in Config.SUNAPI_CAMERAS.items():
            print(f"\n📹 {camera_id}:")
            print(f"   IP: {camera_config['ip']}")
            print(f"   Port: {camera_config['port']}")
            print(f"   Kanal: {camera_config['channel_id']}")
            print(f"   Profil: {camera_config['profile_id']}")
            print(f"   Encoding: {camera_config['encoding']}")
            print(f"   Aktif: {camera_config['enabled']}")
    else:
        print("❌ SUNAPI_CAMERAS konfigürasyonu bulunamadı!")
    
    return True

def test_sunaapi_camera_creation():
    """SUNAPI kamera oluşturma testi"""
    print("\n🔨 SUNAPI Kamera Oluşturma Testi")
    print("=" * 50)
    
    try:
        # Test kamera oluştur
        camera = SUNAPICamera(
            ip_address="192.168.1.121",
            port=554,
            channel_id=0,
            profile_id=1,
            encoding="h264"
        )
        
        print("✅ SUNAPI kamera başarıyla oluşturuldu")
        print(f"   IP: {camera.ip_address}")
        print(f"   Port: {camera.port}")
        print(f"   Kanal: {camera.channel_id}")
        print(f"   Profil: {camera.profile_id}")
        print(f"   Encoding: {camera.encoding}")
        
        # URL formatlarını test et
        print("\n🔗 URL Format Testleri:")
        test_formats = ['profile', 'live_channel', 'multicast']
        for fmt in test_formats:
            url = camera.get_rtsp_url(fmt)
            print(f"   {fmt:15}: {url}")
        
        return camera
        
    except Exception as e:
        print(f"❌ SUNAPI kamera oluşturma hatası: {e}")
        return None

def test_network_camera_sunaapi_mode():
    """NetworkCamera SUNAPI mod testi"""
    print("\n🌐 NetworkCamera SUNAPI Mod Testi")
    print("=" * 50)
    
    try:
        camera = NetworkCamera(
            camera_url="192.168.1.121",
            camera_type="sunaapi"
        )
        
        print("✅ NetworkCamera SUNAPI mod başarıyla oluşturuldu")
        print(f"   Kamera türü: {camera.camera_type}")
        print(f"   SUNAPI mod aktif: {camera.sunaapi_camera is not None}")
        
        if camera.sunaapi_camera:
            print(f"   SUNAPI IP: {camera.sunaapi_camera.ip_address}")
            print(f"   SUNAPI Port: {camera.sunaapi_camera.port}")
        
        return camera
        
    except Exception as e:
        print(f"❌ NetworkCamera SUNAPI mod hatası: {e}")
        return None

def test_sunaapi_formats():
    """SUNAPI format testi"""
    print("\n📹 SUNAPI Format Testi")
    print("=" * 50)
    
    camera = SUNAPICamera("192.168.1.121")
    
    print("🔍 Tüm formatlar test ediliyor...")
    results = camera.test_all_formats()
    
    print("\n📊 Test Sonuçları:")
    for format_name, result in results.items():
        status_icon = "✅" if result['working'] else "❌"
        print(f"   {status_icon} {format_name:20}: {result['status']}")
        if result['working']:
            print(f"      URL: {result['url']}")
    
    return results

def test_sunaapi_connection_simulation():
    """SUNAPI bağlantı simülasyonu (gerçek bağlantı olmadan)"""
    print("\n🎭 SUNAPI Bağlantı Simülasyonu")
    print("=" * 50)
    
    camera = SUNAPICamera("192.168.1.121")
    
    print("🔗 Bağlantı simülasyonu...")
    print("   (Gerçek kamera olmadığı için sadece URL'ler oluşturuluyor)")
    
    # Farklı formatlarda URL'ler oluştur
    formats_to_test = [
        ('profile', {}),
        ('live_channel', {'chid': 0}),
        ('multicast', {'encoding': 'h264'}),
        ('channel_profile', {'chid': 0, 'profile': 1}),
        ('basic', {'encoding': 'h264'})
    ]
    
    for format_type, params in formats_to_test:
        url = camera.get_rtsp_url(format_type, **params)
        print(f"   {format_type:20}: {url}")
    
    print("\n✅ Simülasyon tamamlandı!")
    print("💡 Gerçek kamera ile test etmek için bu URL'leri kullanabilirsiniz")

def main():
    """Ana test fonksiyonu"""
    print("🚀 SUNAPI Kamera Entegrasyon Testi")
    print("=" * 60)
    
    try:
        # 1. Konfigürasyon testi
        test_sunaapi_config()
        
        # 2. Kamera oluşturma testi
        camera = test_sunaapi_camera_creation()
        
        # 3. NetworkCamera SUNAPI mod testi
        network_camera = test_network_camera_sunaapi_mode()
        
        # 4. Format testi (simülasyon)
        test_sunaapi_formats()
        
        # 5. Bağlantı simülasyonu
        test_sunaapi_connection_simulation()
        
        print("\n" + "=" * 60)
        print("✅ Tüm testler başarıyla tamamlandı!")
        print("\n📋 Sonraki Adımlar:")
        print("   1. Gerçek kamera IP adresini config.py'de güncelleyin")
        print("   2. Kamera kimlik bilgilerini env_example.txt'de ayarlayın")
        print("   3. test_sunaapi_camera.py ile gerçek bağlantıyı test edin")
        print("   4. main.py ile ana sistemi SUNAPI kamera ile çalıştırın")
        
    except Exception as e:
        print(f"\n❌ Test hatası: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
