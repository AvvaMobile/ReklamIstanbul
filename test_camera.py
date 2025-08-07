#!/usr/bin/env python3
"""
Kamera test scripti - Kamera erişimini test etmek için
"""

import cv2
import time
import subprocess
import platform
from config import Config

def get_system_cameras():
    """
    Sistem üzerindeki kameraları tespit eder
    """
    print("🔍 Sistem kameraları tespit ediliyor...")
    
    if platform.system() == "Darwin":  # macOS
        return get_macos_cameras()
    elif platform.system() == "Linux":
        return get_linux_cameras()
    elif platform.system() == "Windows":
        return get_windows_cameras()
    else:
        print("Desteklenmeyen işletim sistemi")
        return []

def get_macos_cameras():
    """
    macOS'ta kameraları tespit eder
    """
    try:
        # system_profiler ile kamera bilgilerini al
        result = subprocess.run(['system_profiler', 'SPCameraDataType'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("📹 macOS Kamera Bilgileri:")
            print(result.stdout)
        else:
            print("Kamera bilgileri alınamadı")
            
    except Exception as e:
        print(f"macOS kamera tespiti hatası: {e}")
    
    return []

def get_linux_cameras():
    """
    Linux'ta kameraları tespit eder
    """
    try:
        # /dev/video* dosyalarını listele
        result = subprocess.run(['ls', '/dev/video*'], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            cameras = result.stdout.strip().split('\n')
            print("📹 Linux Kamera Dosyaları:")
            for camera in cameras:
                if camera:
                    print(f"  {camera}")
            return cameras
        else:
            print("Linux kamera dosyaları bulunamadı")
            
    except Exception as e:
        print(f"Linux kamera tespiti hatası: {e}")
    
    return []

def get_windows_cameras():
    """
    Windows'ta kameraları tespit eder
    """
    try:
        # PowerShell ile kamera bilgilerini al
        cmd = "Get-WmiObject Win32_PnPEntity | Where-Object {$_.Name -like '*camera*' -or $_.Name -like '*webcam*'} | Select-Object Name, DeviceID"
        result = subprocess.run(['powershell', '-Command', cmd], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("📹 Windows Kamera Bilgileri:")
            print(result.stdout)
        else:
            print("Windows kamera bilgileri alınamadı")
            
    except Exception as e:
        print(f"Windows kamera tespiti hatası: {e}")
    
    return []

def list_all_cameras():
    """
    Mevcut tüm kameraları listeler ve test eder
    """
    print("\n🔍 Mevcut kameralar kontrol ediliyor...")
    
    available_cameras = []
    
    # Daha geniş bir aralık kontrol et (0-10)
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Kamera özelliklerini al
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                
                camera_info = {
                    'index': i,
                    'width': width,
                    'height': height,
                    'fps': fps,
                    'frame_shape': frame.shape
                }
                
                available_cameras.append(camera_info)
                
                print(f"✅ Kamera {i}: Çalışıyor")
                print(f"   - Çözünürlük: {width}x{height}")
                print(f"   - FPS: {fps:.1f}")
                print(f"   - Frame boyutu: {frame.shape}")
                print()
            else:
                print(f"⚠️  Kamera {i}: Açıldı ama frame okunamıyor")
            cap.release()
        else:
            print(f"❌ Kamera {i}: Erişilemiyor")
    
    return available_cameras

def test_specific_camera(camera_index):
    """
    Belirli bir kamerayı test eder
    """
    print(f"\n📹 Kamera {camera_index} test ediliyor...")
    
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"❌ Kamera {camera_index} açılamadı!")
        return False
    
    # Kamera ayarlarını yap
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.FRAME_HEIGHT)
    
    print(f"✅ Kamera {camera_index} başarıyla açıldı")
    
    # Birkaç frame oku ve test et
    for i in range(5):
        ret, frame = cap.read()
        if ret:
            print(f"✅ Frame {i+1} okundu - Boyut: {frame.shape}")
        else:
            print(f"❌ Frame {i+1} okunamadı")
            cap.release()
            return False
        
        time.sleep(0.5)
    
    cap.release()
    print(f"✅ Kamera {camera_index} test başarılı!")
    return True

def show_camera_preview(camera_index, duration=5):
    """
    Kameranın önizlemesini gösterir
    """
    print(f"\n📹 Kamera {camera_index} önizlemesi ({duration} saniye)...")
    
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"❌ Kamera {camera_index} açılamadı!")
        return False
    
    start_time = time.time()
    
    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if ret:
            # Frame boyutunu ayarla
            frame = cv2.resize(frame, (640, 480))
            
            # Kamera bilgilerini frame üzerine yaz
            cv2.putText(frame, f'Camera {camera_index}', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Press Q to exit', (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow(f'Camera {camera_index} Preview', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Frame okunamadı")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Önizleme tamamlandı")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("KAMERA TEST VE TESPİT SİSTEMİ")
    print("=" * 60)
    
    # Sistem kameralarını tespit et
    system_cameras = get_system_cameras()
    
    # Tüm kameraları listele ve test et
    available_cameras = list_all_cameras()
    
    if available_cameras:
        print(f"\n📊 Toplam {len(available_cameras)} kamera bulundu:")
        for camera in available_cameras:
            print(f"  - Kamera {camera['index']}: {camera['width']}x{camera['height']} @ {camera['fps']:.1f}fps")
        
        # Ana kamera testi
        print("\n" + "=" * 40)
        print("ANA KAMERA TESTİ")
        print("=" * 40)
        
        success = test_specific_camera(Config.CAMERA_INDEX)
        
        # Önizleme seçeneği
        if success:
            print("\n" + "=" * 40)
            print("ÖNİZLEME SEÇENEKLERİ")
            print("=" * 40)
            
            for camera in available_cameras:
                choice = input(f"Kamera {camera['index']} önizlemesini görmek ister misiniz? (y/n): ")
                if choice.lower() == 'y':
                    show_camera_preview(camera['index'])
                    break
        
        print("\n" + "=" * 60)
        if success:
            print("✅ Kamera testi başarılı!")
            print("Ana program çalıştırılabilir.")
        else:
            print("❌ Kamera testi başarısız!")
            print("Lütfen kamera ayarlarını kontrol edin.")
    else:
        print("\n❌ Hiçbir kamera bulunamadı!")
        print("Lütfen kamera bağlantısını kontrol edin.")
    
    print("=" * 60) 