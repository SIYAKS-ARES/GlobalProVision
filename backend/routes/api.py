from fastapi import APIRouter, HTTPException
from typing import Dict, List
from data.dummy_data import DummyDetectionService
from services.hybrid_detection_service import HybridDetectionService
import logging

# Logging konfigürasyonu
logger = logging.getLogger(__name__)

# API router'ını oluştur
router = APIRouter()

# Hibrit detection servisini başlat
hybrid_service = HybridDetectionService()

@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    API'nin sağlık durumunu kontrol eder.

    Returns:
        dict: API'nin durumu
    """
    return {"status": "ok"}


@router.get("/detected-objects")
async def get_detected_objects() -> Dict:
    """
    Anlık olarak algılanan nesneleri döner.
    Şu an dummy veri kullanıyor, ileride gerçek detection servisi bağlanacak.

    Returns:
        dict: Timestamp ve algılanan nesneleri içeren veri
    """
    try:
        detection_result = DummyDetectionService.get_detected_objects()
        return detection_result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Detection servisi hatası: {str(e)}"
        )


@router.get("/detected-objects/test")
async def test_detection(objects: str = "Bıçak,Telefon") -> Dict:
    """
    Test amaçlı endpoint - belirli nesnelerin algılandığını simüle eder.

    Args:
        objects: Virgülle ayrılmış nesne listesi (örn: "Bıçak,Telefon,Kalem")

    Returns:
        dict: Timestamp ve belirtilen nesneleri içeren veri
    """
    try:
        # Virgülle ayrılmış string'i listeye çevir
        object_list = [obj.strip() for obj in objects.split(",")]
        detection_result = DummyDetectionService.get_specific_detection(object_list)
        return detection_result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Test detection hatası: {str(e)}"
        )


@router.get("/detected-objects/available")
async def get_available_objects() -> Dict[str, List[str]]:
    """
    Algılanabilir nesnelerin listesini döner.

    Returns:
        dict: Mevcut algılanabilir nesneler
    """
    return {
        "available_objects": DummyDetectionService.DETECTABLE_OBJECTS,
        "total_count": len(DummyDetectionService.DETECTABLE_OBJECTS)
    }
