# GlobalProVision

Bu proje, GLOBALPROJOB AI HUB kapsamında geliştirilen bir deneme projesidir.

## 📂 Sorumluluklara Göre Klasörler

- `backend/`: API yapısı
- `detection/`: Görüntü işleme modelleri
- `frontend/`: Web UI
- `integration/`: Sistem entegrasyon testleri
- `docs/`: UX düzenlemeleri ve proje dökümantasyonu

## 🚀 İlk Checkpoint: Pazartesi

## 🎯 Proje Amacı

Web arayüzü üzerinden kamera görüntüsünden algılanan **bıçak, telefon, kalem** gibi nesneleri metin olarak göstermek ve risk analizi yapmak.

## 🏗️ Sistem Mimarisi

```
Kamera → Detection Modülü (YOLO/Flask:5000) → Backend API (FastAPI:8000) → Frontend (Web UI)
```

## 📋 Proje Durumu

### ✅ Tamamlanan Modüller:

#### 🔍 Detection Modülü (`detection/`)
- ✅ YOLO tabanlı nesne algılama
- ✅ Gerçek zamanlı kamera görüntüsü işleme
- ✅ Tehlikeli nesne tespiti (bıçak, silah, makas)
- ✅ Risk yüzdesi hesaplama
- ✅ Flask web arayüzü (port 5000)
- ✅ `/data_feed` API endpoint'i

#### 🌐 Backend API (`backend/`)
- ✅ FastAPI tabanlı RESTful API (port 8000)
- ✅ Detection modülü entegrasyonu
- ✅ Gerçek zamanlı veri aktarımı
- ✅ CORS desteği (frontend bağlantısı için)
- ✅ Hata toleransı ve logging
- ✅ Otomatik API dokümantasyonu

### 📋 Bekleyen Modüller:
- 🔄 Frontend Web UI (`frontend/`)
- 🔄 Sistem entegrasyon testleri (`integration/`)

## 🔗 API Endpoint'leri

Backend API şu endpoint'leri sağlıyor:

### Ana Detection Endpoint:
```bash
GET http://localhost:8000/api/v1/detected-objects
```
**Örnek Yanıt:**
```json
{
  "timestamp": "2025-01-14T17:35:00",
  "detected": ["Bıçak", "Kalem", "Telefon"]
}
```

### Diğer Endpoint'ler:
- `GET /api/v1/health` - Sistem sağlık kontrolü
- `GET /api/v1/detected-objects/test` - Test amaçlı simülasyon
- `GET /api/v1/detected-objects/available` - Algılanabilir nesneler listesi
- `GET /docs` - Otomatik API dokümantasyonu

## 🚀 Kurulum ve Çalıştırma

### 1. Detection Modülü:
```bash
cd detection
pip install -r requirements.txt
python app.py  # Port 5000'de çalışır
```

### 2. Backend API:
```bash
cd backend
pip install -r requirements.txt
python app.py  # Port 8000'de çalışır
```

### 3. Test:
```bash
# Detection modülü test
curl http://localhost:5000/data_feed

# Backend API test
curl http://localhost:8000/api/v1/detected-objects
```

## 🖥️ Frontend Entegrasyonu

Frontend geliştiricisi için hazır API:

```javascript
// Gerçek zamanlı veri çekme
async function getDetectedObjects() {
    const response = await fetch('http://localhost:8000/api/v1/detected-objects');
    const data = await response.json();
    
    console.log('Algılanan nesneler:', data.detected);
    console.log('Zaman damgası:', data.timestamp);
    
    return data;
}

// Her 500ms'de güncelle
setInterval(getDetectedObjects, 500);
```

## 🔧 Teknik Detaylar

### Detection Modülü:
- **Framework**: Flask + OpenCV + Ultralytics YOLO
- **Model**: YOLOv8n.pt
- **Algılanan Nesneler**: knife, gun, scissors, person, phone, pen vb.
- **Risk Hesaplama**: Tehlikeli nesne + insan sayısı bazlı

### Backend API:
- **Framework**: FastAPI + Pydantic
- **Port**: 8000
- **Veri Formatı**: JSON
- **Güncellik**: Gerçek zamanlı (detection modülünden çeker)
- **Dil Desteği**: Otomatik İngilizce → Türkçe çeviri

## ✅ Ortak Git Kullanımı:

- Herkes kendi sorumluluğu için ilgili brancht'e çalışır.
- Çalışmaya başlamadan önce:
  git fetch
  git rebase origin/main
- Bitince:
  git pull --rebase origin/main
  git push origin `<branch>`
- PR üzerinden merge yapılır. main'e doğrudan yazılmaz.

## 📈 Sonraki Adımlar

1. **Frontend Geliştirme**: React/Vue.js ile web arayüzü
2. **Kamera Feed Entegrasyonu**: Backend'den video stream
3. **Real-time Updates**: WebSocket veya Server-Sent Events
4. **Production Deployment**: Docker containerization
5. **Güvenlik**: Authentication ve rate limiting
