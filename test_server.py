#!/usr/bin/env python3
"""
Test endpoint sunucusu - Geliştirme ve test için basit bir Flask sunucusu
"""

from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# Gelen verileri saklamak için basit bir liste
received_data = []

@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'message': 'Human Counter API is running'
    })

@app.route('/api/count', methods=['POST'])
def receive_count():
    """
    Sayım verilerini alan endpoint
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Veriyi logla
        print(f"📊 Yeni veri alındı: {json.dumps(data, indent=2)}")
        
        # Veriyi listeye ekle
        received_data.append({
            'received_at': datetime.now().isoformat(),
            'data': data
        })
        
        # Son 100 veriyi tut
        if len(received_data) > 100:
            received_data.pop(0)
        
        return jsonify({
            'status': 'success',
            'message': 'Data received successfully',
            'timestamp': datetime.now().isoformat(),
            'received_count': len(received_data)
        })
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/data', methods=['GET'])
def get_data():
    """
    Alınan verileri görüntüleme endpoint'i
    """
    return jsonify({
        'total_received': len(received_data),
        'data': received_data
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    İstatistik endpoint'i
    """
    if not received_data:
        return jsonify({
            'message': 'No data received yet',
            'total_received': 0
        })
    
    # Son 24 saatteki verileri filtrele
    from datetime import timedelta
    cutoff_time = datetime.now() - timedelta(hours=24)
    
    recent_data = [
        item for item in received_data 
        if datetime.fromisoformat(item['received_at']) > cutoff_time
    ]
    
    # Saatlik toplamları hesapla
    hourly_totals = {}
    for item in recent_data:
        hour = datetime.fromisoformat(item['received_at']).strftime('%Y-%m-%d %H:00')
        count = item['data'].get('hourly_count', 0)
        hourly_totals[hour] = hourly_totals.get(hour, 0) + count
    
    return jsonify({
        'total_received': len(received_data),
        'recent_24h': len(recent_data),
        'hourly_totals': hourly_totals,
        'last_received': received_data[-1]['received_at'] if received_data else None
    })

@app.route('/', methods=['GET'])
def index():
    """
    Ana sayfa
    """
    return jsonify({
        'service': 'Human Counter API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'receive_data': '/api/count (POST)',
            'view_data': '/api/data',
            'stats': '/api/stats'
        },
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Test endpoint sunucusu başlatılıyor...")
    print("📍 URL: http://localhost:8000")
    print("📊 Health check: http://localhost:8000/health")
    print("📈 Veri görüntüleme: http://localhost:8000/api/data")
    print("📊 İstatistikler: http://localhost:8000/api/stats")
    print("\nÇıkmak için Ctrl+C")
    
    app.run(host='0.0.0.0', port=8000, debug=True) 