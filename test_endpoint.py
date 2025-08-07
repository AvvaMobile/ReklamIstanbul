#!/usr/bin/env python3
"""
Endpoint test script - Endpoint bağlantısını test etmek için
"""

import requests
import json
from datetime import datetime
from config import Config

def test_endpoint():
    """
    Endpoint bağlantısını test eder
    """
    print("Endpoint test başlatılıyor...")
    print(f"URL: {Config.ENDPOINT_URL}")
    print(f"API Key: {'*' * len(Config.ENDPOINT_API_KEY) if Config.ENDPOINT_API_KEY else 'Yok'}")
    
    # Test verisi
    test_data = {
        'timestamp': datetime.now().isoformat(),
        'hourly_count': 15,
        'daily_count': 120,
        'total_count': 1000,
        'device_id': 'test_device',
        'location': 'test_location'
    }
    
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        
        if Config.ENDPOINT_API_KEY:
            headers['Authorization'] = f'Bearer {Config.ENDPOINT_API_KEY}'
        
        print(f"\nGönderilen veri:")
        print(json.dumps(test_data, indent=2))
        
        response = requests.post(
            Config.ENDPOINT_URL,
            json=test_data,
            headers=headers,
            timeout=Config.ENDPOINT_TIMEOUT
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Endpoint test başarılı!")
            try:
                print(f"Response Body: {response.json()}")
            except:
                print(f"Response Text: {response.text}")
        else:
            print("❌ Endpoint test başarısız!")
            print(f"Error: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Timeout hatası - Endpoint yanıt vermiyor")
    except requests.exceptions.ConnectionError:
        print("❌ Bağlantı hatası - Endpoint erişilemiyor")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")

def test_health_endpoint():
    """
    Health endpoint'ini test eder
    """
    try:
        health_url = Config.ENDPOINT_URL.replace('/api/count', '/health')
        print(f"\nHealth endpoint test: {health_url}")
        
        headers = {}
        if Config.ENDPOINT_API_KEY:
            headers['Authorization'] = f'Bearer {Config.ENDPOINT_API_KEY}'
        
        response = requests.get(health_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Health endpoint çalışıyor")
            print(f"Response: {response.text}")
        else:
            print(f"❌ Health endpoint hatası: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Health endpoint test hatası: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("ENDPOINT TEST SCRIPT")
    print("=" * 50)
    
    test_health_endpoint()
    test_endpoint()
    
    print("\n" + "=" * 50)
    print("Test tamamlandı")
    print("=" * 50) 