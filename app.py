#!/usr/bin/env python3
"""
İnsan Sayma Sistemi - Web UI (RTSP Kamera)
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
from network_camera import RTSPCamera
import logging

app = Flask(__name__)

# Global değişkenler
detector = None
counter = None
rtsp_camera = None
is_running = False
current_config = {
    'detection_threshold': 0.4,
    'model_path': 'yolov8n.pt'
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

def initialize_system():
    """Sistemi başlatır"""
    global detector, counter, rtsp_camera
    
    # Detector'ı başlat
    detector = HumanDetector(model_path=current_config['model_path'])
    
    # Counter'ı başlat
    counter = HumanCounter(
        device_id=Config.DEVICE_ID,
        location=Config.LOCATION
    )
    
    # RTSP kamera başlat
    rtsp_camera = RTSPCamera()
    if rtsp_camera.connect():
        rtsp_camera.start_capture()
        logger.info("RTSP kamera başlatıldı")
    else:
        logger.error("RTSP kamera başlatılamadı!")
        return False
    
    logger.info("Sistem başlatıldı")
    return True

def cleanup_system():
    """Sistemi temizler"""
    global rtsp_camera
    
    if rtsp_camera:
        rtsp_camera.stop_capture()
        logger.info("RTSP kamera durduruldu")
    
    logger.info("Sistem temizlendi")

def generate_frames():
    """Video frame'lerini üretir"""
    global rtsp_camera, detector, counter, is_running
    
    while is_running:
        if rtsp_camera:
            ret, frame = rtsp_camera.read()
            if ret and frame is not None:
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
                
                # RTSP bilgisi
                cv2.putText(frame, f'RTSP: {Config.RTSP_IP}:{Config.RTSP_PORT}', 
                           (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                # Tarih ve saat
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cv2.putText(frame, current_time, 
                           (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                # Frame'i JPEG formatına çevir
                ret, buffer = cv2.imencode('.jpg', frame)
                if ret:
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            time.sleep(0.033)  # ~30 FPS
        else:
            time.sleep(1)

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video stream endpoint'i"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/start', methods=['POST'])
def start_system():
    """Sistemi başlatır"""
    global is_running
    
    if not is_running:
        if initialize_system():
            is_running = True
            return jsonify({'status': 'success', 'message': 'Sistem başlatıldı'})
        else:
            return jsonify({'status': 'error', 'message': 'Sistem başlatılamadı'})
    else:
        return jsonify({'status': 'info', 'message': 'Sistem zaten çalışıyor'})

@app.route('/api/stop', methods=['POST'])
def stop_system():
    """Sistemi durdurur"""
    global is_running
    
    if is_running:
        is_running = False
        cleanup_system()
        return jsonify({'status': 'success', 'message': 'Sistem durduruldu'})
    else:
        return jsonify({'status': 'info', 'message': 'Sistem zaten durmuş'})

@app.route('/api/status')
def get_status():
    """Sistem durumunu döndürür"""
    global is_running, rtsp_camera, counter
    
    status = {
        'running': is_running,
        'rtsp_connected': rtsp_camera.is_running if rtsp_camera else False,
        'rtsp_url': Config.RTSP_URL,
        'rtsp_ip': Config.RTSP_IP,
        'rtsp_port': Config.RTSP_PORT,
        'rtsp_encoding': Config.RTSP_ENCODING
    }
    
    if counter:
        status.update({
            'hourly_count': counter.hourly_count,
            'daily_count': counter.daily_count,
            'total_count': counter.total_count,
            'active_people': len(counter.active_people)
        })
    
    return jsonify(status)

@app.route('/api/counts')
def get_counts():
    """Sayım verilerini döndürür"""
    global counter
    
    if counter:
        return jsonify({
            'hourly_count': counter.hourly_count,
            'daily_count': counter.daily_count,
            'total_count': counter.total_count,
            'active_people': len(counter.active_people),
            'timestamp': datetime.now().isoformat()
        })
    else:
        return jsonify({'error': 'Counter başlatılmamış'})

@app.route('/api/config', methods=['GET', 'POST'])
def handle_config():
    """Konfigürasyon ayarlarını yönetir"""
    global current_config
    
    if request.method == 'POST':
        data = request.get_json()
        current_config.update(data)
        return jsonify({'status': 'success', 'message': 'Konfigürasyon güncellendi'})
    else:
        return jsonify(current_config)

if __name__ == '__main__':
    # Logging ayarları
    logger = setup_logging()
    
    # Flask uygulamasını başlat
    logger.info("Web UI başlatılıyor...")
    logger.info(f"RTSP URL: {Config.RTSP_URL}")
    
    app.run(host='0.0.0.0', port=5000, debug=False) 