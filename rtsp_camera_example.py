#!/usr/bin/env python3
"""
RTSP Kamera Örnek Uygulaması
rtsp://192.168.1.100:554/H.264/media.smp URL'i ile basit kamera uygulaması
"""

import cv2
import time
import numpy as np
from network_camera import NetworkCamera

class RTSPCameraApp:
    """RTSP Kamera Uygulaması"""
    
    def __init__(self, rtsp_url):
        """
        RTSP kamera uygulaması başlatır
        
        Args:
            rtsp_url: RTSP URL (örn: rtsp://192.168.1.100:554/H.264/media.smp)
        """
        self.rtsp_url = rtsp_url
        self.camera = None
        self.is_running = False
        
        print(f"🎯 RTSP Kamera Uygulaması başlatılıyor...")
        print(f"📡 URL: {rtsp_url}")
    
    def start(self):
        """Kamerayı başlatır"""
        try:
            # NetworkCamera ile başlat
            self.camera = NetworkCamera(
                camera_url=self.rtsp_url,
                camera_type='rtsp'
            )
            
            if self.camera.connect():
                print("✅ Kamera bağlantısı başarılı!")
                self.is_running = True
                return True
            else:
                print("❌ Kamera bağlantısı başarısız!")
                return False
                
        except Exception as e:
            print(f"❌ Kamera başlatma hatası: {e}")
            return False
    
    def show_stream(self, window_name="RTSP Kamera", save_frames=False):
        """Kamera stream'ini gösterir"""
        if not self.is_running:
            print("❌ Kamera çalışmıyor!")
            return
        
        print("📺 Stream başlatılıyor... (Çıkmak için 'q' tuşuna basın)")
        
        frame_count = 0
        start_time = time.time()
        
        try:
            while self.is_running:
                ret, frame = self.camera.read()
                
                if ret:
                    frame_count += 1
                    
                    # FPS hesapla
                    elapsed_time = time.time() - start_time
                    if elapsed_time > 0:
                        fps = frame_count / elapsed_time
                        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        cv2.putText(frame, f"Frame: {frame_count}", (10, 70), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    # Frame'i göster
                    cv2.imshow(window_name, frame)
                    
                    # Frame kaydet (opsiyonel)
                    if save_frames and frame_count % 30 == 0:  # Her 30 frame'de bir
                        filename = f"frame_{frame_count:04d}.jpg"
                        cv2.imwrite(filename, frame)
                        print(f"💾 Frame kaydedildi: {filename}")
                    
                    # 'q' tuşu ile çık
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    print("⚠️ Frame okunamadı, yeniden deneniyor...")
                    time.sleep(0.1)
                    
        except KeyboardInterrupt:
            print("\n⏹️ Stream kullanıcı tarafından durduruldu.")
        except Exception as e:
            print(f"❌ Stream hatası: {e}")
        finally:
            cv2.destroyAllWindows()
    
    def capture_single_frame(self):
        """Tek frame yakalar"""
        if not self.is_running:
            print("❌ Kamera çalışmıyor!")
            return None
        
        ret, frame = self.camera.read()
        if ret:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"capture_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"📸 Frame yakalandı: {filename}")
            return frame
        else:
            print("❌ Frame yakalanamadı!")
            return None
    
    def stop(self):
        """Kamerayı durdurur"""
        self.is_running = False
        
        if self.camera:
            self.camera.stop_capture()
        
        print("🛑 Kamera durduruldu.")

def main():
    """Ana fonksiyon"""
    print("🚀 RTSP Kamera Örnek Uygulaması")
    print("=" * 50)
    
    # RTSP URL
    rtsp_url = "rtsp://192.168.1.100:554/H.264/media.smp"
    
    # Uygulama oluştur
    app = RTSPCameraApp(rtsp_url)
    
    try:
        # Kamerayı başlat
        if app.start():
            print("\n📋 Kullanılabilir komutlar:")
            print("   1. Stream göster")
            print("   2. Tek frame yakala")
            print("   3. Çıkış")
            
            while True:
                choice = input("\nSeçiminizi yapın (1-3): ").strip()
                
                if choice == '1':
                    print("\n📺 Stream başlatılıyor...")
                    app.show_stream(save_frames=True)
                    
                elif choice == '2':
                    print("\n📸 Frame yakalanıyor...")
                    app.capture_single_frame()
                    
                elif choice == '3':
                    print("👋 Çıkılıyor...")
                    break
                    
                else:
                    print("❌ Geçersiz seçim!")
        
        else:
            print("❌ Uygulama başlatılamadı!")
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Uygulama kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n❌ Uygulama hatası: {e}")
        import traceback
        traceback.print_exc()
    finally:
        app.stop()

if __name__ == "__main__":
    main()
