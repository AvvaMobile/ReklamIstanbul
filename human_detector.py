import cv2
import numpy as np
from ultralytics import YOLO
import time
from config import Config

class HumanDetector:
    def __init__(self, model_path=None):
        """
        İnsan tespiti için YOLO modelini yükler
        """
        if model_path is None:
            model_path = Config.MODEL_PATH
            
        try:
            self.model = YOLO(model_path)
            # GPU kullanımını ayarla
            self.model.to(Config.DEVICE)
            print(f"YOLO modeli yüklendi: {model_path} - Cihaz: {Config.DEVICE}")
        except Exception as e:
            print(f"Model yüklenirken hata: {e}")
            try:
                # Alternatif yükleme yöntemi
                print("Alternatif model yükleme yöntemi deneniyor...")
                self.model = YOLO('yolov8s.pt')
                self.model.to(Config.DEVICE)
                print("YOLO modeli alternatif yöntemle yüklendi")
            except Exception as e2:
                print(f"Alternatif yükleme de başarısız: {e2}")
                # En basit yöntem
                print("En basit model yükleme yöntemi deneniyor...")
                self.model = YOLO()
                self.model.to(Config.DEVICE)
                print("Varsayılan YOLO modeli yüklendi")
            
        self.detection_threshold = Config.DETECTION_THRESHOLD
        self.frame_count = 0
        
    def detect_humans(self, frame):
        """
        Frame'deki insanları tespit eder - Optimize edilmiş
        """
        try:
            # Her N frame'de bir işle (performans için)
            self.frame_count += 1
            if self.frame_count % Config.PROCESS_EVERY_N_FRAMES != 0:
                return []
            
            # Frame'i optimize et - Config'deki boyutları kullan
            target_size = (Config.FRAME_WIDTH, Config.FRAME_HEIGHT)
            if frame.shape[:2] != target_size[::-1]:  # OpenCV (height, width) formatı
                frame_resized = cv2.resize(frame, target_size)
            else:
                frame_resized = frame
            
            # Model parametrelerini optimize et
            results = self.model(
                frame_resized, 
                classes=[0],  # class 0 = person
                conf=Config.MODEL_CONFIDENCE,
                iou=Config.MODEL_IOU_THRESHOLD,
                max_det=Config.MODEL_MAX_DET,
                verbose=False
            )
            
            detections = []
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        confidence = box.conf[0].item()
                        if confidence > self.detection_threshold:
                            x1, y1, x2, y2 = box.xyxy[0].tolist()
                            
                            # Orijinal frame boyutuna geri dönüştür
                            if frame.shape[:2] != target_size[::-1]:
                                h_scale = frame.shape[0] / target_size[1]  # height
                                w_scale = frame.shape[1] / target_size[0]  # width
                                x1 = int(x1 * w_scale)
                                y1 = int(y1 * h_scale)
                                x2 = int(x2 * w_scale)
                                y2 = int(y2 * h_scale)
                            
                            detections.append({
                                'bbox': (int(x1), int(y1), int(x2), int(y2)),
                                'confidence': confidence
                            })
            
            return detections
        except Exception as e:
            print(f"İnsan tespiti sırasında hata: {e}")
            return []
    
    def detect_humans_with_tracking(self, frame, previous_detections=None):
        """
        Takip ile insan tespiti - Daha stabil sonuçlar
        """
        current_detections = self.detect_humans(frame)
        
        if previous_detections is None:
            return current_detections
        
        # Önceki tespitlerle birleştir (tracking)
        tracked_detections = []
        
        for current in current_detections:
            best_match = None
            best_distance = float('inf')
            
            for prev in previous_detections:
                # Mesafe hesapla
                curr_center = ((current['bbox'][0] + current['bbox'][2]) // 2,
                              (current['bbox'][1] + current['bbox'][3]) // 2)
                prev_center = ((prev['bbox'][0] + prev['bbox'][2]) // 2,
                              (prev['bbox'][1] + prev['bbox'][3]) // 2)
                
                distance = np.sqrt((curr_center[0] - prev_center[0])**2 + 
                                 (curr_center[1] - prev_center[1])**2)
                
                if distance < Config.TRACKING_THRESHOLD and distance < best_distance:
                    best_match = prev
                    best_distance = distance
            
            if best_match:
                # Güven skorunu ortalama al
                avg_confidence = (current['confidence'] + best_match['confidence']) / 2
                tracked_detections.append({
                    'bbox': current['bbox'],
                    'confidence': avg_confidence
                })
            else:
                tracked_detections.append(current)
        
        return tracked_detections
    
    def draw_detections(self, frame, detections):
        """
        Tespit edilen insanları frame üzerine çizer
        """
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            confidence = detection['confidence']
            
            # Güven skoruna göre renk belirle
            if confidence > 0.7:
                color = (0, 255, 0)  # Yeşil - yüksek güven
            elif confidence > 0.5:
                color = (0, 255, 255)  # Sarı - orta güven
            else:
                color = (0, 0, 255)  # Kırmızı - düşük güven
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f'Person: {confidence:.2f}', 
                       (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        return frame 