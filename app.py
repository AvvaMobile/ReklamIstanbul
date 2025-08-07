#!/usr/bin/env python3
"""
İnsan Sayma Sistemi - Web UI
"""

from flask import Flask, render_template, request, jsonify, Response
import cv2
import threading
import time
import json
import os
from datetime import datetime
from human_detector import HumanDetector
from counter import HumanCounter
from config import Config
from screen_capture import ScreenCapture
import logging

app = Flask(__name__)

# Global değişkenler
detector = None
counter = None
video_source = None
screen_capture = None
is_running = False
current_config = {
    'use_screen_capture': False,
    'camera_index': 0,
    'screen_region': None,
    'detection_threshold': 0.4,
    'model_path': 'yolov8s.pt'
}

def setup_logging():
    """Logging ayarlarını yapılandırır"""
    os.makedirs(Config.LOG_DIR, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'{Config.LOG_DIR}/web_ui.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def get_available_cameras():
    """Mevcut kameraları listeler"""
    cameras = []
    for i in range(10):  # 0-9 arası kamera indekslerini kontrol et
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                cameras.append({
                    'index': i,
                    'name': f'Kamera {i}',
                    'resolution': f'{int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}'
                })
            cap.release()
    return cameras

def initialize_system():
    """Sistemi başlatır"""
    global detector, counter, video_source, screen_capture
    
    # Detector'ı başlat
    detector = HumanDetector(model_path=current_config['model_path'])
    
    # Counter'ı başlat
    counter = HumanCounter(
        device_id='web_ui',
        location='web_interface'
    )
    
    # Video kaynağını ayarla
    if current_config['use_screen_capture']:
        screen_capture = ScreenCapture(
            monitor=0,
            region=current_config['screen_region']
        )
        screen_capture.start_capture()
        video_source = screen_capture
    else:
        video_source = cv2.VideoCapture(current_config['camera_index'])
        video_source.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        video_source.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        video_source.set(cv2.CAP_PROP_FPS, 30)
    
    logger.info("Sistem başlatıldı")

def cleanup_system():
    """Sistemi temizler"""
    global video_source, screen_capture
    
    if screen_capture:
        screen_capture.stop_capture()
    elif video_source:
        video_source.release()
    
    logger.info("Sistem temizlendi")

def generate_frames():
    """Video frame'lerini üretir"""
    global is_running, detector, counter, video_source
    
    while is_running:
        try:
            if current_config['use_screen_capture']:
                ret, frame = video_source.read()
            else:
                ret, frame = video_source.read()
            
            if not ret:
                continue
            
            # İnsanları tespit et
            detections = detector.detect_humans(frame)
            
            # Tespit edilen insanları çiz
            frame = detector.draw_detections(frame, detections)
            
            # İnsanları say
            frame, hourly_count, daily_count = counter.count_humans(detections, frame)
            
            # Bilgileri ekrana yaz
            cv2.putText(frame, f'Saatlik: {hourly_count}', 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f'Gunluk: {daily_count}', 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            cv2.putText(frame, f'Toplam: {counter.total_count}', 
                       (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            # Video kaynağı bilgisi
            source_info = "Ekran Yakalama" if current_config['use_screen_capture'] else "Kamera"
            cv2.putText(frame, f'Kaynak: {source_info}', 
                       (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Frame'i JPEG formatına dönüştür
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            time.sleep(0.03)  # ~30 FPS
            
        except Exception as e:
            logger.error(f"Frame üretme hatası: {e}")
            continue

# Logging ayarları
logger = setup_logging()

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

@app.route('/api/cameras')
def get_cameras():
    """Mevcut kameraları döndürür"""
    cameras = get_available_cameras()
    return jsonify(cameras)

@app.route('/api/config', methods=['GET', 'POST'])
def config():
    """Konfigürasyon yönetimi"""
    global current_config
    
    if request.method == 'POST':
        data = request.json
        current_config.update(data)
        logger.info(f"Konfigürasyon güncellendi: {current_config}")
        return jsonify({'status': 'success', 'config': current_config})
    else:
        return jsonify(current_config)

@app.route('/api/start', methods=['POST'])
def start_system():
    """Sistemi başlatır"""
    global is_running
    
    if is_running:
        return jsonify({'status': 'error', 'message': 'Sistem zaten çalışıyor'})
    
    try:
        initialize_system()
        is_running = True
        logger.info("Sistem başlatıldı")
        return jsonify({'status': 'success', 'message': 'Sistem başlatıldı'})
    except Exception as e:
        logger.error(f"Sistem başlatma hatası: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/stop', methods=['POST'])
def stop_system():
    """Sistemi durdurur"""
    global is_running
    
    if not is_running:
        return jsonify({'status': 'error', 'message': 'Sistem zaten durmuş'})
    
    try:
        is_running = False
        cleanup_system()
        logger.info("Sistem durduruldu")
        return jsonify({'status': 'success', 'message': 'Sistem durduruldu'})
    except Exception as e:
        logger.error(f"Sistem durdurma hatası: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/stats')
def get_stats():
    """İstatistikleri döndürür"""
    if counter:
        stats = counter.get_stats()
        stats['is_running'] = is_running
        return jsonify(stats)
    else:
        return jsonify({'is_running': is_running})

@app.route('/video_feed')
def video_feed():
    """Video stream endpoint'i"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 