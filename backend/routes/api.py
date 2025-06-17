from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List
from services.detection_service import DetectionService
import logging

# Logging konfigürasyonu
logger = logging.getLogger(__name__)

# API router'ını oluştur
router = APIRouter()

# Detection servisini başlat
detection_service = DetectionService()

@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    API'nin ve detection modülünün sağlık durumunu kontrol eder.
    
    Returns:
        dict: API ve detection modülünün durumu
    """
    detection_status = detection_service.health_check()
    
    return {
        "status": "ok",
        "detection_service": "connected" if detection_status else "disconnected",
        "timestamp": detection_service.get_detected_objects()["timestamp"]
    }


@router.get("/detected-objects")
async def get_detected_objects() -> Dict:
    """
    Detection modülünden gerçek zamanlı olarak algılanan nesneleri döner.
    Frontend bu endpoint'i sürekli çağırarak güncel verileri alacak.
    
    Returns:
        dict: Timestamp, algılanan nesneler, risk analizi ve kişi sayısı
    """
    try:
        detection_result = detection_service.get_detected_objects()
        logger.info(f"Frontend'e gönderilen veri: {detection_result}")
        return detection_result
        
    except Exception as e:
        logger.error(f"Detection servisi hatası: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Detection servisi hatası: {str(e)}"
        )


@router.get("/detected-objects/risk")
async def get_risk_analysis() -> Dict:
    """
    Sadece risk analizi verilerini döner.
    
    Returns:
        dict: Risk yüzdesi ve tehlike durumu
    """
    try:
        detection_result = detection_service.get_detected_objects()
        
        risk_level = "DÜŞÜK"
        if detection_result["danger_percentage"] > 70:
            risk_level = "YÜKSEK"
        elif detection_result["danger_percentage"] > 30:
            risk_level = "ORTA"
        
        return {
            "timestamp": detection_result["timestamp"],
            "danger_percentage": detection_result["danger_percentage"],
            "risk_level": risk_level,
            "person_count": detection_result["person_count"],
            "detected_dangerous_objects": [
                obj for obj in detection_result["detected"] 
                if obj in ["Bıçak", "Silah", "Makas"]
            ]
        }
        
    except Exception as e:
        logger.error(f"Risk analizi hatası: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Risk analizi hatası: {str(e)}"
        )


@router.get("/detected-objects/summary")
async def get_detection_summary() -> Dict:
    """
    Algılanan nesnelerin özet halini döner.
    
    Returns:
        dict: Nesne sayıları ve genel durum
    """
    try:
        detection_result = detection_service.get_detected_objects()
        
        # Nesneleri say
        object_counts = {}
        for obj in detection_result["detected"]:
            object_counts[obj] = object_counts.get(obj, 0) + 1
        
        return {
            "timestamp": detection_result["timestamp"],
            "total_objects": len(detection_result["detected"]),
            "object_counts": object_counts,
            "person_count": detection_result["person_count"],
            "danger_percentage": detection_result["danger_percentage"],
            "unique_objects": len(object_counts)
        }
        
    except Exception as e:
        logger.error(f"Özet veri hatası: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Özet veri hatası: {str(e)}"
        )


@router.get("/detection-status")
async def get_detection_status() -> Dict:
    """
    Detection modülünün durumu hakkında detaylı bilgi döner.
    
    Returns:
        dict: Detection modülü bağlantı durumu
    """
    detection_online = detection_service.health_check()
    
    return {
        "detection_service_online": detection_online,
        "detection_url": detection_service.detection_url,
        "last_update": detection_service.get_detected_objects()["timestamp"],
        "status": "operational" if detection_online else "offline"
    }
