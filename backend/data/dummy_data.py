import random
from datetime import datetime
from typing import List


class DummyDetectionService:
    """
    Gerçek detection modülü hazır olana kadar kullanılacak dummy veri sağlayıcısı.
    İleride bu sınıf gerçek detection servisi ile değiştirilecek.
    """
    
    # Algılanabilir nesneler listesi
    DETECTABLE_OBJECTS = ["Bıçak", "Telefon", "Kalem"]
    
    @staticmethod
    def get_detected_objects() -> dict:
        """
        Rastgele dummy detection verisi döner.
        
        Returns:
            dict: Timestamp ve algılanan nesneleri içeren sözlük
        """
        # Rastgele 0-3 arası nesne seç
        num_objects = random.randint(0, 3)
        detected_objects = random.sample(
            DummyDetectionService.DETECTABLE_OBJECTS, 
            num_objects
        )
        
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "detected": detected_objects
        }
    
    @staticmethod
    def get_specific_detection(objects: List[str]) -> dict:
        """
        Belirli nesnelerin algılandığını simüle eder.
        Test amaçlı kullanılabilir.
        
        Args:
            objects: Algılandığı varsayılan nesneler listesi
            
        Returns:
            dict: Timestamp ve belirtilen nesneleri içeren sözlük
        """
        # Sadece geçerli nesneleri filtrele
        valid_objects = [
            obj for obj in objects 
            if obj in DummyDetectionService.DETECTABLE_OBJECTS
        ]
        
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "detected": valid_objects
        } 