from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.api import router as api_router

# FastAPI uygulamasını oluştur
app = FastAPI(
    title="GlobalProVision API",
    description="Görüntü işleme tabanlı nesne algılama API'si",
    version="1.0.0",
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
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/v1/health",
            "detected_objects": "/api/v1/detected-objects",
            "test_detection": "/api/v1/detected-objects/test",
            "available_objects": "/api/v1/detected-objects/available",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 