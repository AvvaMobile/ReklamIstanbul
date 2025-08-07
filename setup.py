#!/usr/bin/env python3
"""
Kurulum scripti - Gerekli klasörleri ve dosyaları oluşturur
"""

import os
import shutil
from pathlib import Path

def create_directories():
    """
    Gerekli klasörleri oluşturur
    """
    directories = [
        'data',
        'data/daily_counts',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Klasör oluşturuldu: {directory}")

def create_env_file():
    """
    .env dosyasını oluşturur
    """
    if not os.path.exists('.env'):
        if os.path.exists('env_example.txt'):
            shutil.copy('env_example.txt', '.env')
            print("✅ .env dosyası oluşturuldu (env_example.txt'den kopyalandı)")
        else:
            print("⚠️  env_example.txt dosyası bulunamadı")
    else:
        print("✅ .env dosyası zaten mevcut")

def check_dependencies():
    """
    Gerekli Python paketlerini kontrol eder
    """
    required_packages = [
        ('cv2', 'opencv-python'),
        ('ultralytics', 'ultralytics'),
        ('numpy', 'numpy'),
        ('requests', 'requests'),
        ('dotenv', 'python-dotenv')
    ]
    
    missing_packages = []
    
    for import_name, package_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print("❌ Eksik paketler:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nKurulum için: pip install -r requirements.txt")
        return False
    else:
        print("✅ Tüm gerekli paketler yüklü")
        return True

def main():
    """
    Ana kurulum fonksiyonu
    """
    print("=" * 50)
    print("İNSAN SAYMA SİSTEMİ KURULUMU")
    print("=" * 50)
    
    # Klasörleri oluştur
    print("\n1. Klasörler oluşturuluyor...")
    create_directories()
    
    # .env dosyasını oluştur
    print("\n2. Environment dosyası kontrol ediliyor...")
    create_env_file()
    
    # Bağımlılıkları kontrol et
    print("\n3. Python paketleri kontrol ediliyor...")
    dependencies_ok = check_dependencies()
    
    print("\n" + "=" * 50)
    if dependencies_ok:
        print("✅ Kurulum tamamlandı!")
        print("\nKullanım:")
        print("1. .env dosyasını düzenleyin")
        print("2. python main.py ile çalıştırın")
        print("3. python test_endpoint.py ile endpoint'i test edin")
    else:
        print("⚠️  Kurulum tamamlandı ancak eksik paketler var")
        print("Lütfen eksik paketleri yükleyin")
    print("=" * 50)

if __name__ == "__main__":
    main() 