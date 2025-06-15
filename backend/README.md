# 🔥 GlobalProVision Backend API

GlobalProVision projesi için gerçek zamanlı nesne algılama ve risk analizi API'si.

## 🏗️ Mimari

```
Detection Modülü (Flask:5000) → Backend API (FastAPI:8000) → Frontend
```

- **Detection Modülü**: YOLO tabanlı görüntü işleme (Flask, port 5000)
- **Backend API**: RESTful API servisi (FastAPI, port 8000)
- **Frontend**: Web arayüzü (API'den veri çekecek)

## 📁 Klasör Yapısı

```
backend/
├── app.py                    # Ana FastAPI uygulaması
├── requirements.txt          # Python bağımlılıkları
├── test_api.py              # API test scripti
├── services/
│   ├── __init__.py
│   └── detection_service.py  # Detection modülü entegrasyonu
└── routes/
    ├── __init__.py
    └── api.py               # API endpoint'leri
```

## 🚀 Kurulum ve Çalıştırma

### 1. Bağımlılıkları Yükle

```bash
cd backend
pip install -r requirements.txt
```

### 2. Detection Modülünü Başlat

**Önemli**: Backend API'si çalışmadan önce detection modülü çalışıyor olmalı!

```bash
# Başka bir terminal penceresinde
cd detection
python app.py
# Detection modülü port 5000'de çalışacak
```

### 3. Backend API'sini Başlat

```bash
cd backend
python app.py
# API port 8000'de çalışacak
```

### 4. Test Et

```bash
python test_api.py
```

## 🔗 API Endpoint'leri

### 🏠 Ana Endpoint

- **GET** `/` - API bilgileri ve endpoint listesi

### 🩺 Sağlık Kontrolü

- **GET** `/api/v1/health` - API ve detection modülü durumu

```json
{
  "status": "ok",
  "detection_service": "connected",
  "timestamp": "2025-01-14T17:35:00"
}
```

### 🎯 Nesne Algılama (Ana Endpoint)

- **GET** `/api/v1/detected-objects` - Gerçek zamanlı algılanan nesneler

```json
{
  "timestamp": "2025-01-14T17:35:00",
  "detected": ["Bıçak", "Kalem", "Telefon"],
  "danger_percentage": 75.5,
  "person_count": 2
}
```

### ⚠️ Risk Analizi

- **GET** `/api/v1/detected-objects/risk` - Sadece risk verileri

```json
{
  "timestamp": "2025-01-14T17:35:00",
  "danger_percentage": 75.5,
  "risk_level": "YÜKSEK",
  "person_count": 2,
  "detected_dangerous_objects": ["Bıçak"]
}
```

### 📊 Detection Özeti

- **GET** `/api/v1/detected-objects/summary` - Nesne sayıları özeti

```json
{
  "timestamp": "2025-01-14T17:35:00",
  "total_objects": 5,
  "object_counts": {
    "Bıçak": 1,
    "Kalem": 2,
    "Telefon": 2
  },
  "person_count": 2,
  "danger_percentage": 75.5,
  "unique_objects": 3
}
```

### 🔌 Detection Modül Durumu

- **GET** `/api/v1/detection-status` - Detection modülü bağlantı durumu

## 🖥️ Frontend Entegrasyonu

Frontend geliştiricisi için örnek kullanım:

### JavaScript (Fetch API)

```javascript
// Ana detection verilerini çek
async function getDetectedObjects() {
    try {
        const response = await fetch('http://localhost:8000/api/v1/detected-objects');
        const data = await response.json();
      
        console.log('Algılanan nesneler:', data.detected);
        console.log('Risk yüzdesi:', data.danger_percentage);
      
        return data;
    } catch (error) {
        console.error('API hatası:', error);
    }
}

// Sürekli güncelleme (her 500ms)
setInterval(getDetectedObjects, 500);
```

### JavaScript (Axios)

```javascript
// Risk analizi verilerini çek
async function getRiskAnalysis() {
    try {
        const response = await axios.get('http://localhost:8000/api/v1/detected-objects/risk');
      
        updateRiskUI(response.data);
      
    } catch (error) {
        console.error('Risk analizi hatası:', error);
    }
}
```

## 🔧 Konfigürasyon

### Detection Modülü Ayarları

`services/detection_service.py` dosyasında:

```python
# Detection modülü adresi değiştirilebilir
detection_service = DetectionService(
    detection_host="localhost",  # Detection modülü host'u
    detection_port=5000         # Detection modülü port'u
)
```

### Nesne Çevirileri

İngilizce nesne adları otomatik olarak Türkçeye çevrilir:

- `knife` → `Bıçak`
- `gun` → `Silah`
- `scissors` → `Makas`
- `phone` → `Telefon`

## 📈 Performans

- **Yanıt Süresi**: ~50-100ms
- **Güncelleme Sıklığı**: Gerçek zamanlı (detection modülüne bağlı)
- **Hata Toleransı**: Detection modülü çalışmazsa son bilinen veri döner

## 🛠️ Geliştirme

### Yeni Endpoint Ekleme

1. `routes/api.py` dosyasına yeni endpoint ekle
2. Gerekirse `services/detection_service.py` dosyasını güncelle
3. Test scripti ile test et

### Loglama

Tüm API çağrıları ve hatalar loglanır:

```bash
INFO:     Detection modülünden alınan veri: {...}
INFO:     Frontend'e gönderilen veri: {...}
ERROR:    Detection modülüne bağlanırken hata: ...
```

## 🚨 Sorun Giderme

### API Çalışmıyor

```bash
# Port kontrolü
lsof -i :8000

# Log kontrolü
python app.py
```

### Detection Modülüne Bağlanamıyor

```bash
# Detection modülü çalışıyor mu?
curl http://localhost:5000/data_feed

# Health check
curl http://localhost:8000/api/v1/health
```

### CORS Hataları

FastAPI'de CORS ayarları zaten yapılandırıldı. Frontend farklı port'ta çalışıyorsa sorun olmayacak.

## 📚 Dokümantasyon

API çalışırken otomatik dokümantasyon:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
