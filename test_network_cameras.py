#!/usr/bin/env python3
"""
Network Kamera Test Script'i
Switch üzerinden bağlı kameraları test eder
"""

import cv2
import time
import requests
import socket
from network_camera import NetworkCamera, NetworkCameraManager
from config import Config

def test_network_connectivity(ip_address, port=80):
    """Network bağlantısını test eder"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((ip_address, port))
        sock.close()
        return result == 0
    except:
        return False

def test_rtsp_connection(rtsp_url):
    """RTSP bağlantısını test eder"""
    try:
        cap = cv2.VideoCapture(rtsp_url)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            return ret
        return False
    except:
        return False

def test_http_connection(http_url):
    """HTTP bağlantısını test eder"""
    try:
        response = requests.get(http_url, timeout=5)
        return response.status_code == 200
    except:
        return False

def scan_network_cameras(network_range="192.168.1"):
    """Network'ta kamera tarar"""
    print(f"🔍 Network Kamera Taraması: {network_range}.0/24")
    print("=" * 50)
    
    found_cameras = []
    
    for i in range(1, 255):
        ip = f"{network_range}.{i}"
        print(f"Taranan IP: {ip}", end=" ")
        
        # Ping testi
        if test_network_connectivity(ip, 80):
            print("✅ HTTP erişilebilir")
            
            # RTSP testi
            rtsp_url = f"rtsp://{ip}:554/stream1"
            if test_rtsp_connection(rtsp_url):
                print(f"   ✅ RTSP stream bulundu: {rtsp_url}")
                found_cameras.append({
                    'ip': ip,
                    'type': 'rtsp',
                    'url': rtsp_url
                })
            
            # HTTP stream testi
            http_url = f"http://{ip}:8080/video"
            if test_http_connection(http_url):
                print(f"   ✅ HTTP stream bulundu: {http_url}")
                found_cameras.append({
                    'ip': ip,
                    'type': 'http',
                    'url': http_url
                })
            
        else:
            print("❌ Erişilemiyor")
    
    return found_cameras

def test_specific_camera(camera_url, camera_type='auto'):
    """Belirli bir kamerayı test eder"""
    print(f"\n📹 Kamera Testi: {camera_url}")
    print("=" * 40)
    
    camera = NetworkCamera(camera_url, camera_type)
    
    # Bağlantı testi
    if camera.connect():
        print("✅ Bağlantı başarılı")
        
        # Kamera bilgileri
        info = camera.get_camera_info()
        print(f"   - Tür: {info['type']}")
        print(f"   - Çözünürlük: {info.get('width', 'N/A')}x{info.get('height', 'N/A')}")
        print(f"   - FPS: {info.get('fps', 'N/A')}")
        
        # Frame testi
        print("\nFrame testi yapılıyor...")
        camera.start_capture()
        
        for i in range(10):
            ret, frame = camera.read()
            if ret:
                print(f"   ✅ Frame {i+1}: {frame.shape}")
            else:
                print(f"   ❌ Frame {i+1}: Okunamıyor")
            time.sleep(0.1)
        
        camera.stop_capture()
        print("✅ Kamera testi başarılı!")
        return True
        
    else:
        print("❌ Bağlantı başarısız!")
        return False

def test_camera_manager():
    """Kamera yöneticisini test eder"""
    print("\n🎛️  Kamera Yöneticisi Testi")
    print("=" * 40)
    
    manager = NetworkCameraManager()
    
    # Test kameraları ekle
    test_cameras = [
        ('test_1', '192.168.1.100', 'ip'),
        ('test_2', 'rtsp://192.168.1.101:554/stream1', 'rtsp'),
        ('test_3', 'http://192.168.1.102:8080/video', 'http'),
    ]
    
    for camera_id, url, camera_type in test_cameras:
        print(f"\nKamera ekleniyor: {camera_id}")
        camera = manager.add_camera(camera_id, url, camera_type)
        
        if camera.connect():
            print(f"✅ {camera_id} bağlantısı başarılı")
            manager.start_camera(camera_id)
        else:
            print(f"❌ {camera_id} bağlantısı başarısız")
    
    # Tüm kameraları listele
    print(f"\n📋 Toplam {len(manager.get_all_cameras())} kamera:")
    for camera_id, camera in manager.get_all_cameras().items():
        info = camera.get_camera_info()
        status = "🟢 Aktif" if camera.is_running else "🔴 Pasif"
        print(f"   - {camera_id}: {info['url']} ({status})")
    
    # Test sonrası temizlik
    manager.stop_all()
    print("\n✅ Kamera yöneticisi testi tamamlandı!")

def main():
    """Ana fonksiyon"""
    print("🚀 Network Kamera Test Sistemi")
    print("=" * 60)
    print()
    
    # Network tarama
    print("1️⃣ Network Kamera Taraması")
    found_cameras = scan_network_cameras()
    
    if found_cameras:
        print(f"\n🎯 {len(found_cameras)} kamera bulundu:")
        for cam in found_cameras:
            print(f"   - {cam['ip']} ({cam['type']}): {cam['url']}")
        
        # Bulunan kameraları test et
        print("\n2️⃣ Bulunan Kameralar Test Ediliyor")
        for cam in found_cameras[:3]:  # İlk 3'ünü test et
            test_specific_camera(cam['url'], cam['type'])
    else:
        print("\n❌ Hiçbir kamera bulunamadı!")
        print("Manuel test için örnek kamera URL'leri:")
        print("   - IP Kamera: 192.168.1.100")
        print("   - RTSP: rtsp://192.168.1.100:554/stream1")
        print("   - HTTP: http://192.168.1.100:8080/video")
    
    # Kamera yöneticisi testi
    print("\n3️⃣ Kamera Yöneticisi Testi")
    test_camera_manager()
    
    print("\n" + "=" * 60)
    print("🎉 Network kamera testi tamamlandı!")
    print("\n📋 Sonraki adımlar:")
    print("1. .env dosyasında kamera URL'lerini ayarlayın")
    print("2. USE_NETWORK_CAMERAS=True yapın")
    print("3. Ana uygulamayı çalıştırın: python main.py")

if __name__ == "__main__":
    main()
