import requests
import json
from datetime import datetime
from typing import Dict, List, Optional
import logging
from data.dummy_data import DummyDetectionService

# Logging konfigürasyonu
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HybridDetectionService:
    """
    Hibrit detection servisi - gerçek detection modülü çalışırsa onu kullanır,
    çalışmazsa dummy data'ya geçer. Detection modülünde değişiklik gerektirmez.
    """
    
    def __init__(self, detection_ports: List[int] = [5000, 5001]):
        """
        Hibrit servisi başlatır.
        
        Args:
            detection_ports: Deneyeceği port listesi (5000 AirPlay, 5001 alternatif)
        """
        self.detection_ports = detection_ports
        self.active_detection_url = None
        self.last_known_data = {}
        self.detection_online = False
        
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
        
        # Başlangıçta hangi portta detection çalıştığını bul
        self._discover_detection_service()
    
    def _discover_detection_service(self):
        """
        Detection modülünün hangi portta çalıştığını bulur.
        """
        for port in self.detection_ports:
            try:
                url = f"http://localhost:{port}/data_feed"
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    self.active_detection_url = url
                    self.detection_online = True
                    logger.info(f"✅ Detection modülü bulundu: port {port}")
                    return
            except:
                continue
        
        self.detection_online = False
        logger.warning("⚠️ Detection modülü bulunamadı, dummy mode aktif")
    
    def _translate_object_name(self, english_name: str) -> str:
        """
        İngilizce nesne adını Türkçeye çevirir.
        """
        return self.object_translations.get(english_name.lower(), english_name.title())
    
    def _try_real_detection(self) -> Optional[Dict]:
        """
        Gerçek detection modülünden veri çekmeyi dener.
        """
        if not self.active_detection_url:
            return None
            
        try:
            response = requests.get(self.active_detection_url, timeout=3)
            response.raise_for_status()
            
            detection_data = response.json()
            logger.info(f"🔍 Detection modülünden alınan veri: {detection_data}")
            
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
                "person_count": detection_data.get('detection_results', {}).get('insan_sayisi', 0),
                "source": "real_detection",
                "detection_port": self.active_detection_url.split(':')[-1].split('/')[0]
            }
            
            # Son bilinen veriyi güncelle
            self.last_known_data = formatted_data
            self.detection_online = True
            
            return formatted_data
            
        except Exception as e:
            logger.warning(f"⚠️ Detection modülü hatası: {e}")
            self.detection_online = False
            return None
    
    def get_detected_objects(self) -> Dict:
        """
        Ana method - önce gerçek detection'ı dener, olmazsa dummy data kullanır.
        """
        # Önce gerçek detection'ı dene
        real_data = self._try_real_detection()
        if real_data:
            return real_data
        
        # Gerçek detection çalışmıyorsa dummy data kullan
        logger.info("🤖 Dummy data modu aktif")
        dummy_data = DummyDetectionService.get_detected_objects()
        
        # Dummy data'ya kaynak bilgisi ekle
        dummy_data.update({
            "source": "dummy_data",
            "detection_port": "none",
            "danger_percentage": 0,
            "person_count": 0
        })
        
        return dummy_data
    
    def health_check(self) -> Dict:
        """
        Sistem durumunu kontrol eder.
        """
        # Detection servisini yeniden keşfet
        if not self.detection_online:
            self._discover_detection_service()
        
        return {
            "detection_online": self.detection_online,
            "active_port": self.active_detection_url.split(':')[-1].split('/')[0] if self.active_detection_url else "none",
            "mode": "real_detection" if self.detection_online else "dummy_data",
            "available_ports": self.detection_ports
        }
    
    def force_dummy_mode(self) -> Dict:
        """
        Test amaçlı - zorla dummy mode'a geçer.
        """
        logger.info("🔧 Zorla dummy mode aktif")
        dummy_data = DummyDetectionService.get_detected_objects()
        dummy_data.update({
            "source": "forced_dummy_data",
            "detection_port": "none",
            "danger_percentage": 0,
            "person_count": 0
        })
        return dummy_data 