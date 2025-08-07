import requests
import json
import time
from datetime import datetime
from config import Config
import logging

class EndpointClient:
    def __init__(self):
        """
        Endpoint ile iletişim kuracak client
        """
        self.url = Config.ENDPOINT_URL
        self.api_key = Config.ENDPOINT_API_KEY
        self.timeout = Config.ENDPOINT_TIMEOUT
        
        # Logging ayarları
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{Config.LOG_DIR}/endpoint.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def send_count_data(self, count_data):
        """
        Sayım verilerini endpoint'e gönderir
        """
        try:
            headers = {
                'Content-Type': 'application/json'
            }
            
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
            
            payload = {
                'timestamp': datetime.now().isoformat(),
                'hourly_count': count_data['hourly_count'],
                'daily_count': count_data['daily_count'],
                'total_count': count_data['total_count'],
                'device_id': count_data.get('device_id', 'default'),
                'location': count_data.get('location', 'unknown')
            }
            
            self.logger.info(f"Endpoint'e veri gönderiliyor: {payload}")
            
            response = requests.post(
                self.url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                self.logger.info(f"Veri başarıyla gönderildi. Response: {response.json()}")
                return True, response.json()
            else:
                self.logger.error(f"Endpoint hatası: {response.status_code} - {response.text}")
                return False, response.text
                
        except requests.exceptions.Timeout:
            self.logger.error("Endpoint timeout hatası")
            return False, "Timeout"
        except requests.exceptions.ConnectionError:
            self.logger.error("Endpoint bağlantı hatası")
            return False, "Connection Error"
        except Exception as e:
            self.logger.error(f"Endpoint gönderim hatası: {e}")
            return False, str(e)
    
    def test_connection(self):
        """
        Endpoint bağlantısını test eder
        """
        try:
            headers = {}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
                
            response = requests.get(
                self.url.replace('/api/count', '/health'),
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                self.logger.info("Endpoint bağlantısı başarılı")
                return True
            else:
                self.logger.warning(f"Endpoint test hatası: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Endpoint test hatası: {e}")
            return False 