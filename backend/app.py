from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.api import router as api_router
import logging

# Logging konfigürasyonu
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI uygulamasını oluştur
app = FastAPI(
    title="GlobalProVision API",
    description="Gerçek zamanlı görüntü işleme tabanlı nesne algılama API'si",
    version="2.0.0",
)

# CORS middleware ekle (frontend bağlantısı için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Üretimde specific domainler kullanılmalı
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API router'ını ekle
app.include_router(api_router, prefix="/api/v1")

# Ana endpoint
@app.get("/")
async def root():
    """
    Ana endpoint - API bilgilerini döner.
    """
    return {
        "message": "GlobalProVision API'sine hoş geldiniz!",
        "version": "2.0.0",
        "description": "Gerçek zamanlı nesne algılama ve risk analizi API'si",
        "endpoints": {
            "health": "/api/v1/health",
            "detected_objects": "/api/v1/detected-objects",
            "risk_analysis": "/api/v1/detected-objects/risk",
            "detection_summary": "/api/v1/detected-objects/summary",
            "detection_status": "/api/v1/detection-status",
            "docs": "/docs"
        },
        "integration": {
            "detection_module": "Flask uygulaması (port 5000)",
            "data_source": "Gerçek zamanlı kamera verisi",
            "update_frequency": "Sürekli"
        }
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("GlobalProVision API başlatılıyor...")
    logger.info("Detection modülünün port 5000'de çalıştığından emin olun")
    uvicorn.run(app, host="0.0.0.0", port=8000)
