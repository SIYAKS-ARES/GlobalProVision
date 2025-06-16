import requests
import json
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Logging konfigürasyonu
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DetectionService:
    """
    Detection modülünden gerçek zamanlı veri çeken servis sınıfı.
    Flask tabanlı detection uygulamasından /data_feed endpoint'ini kullanır.
    """
    
    def __init__(self, detection_host: str = "localhost", detection_port: int = 5000):
        """
        Detection servisini başlatır.
        
        Args:
            detection_host: Detection Flask uygulamasının host adresi
            detection_port: Detection Flask uygulamasının port numarası
        """
        self.detection_url = f"http://{detection_host}:{detection_port}/data_feed"
        self.last_known_data = {}
        
        # Nesne adı çevirileri (İngilizce -> Türkçe)
        self.object_translations = {
            'knife': 'Bıçak',
            'gun': 'Silah', 
            'scissors': 'Makas',
            'person': 'İnsan',
            'phone': 'Telefon',
            'cell phone': 'Telefon',
            'pen': 'Kalem',
            'pencil': 'Kalem',
            'bottle': 'Şişe',
            'cup': 'Bardak',
            'book': 'Kitap'
        }
    
    def _translate_object_name(self, english_name: str) -> str:
        """
        İngilizce nesne adını Türkçeye çevirir.
        
        Args:
            english_name: İngilizce nesne adı
            
        Returns:
            str: Türkçe nesne adı
        """
        return self.object_translations.get(english_name.lower(), english_name.title())
    
    def get_detected_objects(self) -> Dict:
        """
        Detection modülünden gerçek zamanlı veri çeker ve frontend formatına dönüştürür.
        
        Returns:
            dict: Frontend için formatlanmış detection verisi
        """
        try:
            # Detection modülünden veri çek
            response = requests.get(self.detection_url, timeout=5)
            response.raise_for_status()
            
            detection_data = response.json()
            logger.info(f"Detection modülünden alınan veri: {detection_data}")
            
            # Veriyi frontend formatına dönüştür
            detected_objects = []
            
            if 'detection_results' in detection_data and 'nesneler' in detection_data['detection_results']:
                for obj_name, count in detection_data['detection_results']['nesneler'].items():
                    # Türkçe çeviri yap
                    translated_name = self._translate_object_name(obj_name)
                    
                    # Her nesneyi count kadar ekle
                    for _ in range(count):
                        detected_objects.append(translated_name)
            
            # Formatlanmış veriyi hazırla
            formatted_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "detected": detected_objects,
                "danger_percentage": detection_data.get('danger_percentage', 0),
                "person_count": detection_data.get('detection_results', {}).get('insan_sayisi', 0)
            }
            
            # Son bilinen veriyi güncelle
            self.last_known_data = formatted_data
            
            return formatted_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Detection modülüne bağlanırken hata: {e}")
            
            # Bağlantı hatası durumunda son bilinen veriyi dön
            if self.last_known_data:
                logger.info("Son bilinen veri döndürülüyor")
                return {
                    **self.last_known_data,
                    "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                    "status": "connection_error"
                }
            
            # Hiç veri yoksa boş dön
            return {
                "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "detected": [],
                "danger_percentage": 0,
                "person_count": 0,
                "status": "detection_service_unavailable"
            }
            
        except Exception as e:
            logger.error(f"Beklenmeyen hata: {e}")
            return {
                "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "detected": [],
                "danger_percentage": 0,
                "person_count": 0,
                "status": "error",
                "error_message": str(e)
            }
    
    def health_check(self) -> bool:
        """
        Detection modülünün çalışır durumda olup olmadığını kontrol eder.
        
        Returns:
            bool: Detection modülü erişilebilir ise True
        """
        try:
            response = requests.get(self.detection_url, timeout=3)
            return response.status_code == 200
        except:
            return False 