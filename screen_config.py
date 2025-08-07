#!/usr/bin/env python3
"""
Ekran yakalama konfigürasyon dosyası
"""

class ScreenConfig:
    """Ekran yakalama ayarları"""
    
    # Temel ayarlar
    USE_SCREEN_CAPTURE = True
    SCREEN_CAPTURE_FPS = 10
    
    # Bölge ayarları (x, y, width, height)
    # None = tüm ekran
    # (0, 0, 800, 600) = sol üst köşeden 800x600 piksel
    SCREEN_REGION = None
    
    # Monitör seçimi (çoklu monitör için)
    SCREEN_MONITOR = 0
    
    # Performans ayarları
    PROCESS_EVERY_N_FRAMES = 3  # Ekran yakalama için yavaş işleme
    
    # Önceden tanımlanmış bölgeler
    REGIONS = {
        'full_screen': None,
        'top_left': (0, 0, 800, 600),
        'center': (400, 300, 800, 600),
        'bottom_right': (800, 600, 800, 600),
        'small_region': (100, 100, 400, 300),
        'webcam_area': (200, 200, 640, 480)
    }
    
    @classmethod
    def set_region(cls, region_name):
        """Önceden tanımlanmış bölgeyi ayarla"""
        if region_name in cls.REGIONS:
            cls.SCREEN_REGION = cls.REGIONS[region_name]
            print(f"Bölge ayarlandı: {region_name}")
            return True
        else:
            print(f"Bilinmeyen bölge: {region_name}")
            print(f"Mevcut bölgeler: {list(cls.REGIONS.keys())}")
            return False
    
    @classmethod
    def set_custom_region(cls, x, y, width, height):
        """Özel bölge ayarla"""
        cls.SCREEN_REGION = (x, y, width, height)
        print(f"Özel bölge ayarlandı: ({x}, {y}, {width}, {height})")
    
    @classmethod
    def get_region_info(cls):
        """Mevcut bölge bilgisini döndür"""
        if cls.SCREEN_REGION is None:
            return "Tüm ekran"
        else:
            x, y, w, h = cls.SCREEN_REGION
            return f"Bölge: ({x}, {y}, {w}, {h})"

def test_regions():
    """Bölge test fonksiyonu"""
    print("=== BÖLGE TESTİ ===")
    
    for region_name, region in ScreenConfig.REGIONS.items():
        if region is None:
            print(f"{region_name}: Tüm ekran")
        else:
            x, y, w, h = region
            print(f"{region_name}: ({x}, {y}, {w}, {h})")

if __name__ == "__main__":
    test_regions() 