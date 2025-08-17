#!/usr/bin/env python3
"""
Hızlı Başlangıç Scripti - Yeni bilgisayarlarda test için
"""

import sys
import os
import subprocess
import importlib

def check_python_version():
    """Python versiyonunu kontrol eder"""
    print("🐍 Python Versiyon Kontrolü...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"❌ Python 3.9+ gerekli! Mevcut: {version.major}.{version.minor}")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Uygun!")
        return True

def check_dependencies():
    """Gerekli modülleri kontrol eder"""
    print("\n📦 Modül Kontrolü...")
    
    required_modules = [
        'cv2', 'ultralytics', 'torch', 'numpy', 
        'requests', 'flask', 'PIL', 'psutil'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module} - Yüklü")
        except ImportError:
            print(f"❌ {module} - Eksik")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️  Eksik modüller: {', '.join(missing_modules)}")
        print("💡 Çözüm: pip install -r requirements.txt")
        return False
    else:
        print("✅ Tüm modüller yüklü!")
        return True

def check_model_files():
    """Model dosyalarını kontrol eder"""
    print("\n🤖 Model Dosya Kontrolü...")
    
    model_files = [
        'yolov8n.pt', 'yolov8s.pt', 'yolov8m.pt', 'yolov8l.pt'
    ]
    
    missing_models = []
    
    for model in model_files:
        if os.path.exists(model):
            size_mb = os.path.getsize(model) / (1024 * 1024)
            print(f"✅ {model} - {size_mb:.1f}MB")
        else:
            print(f"❌ {model} - Eksik")
            missing_models.append(model)
    
    if missing_models:
        print(f"\n⚠️  Eksik model dosyaları: {', '.join(missing_models)}")
        print("💡 Çözüm: Model dosyalarını proje klasörüne kopyalayın")
        return False
    else:
        print("✅ Tüm model dosyaları mevcut!")
        return True

def check_system_info():
    """Sistem bilgilerini gösterir"""
    print("\n💻 Sistem Bilgileri...")
    
    import platform
    import psutil
    
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Python: {platform.python_version()}")
    print(f"CPU: {psutil.cpu_count()} çekirdek")
    print(f"RAM: {psutil.virtual_memory().total / (1024**3):.1f}GB")
    
    # GPU kontrolü
    try:
        import torch
        if torch.cuda.is_available():
            print(f"GPU: CUDA destekli ({torch.cuda.get_device_name(0)})")
        else:
            print("GPU: CUDA desteklenmiyor (CPU kullanılacak)")
    except:
        print("GPU: Torch kurulumu gerekli")

def run_basic_test():
    """Temel test çalıştırır"""
    print("\n🧪 Temel Test Çalıştırılıyor...")
    
    try:
        # Config testi
        from config import Config
        print(f"✅ Config yüklendi - Model: {Config.MODEL_PATH}")
        
        # Detector testi
        from human_detector import HumanDetector
        detector = HumanDetector()
        print("✅ Human Detector başlatıldı")
        
        # Counter testi
        from counter import HumanCounter
        counter = HumanCounter()
        print("✅ Human Counter başlatıldı")
        
        print("✅ Temel test başarılı!")
        return True
        
    except Exception as e:
        print(f"❌ Temel test başarısız: {e}")
        return False

def main():
    """Ana fonksiyon"""
    print("🚀 AvvaImageAI - Hızlı Başlangıç Testi")
    print("=" * 50)
    
    # Sistem kontrolleri
    if not check_python_version():
        return False
    
    if not check_dependencies():
        return False
    
    if not check_model_files():
        return False
    
    check_system_info()
    
    # Temel test
    if not run_basic_test():
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Tüm testler başarılı! Sistem kullanıma hazır.")
    print("\n📋 Sonraki adımlar:")
    print("1. Kamera testi: python3 test_camera.py")
    print("2. Ekran yakalama testi: python3 test_screen_capture.py")
    print("3. Performans testi: python3 performance_test.py")
    print("4. Ana uygulama: python3 main.py")
    print("5. Web arayüzü: python3 app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
