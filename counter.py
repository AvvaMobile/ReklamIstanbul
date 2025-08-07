import cv2
import numpy as np
from datetime import datetime, timedelta
import json
import os
import logging
from config import Config
from endpoint_client import EndpointClient

class HumanCounter:
    def __init__(self, device_id='default', location='unknown'):
        """
        İnsan sayma sistemi - Kamera açısına giren kişileri sayar
        """
        self.counted_people = set()  # Sayılan insanları takip etmek için
        self.active_people = {}  # Aktif insanları takip etmek için (ID -> son görülme zamanı)
        self.person_positions = {}  # Kişi pozisyonlarını takip etmek için (ID -> (center_x, center_y))
        self.total_count = 0
        self.daily_count = 0
        self.hourly_count = 0
        self.last_reset_date = datetime.now().date()
        self.last_reset_hour = datetime.now().hour
        self.device_id = device_id
        self.location = location
        
        # İnsan takip ayarları - İyileştirilmiş
        self.person_timeout = Config.PERSON_TIMEOUT
        self.min_confidence = Config.MIN_CONFIDENCE
        self.position_threshold = Config.TRACKING_THRESHOLD
        self.size_threshold = Config.SIZE_THRESHOLD
        
        # Performans optimizasyonları
        self.frame_skip_counter = 0
        self.previous_detections = []
        
        # Endpoint client'ı başlat
        self.endpoint_client = EndpointClient()
        
        # Logging ayarları
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{Config.LOG_DIR}/counter.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Klasörleri oluştur
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        os.makedirs(Config.LOG_DIR, exist_ok=True)
        
    def should_reset_hourly(self):
        """
        Saatlik sıfırlama gerekiyor mu kontrol eder
        """
        if not Config.HOURLY_RESET:
            return False
            
        current_hour = datetime.now().hour
        return current_hour != self.last_reset_hour
    
    def should_reset_daily(self):
        """
        Günlük sıfırlama gerekiyor mu kontrol eder
        """
        current_date = datetime.now().date()
        return current_date != self.last_reset_date
    
    def reset_hourly_count(self):
        """
        Saatlik sayımı sıfırlar ve endpoint'e gönderir
        """
        if self.hourly_count > 0:
            self.logger.info(f"Saatlik sayım sıfırlanıyor. Son sayım: {self.hourly_count}")
            
            # Endpoint'e veri gönder
            count_data = {
                'hourly_count': self.hourly_count,
                'daily_count': self.daily_count,
                'total_count': self.total_count,
                'device_id': self.device_id,
                'location': self.location
            }
            
            success, response = self.endpoint_client.send_count_data(count_data)
            
            if success:
                self.logger.info("Saatlik veri başarıyla endpoint'e gönderildi")
            else:
                self.logger.error(f"Endpoint'e veri gönderilemedi: {response}")
        
        # Sayacı sıfırla
        self.hourly_count = 0
        self.last_reset_hour = datetime.now().hour
        self.counted_people.clear()
        self.active_people.clear()
        self.person_positions.clear()
        
    def reset_daily_count(self):
        """
        Günlük sayımı sıfırlar
        """
        self.logger.info(f"Günlük sayım sıfırlanıyor. Son sayım: {self.daily_count}")
        self.daily_count = 0
        self.last_reset_date = datetime.now().date()
        self.counted_people.clear()
        self.active_people.clear()
        self.person_positions.clear()
        
        # Günlük veriyi kaydet
        self.save_daily_count()
    
    def calculate_distance(self, pos1, pos2):
        """
        İki pozisyon arasındaki mesafeyi hesaplar
        """
        return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def calculate_size_similarity(self, area1, area2):
        """
        İki alan arasındaki benzerliği hesaplar
        """
        if area1 == 0 or area2 == 0:
            return 0
        return min(area1, area2) / max(area1, area2)
    
    def find_existing_person(self, detection):
        """
        Tespit edilen kişinin mevcut aktif kişilerden biri olup olmadığını kontrol eder - İyileştirilmiş
        """
        x1, y1, x2, y2 = detection['bbox']
        current_center = ((x1 + x2) // 2, (y1 + y2) // 2)
        current_area = (x2 - x1) * (y2 - y1)
        
        best_match = None
        best_score = 0
        
        for person_id, last_position in self.person_positions.items():
            if person_id in self.active_people:
                # Pozisyon mesafesini kontrol et
                distance = self.calculate_distance(current_center, last_position)
                
                # Boyut benzerliğini kontrol et
                last_area = self.person_positions.get(f"{person_id}_area", current_area)
                size_similarity = self.calculate_size_similarity(current_area, last_area)
                
                # Toplam skor hesapla
                position_score = max(0, 1 - distance / self.position_threshold)
                size_score = size_similarity
                total_score = (position_score + size_score) / 2
                
                if total_score > best_score and total_score > 0.6:
                    best_match = person_id
                    best_score = total_score
        
        return best_match
    
    def generate_person_id(self, detection):
        """
        İnsan için benzersiz ID oluşturur - İyileştirilmiş
        """
        x1, y1, x2, y2 = detection['bbox']
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        area = (x2 - x1) * (y2 - y1)
        
        # Daha stabil ID oluştur (pozisyonu yuvarla)
        rounded_x = (center_x // 10) * 10  # Daha hassas
        rounded_y = (center_y // 10) * 10
        rounded_area = (area // 500) * 500  # Daha hassas
        
        return f"{rounded_x}_{rounded_y}_{rounded_area}"
    
    def cleanup_inactive_people(self):
        """
        Belirli süre görünmeyen insanları aktif listesinden çıkarır
        """
        current_time = datetime.now()
        inactive_people = []
        
        for person_id, last_seen in self.active_people.items():
            time_diff = (current_time - last_seen).total_seconds()
            if time_diff > self.person_timeout:
                inactive_people.append(person_id)
                self.logger.debug(f"Kişi {person_id} {time_diff:.1f}s görünmedi, aktif listesinden çıkarıldı")
        
        for person_id in inactive_people:
            del self.active_people[person_id]
            if person_id in self.person_positions:
                del self.person_positions[person_id]
            if f"{person_id}_area" in self.person_positions:
                del self.person_positions[f"{person_id}_area"]
    
    def count_humans(self, detections, frame):
        """
        Tespit edilen insanları sayar - Kamera açısına giren kişileri sayar - İyileştirilmiş
        """
        current_time = datetime.now()
        
        # Saatlik sıfırlama kontrolü
        if self.should_reset_hourly():
            self.reset_hourly_count()
        
        # Günlük sıfırlama kontrolü
        if self.should_reset_daily():
            self.reset_daily_count()
        
        # Aktif olmayan insanları temizle
        self.cleanup_inactive_people()
        
        # Frame atlama kontrolü (performans için)
        self.frame_skip_counter += 1
        if self.frame_skip_counter % Config.SKIP_FRAMES_FOR_TRACKING != 0:
            # Frame'i güncelle ama detaylı işleme yapma
            self.draw_info_on_frame(frame, set(), detections)
            return frame, self.hourly_count, self.daily_count
        
        # Mevcut frame'deki insanları işle
        current_frame_people = set()
        
        for detection in detections:
            confidence = detection['confidence']
            
            # Güven skoru çok düşükse atla
            if confidence < self.min_confidence:
                continue
            
            x1, y1, x2, y2 = detection['bbox']
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            area = (x2 - x1) * (y2 - y1)
            
            # Bu kişi mevcut aktif kişilerden biri mi kontrol et
            existing_person_id = self.find_existing_person(detection)
            
            if existing_person_id:
                # Mevcut kişi - pozisyonunu güncelle
                person_id = existing_person_id
                self.person_positions[person_id] = (center_x, center_y)
                self.person_positions[f"{person_id}_area"] = area
                self.active_people[person_id] = current_time
                current_frame_people.add(person_id)
                
                self.logger.debug(f"Mevcut kişi güncellendi: {person_id}")
            else:
                # Yeni kişi - ID oluştur ve say
                person_id = self.generate_person_id(detection)
                
                # Bu ID daha önce sayılmış mı kontrol et
                if person_id not in self.counted_people:
                    # Yeni insan - say
                    self.counted_people.add(person_id)
                    self.total_count += 1
                    self.daily_count += 1
                    self.hourly_count += 1
                    
                    self.logger.info(f"Yeni insan kamera açısına girdi. Saatlik: {self.hourly_count}, Günlük: {self.daily_count}")
                
                # Aktif listesine ekle
                self.active_people[person_id] = current_time
                self.person_positions[person_id] = (center_x, center_y)
                self.person_positions[f"{person_id}_area"] = area
                current_frame_people.add(person_id)
        
        # Frame üzerine bilgileri çiz
        self.draw_info_on_frame(frame, current_frame_people, detections)
        
        return frame, self.hourly_count, self.daily_count
    
    def draw_info_on_frame(self, frame, current_frame_people, detections):
        """
        Frame üzerine bilgileri çizer - İyileştirilmiş
        """
        # Aktif insan sayısını göster
        active_count = len(current_frame_people)
        
        # Bilgi metinleri
        cv2.putText(frame, f'Aktif Insanlar: {active_count}', 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.putText(frame, f'Saatlik Sayim: {self.hourly_count}', 
                   (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        cv2.putText(frame, f'Gunluk Sayim: {self.daily_count}', 
                   (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        cv2.putText(frame, f'Toplam Sayim: {self.total_count}', 
                   (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        # Performans bilgisi
        cv2.putText(frame, f'FPS: {self.get_fps():.1f}', 
                   (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Kamera açısı bilgisi
        cv2.putText(frame, 'Kamera Acisina Giren Kisiler Sayiliyor', 
                   (10, frame.shape[0] - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Aktif insanlar için çerçeve çiz
        for person_id in current_frame_people:
            # Bu kişinin son tespit bilgilerini bul
            for detection in detections:
                temp_id = self.find_existing_person(detection)
                if temp_id == person_id:
                    x1, y1, x2, y2 = detection['bbox']
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f'ID: {person_id[:8]}', (x1, y1-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    break
    
    def get_fps(self):
        """
        Tahmini FPS değerini döndürür
        """
        # Basit FPS hesaplama (gerçek implementasyon için daha gelişmiş bir sistem gerekir)
        return 30.0  # Varsayılan değer
    
    def save_daily_count(self):
        """
        Günlük sayım verilerini kaydeder
        """
        today = datetime.now().strftime('%Y-%m-%d')
        data = {
            'date': today,
            'daily_count': self.daily_count,
            'total_count': self.total_count,
            'device_id': self.device_id,
            'location': self.location,
            'timestamp': datetime.now().isoformat()
        }
        
        # JSON dosyasına kaydet
        filename = f'{Config.DATA_DIR}/{today}.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.logger.info(f"Günlük veri kaydedildi: {filename}")
    
    def get_stats(self):
        """
        Mevcut istatistikleri döndürür
        """
        return {
            'hourly_count': self.hourly_count,
            'daily_count': self.daily_count,
            'total_count': self.total_count,
            'active_people': len(self.active_people),
            'last_reset_hour': self.last_reset_hour,
            'last_reset_date': self.last_reset_date.isoformat(),
            'device_id': self.device_id,
            'location': self.location
        } 