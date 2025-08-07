#!/usr/bin/env python3
"""
Model seçici - Farklı YOLO modellerini test eder ve en iyi performansı veren modeli seçer
"""

import cv2
import time
import numpy as np
from ultralytics import YOLO
import os
from config import Config
import logging

class ModelSelector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.models = {
            'yolov8n.pt': 'Nano - Hızlı, küçük',
            'yolov8s.pt': 'Small - Dengeli',
            'yolov8m.pt': 'Medium - Orta performans',
            'yolov8l.pt': 'Large - Yüksek doğruluk',
            'yolov8x.pt': 'XLarge - En yüksek doğruluk'
        }
    
    def test_model_performance(self, model_path, test_frames=50):
        """Belirli bir modelin performansını test eder"""
        try:
            self.logger.info(f"Model test ediliyor: {model_path}")
            
            # Model yükle
            model = YOLO(model_path)
            model.to(Config.DEVICE)
            
            # Test görüntüsü oluştur
            test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
            
            # Performans testi
            start_time = time.time()
            total_detections = 0
            
            for i in range(test_frames):
                results = model(
                    test_frame, 
                    classes=[0],  # person class
                    conf=Config.MODEL_CONFIDENCE,
                    iou=Config.MODEL_IOU_THRESHOLD,
                    max_det=Config.MODEL_MAX_DET,
                    verbose=False
                )
                
                for result in results:
                    if result.boxes is not None:
                        total_detections += len(result.boxes)
            
            end_time = time.time()
            total_time = end_time - start_time
            avg_time = total_time / test_frames
            fps = 1 / avg_time if avg_time > 0 else 0
            
            # Model boyutunu hesapla
            model_size = os.path.getsize(model_path) / (1024 * 1024) if os.path.exists(model_path) else 0
            
            return {
                'model_path': model_path,
                'avg_time': avg_time,
                'fps': fps,
                'total_detections': total_detections,
                'model_size_mb': model_size,
                'success': True
            }
            
        except Exception as e:
            self.logger.error(f"Model test hatası {model_path}: {e}")
            return {
                'model_path': model_path,
                'avg_time': None,
                'fps': None,
                'total_detections': 0,
                'model_size_mb': 0,
                'success': False,
                'error': str(e)
            }
    
    def find_best_model(self, min_fps=10, max_model_size_mb=100):
        """En iyi modeli bulur"""
        self.logger.info("En iyi model aranıyor...")
        
        results = []
        
        for model_path, description in self.models.items():
            self.logger.info(f"Test ediliyor: {model_path} - {description}")
            result = self.test_model_performance(model_path)
            results.append(result)
            
            if result['success']:
                self.logger.info(f"✓ {model_path}: {result['fps']:.1f} FPS, {result['model_size_mb']:.1f} MB")
            else:
                self.logger.info(f"✗ {model_path}: Başarısız")
        
        # Filtreleme ve sıralama
        valid_results = [r for r in results if r['success'] and r['fps'] >= min_fps and r['model_size_mb'] <= max_model_size_mb]
        
        if not valid_results:
            self.logger.warning("Hiçbir model kriterleri karşılamıyor!")
            return None
        
        # En iyi modeli seç (FPS'e göre)
        best_model = max(valid_results, key=lambda x: x['fps'])
        
        self.logger.info(f"En iyi model: {best_model['model_path']}")
        self.logger.info(f"FPS: {best_model['fps']:.1f}")
        self.logger.info(f"Model boyutu: {best_model['model_size_mb']:.1f} MB")
        
        return best_model
    
    def download_model(self, model_name):
        """Modeli indirir"""
        try:
            self.logger.info(f"Model indiriliyor: {model_name}")
            model = YOLO(model_name)
            self.logger.info(f"Model başarıyla indirildi: {model_name}")
            return True
        except Exception as e:
            self.logger.error(f"Model indirme hatası: {e}")
            return False
    
    def get_available_models(self):
        """Mevcut modelleri listeler"""
        available = []
        
        for model_path in self.models.keys():
            if os.path.exists(model_path):
                size_mb = os.path.getsize(model_path) / (1024 * 1024)
                available.append({
                    'name': model_path,
                    'description': self.models[model_path],
                    'size_mb': size_mb
                })
        
        return available
    
    def recommend_model(self, target_fps=20, max_size_mb=50):
        """Hedef performansa göre model önerir"""
        self.logger.info(f"Hedef FPS: {target_fps}, Maksimum boyut: {max_size_mb} MB")
        
        available = self.get_available_models()
        
        if not available:
            self.logger.info("Hiçbir model bulunamadı. Modeller indiriliyor...")
            for model_name in self.models.keys():
                self.download_model(model_name)
            available = self.get_available_models()
        
        # Performans testi yap
        best_model = self.find_best_model(min_fps=target_fps, max_model_size_mb=max_size_mb)
        
        if best_model:
            self.logger.info(f"Önerilen model: {best_model['model_path']}")
            return best_model['model_path']
        else:
            self.logger.warning("Uygun model bulunamadı!")
            return None

def main():
    """Ana fonksiyon"""
    logging.basicConfig(level=logging.INFO)
    selector = ModelSelector()
    
    print("=== MODEL SEÇİCİ ===")
    print("1. Mevcut modelleri listele")
    print("2. En iyi modeli bul")
    print("3. Model öner")
    print("4. Performans testi")
    
    choice = input("Seçiminiz (1-4): ")
    
    if choice == '1':
        models = selector.get_available_models()
        print("\nMevcut modeller:")
        for model in models:
            print(f"- {model['name']}: {model['description']} ({model['size_mb']:.1f} MB)")
    
    elif choice == '2':
        best = selector.find_best_model()
        if best:
            print(f"\nEn iyi model: {best['model_path']}")
            print(f"FPS: {best['fps']:.1f}")
            print(f"Boyut: {best['model_size_mb']:.1f} MB")
    
    elif choice == '3':
        target_fps = float(input("Hedef FPS: "))
        max_size = float(input("Maksimum boyut (MB): "))
        recommended = selector.recommend_model(target_fps, max_size)
        if recommended:
            print(f"\nÖnerilen model: {recommended}")
    
    elif choice == '4':
        model_path = input("Test edilecek model: ")
        result = selector.test_model_performance(model_path)
        if result['success']:
            print(f"\nSonuçlar:")
            print(f"FPS: {result['fps']:.1f}")
            print(f"Ortalama süre: {result['avg_time']:.4f} saniye")
            print(f"Toplam tespit: {result['total_detections']}")
            print(f"Model boyutu: {result['model_size_mb']:.1f} MB")
        else:
            print(f"Hata: {result.get('error', 'Bilinmeyen hata')}")

if __name__ == "__main__":
    main() 