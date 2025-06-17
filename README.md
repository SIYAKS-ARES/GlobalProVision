# GlobalProVision

Bu proje, GLOBALPROJOB AI HUB kapsamında geliştirilen bir **nesne algılama ve güvenlik analizi sistemidir**. 

🎯 **Proje tamamlandı!** Kamera görüntülerinden tehlikeli nesneleri algılayan, gerçek zamanlı risk analizi yapan tam fonksiyonel bir sistem.

## 📂 Sorumluluklara Göre Klasörler

### 🎯 Ana Modüller

- **`backend/`**: FastAPI tabanlı REST API servisi
  - `app.py`: Ana uygulama dosyası (FastAPI server)
  - `routes/`: API endpoint'leri ve routing mantığı
  - `services/`: İş mantığı ve detection entegrasyonu
  - `data/`: Test verileri ve dummy data
  - `test_*.py`: Unit ve integration testleri

- **`detection/`**: YOLO tabanlı görüntü işleme modülü
  - `app.py`: Flask tabanlı detection server
  - `models/`: YOLOv8 model dosyaları (yolov8n.pt)
  - `templates/`: Web arayüzü şablonları
  - `danger_threshold.py`: Risk analizi algoritması

- **`frontend/`**: React tabanlı web kullanıcı arayüzü
  - React 19.1.0 + modern JavaScript
  - Gerçek zamanlı veri görselleştirme
  - Responsive tasarım

- **`integration/`**: Sistem entegrasyon testleri
  - End-to-end test senaryoları
  - Performans testleri

- **`docs/`**: UX düzenlemeleri ve proje dökümantasyonu
  - Kullanıcı deneyimi tasarım dokümanları
  - API dökümantasyonu

## 🎉 Proje Durumu: TAMAMLANDI

**Son Güncelleme**: Ocak 2025  
**Durum**: ✅ Production'a hazır - Sadece dokümantasyon kaldı

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

#### 🖥️ Frontend Web UI (`frontend/`)

- ✅ React 19.1.0 tabanlı modern web arayüzü
- ✅ Gerçek zamanlı nesne algılama görselleştirmesi
- ✅ Responsive tasarım ve kullanıcı deneyimi
- ✅ Backend API entegrasyonu
- ✅ Canlı kamera feed görüntüleme
- ✅ Risk analizi dashboard'u

#### 🧪 Test Modülü (`integration/`)

- ✅ Backend API unit testleri
- ✅ Detection endpoint testleri  
- ✅ Frontend component testleri
- ✅ End-to-end sistem testleri

### 📝 Kalan Görevler:

- 📋 **Dokümantasyon** (`docs/`): UX tasarım dokümanları ve kullanıcı kılavuzu

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

### 📋 Sistem Gereksinimleri

- **Python**: 3.8+ (detection ve backend için)
- **Node.js**: 16+ (frontend için)
- **Kamera**: USB webcam veya dahili kamera
- **İşletim Sistemi**: Windows, macOS, Linux
- **RAM**: En az 4GB (YOLO modeli için)

### ⚙️ Geliştirme Ortamı Kurulumu

#### 1. Projeyi Klonlayın:

```bash
git clone <repository-url>
cd GlobalProVision
```

#### 2. Detection Modülü Kurulumu:

```bash
cd detection
pip install -r requirements.txt
python app.py  # Port 5000'de çalışır
```

**Bağımlılıklar:**
- `ultralytics` (YOLO)
- `opencv-python` (kamera işlemleri)
- `flask` (web server)

#### 3. Backend API Kurulumu:

```bash
cd backend
pip install fastapi uvicorn requests python-multipart
python app.py  # Port 8000'de çalışır
```

#### 4. Frontend Kurulumu:

```bash
cd frontend
npm install
npm start  # Port 3000'de çalışır
```

#### 5. Tam Sistem Testi:

```bash
# Detection modülü test
curl http://localhost:5000/data_feed

# Backend API test  
curl http://localhost:8000/api/v1/detected-objects

# Frontend erişim
# http://localhost:3000 adresini ziyaret edin
```

### 🔄 Hızlı Başlangıç (Tüm Servisler)

```bash
# Terminal 1: Detection modülü
cd detection && python app.py

# Terminal 2: Backend API  
cd backend && python app.py

# Terminal 3: Frontend
cd frontend && npm start
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

### Frontend:

- **Framework**: React 19.1.0
- **Port**: 3000 (development), 80/443 (production)
- **State Management**: React Hooks
- **Styling**: CSS3 + Modern UI patterns
- **Build Tool**: Create React App + Webpack

## 🔒 Güvenlik

### 🛡️ Güvenlik Önlemleri

- **Input Validation**: Tüm API girdileri doğrulanır
- **CORS Policy**: Sadece izin verilen domain'ler
- **Rate Limiting**: API isteklerinde hız sınırı
- **Error Handling**: Güvenli hata mesajları

### 🔐 Production Güvenlik Checklist

- [ ] HTTPS sertifikası (SSL/TLS)
- [ ] API key authentication
- [ ] Database şifreleme
- [ ] Log monitoring
- [ ] Güvenlik açığı taraması

## ⚡ Performans

### 📊 Beklenen Performans

- **Detection Latency**: ~50-100ms (webcam)
- **API Response Time**: ~10-50ms
- **Concurrent Users**: 10-50 kullanıcı
- **Memory Usage**: ~2-4GB (YOLO model)

### 🚀 Optimizasyon Önerileri

- **GPU Kullanımı**: CUDA desteği ile YOLO hızlandırma
- **Model Optimizasyonu**: TensorRT ile model optimizasyonu
- **Caching**: Redis ile API response cache
- **Load Balancing**: Nginx ile yük dağıtımı

## ✅ Ortak Git Kullanımı:

- Herkes kendi sorumluluğu için ilgili brancht'e çalışır.
- Çalışmaya başlamadan önce:
  git fetch
  git rebase origin/main
- Bitince:
  git pull --rebase origin/main
  git push origin `<branch>`
- PR üzerinden merge yapılır. main'e doğrudan yazılmaz.

## 🧪 Test Stratejisi
<<<<<<< Updated upstream

### ✅ Mevcut Testler

```bash
# Backend API testleri
cd backend
python test_api.py        # Unit testler
python test_endpoints.py  # Endpoint testleri

# Frontend testleri
cd frontend  
npm test                  # React component testleri
```

### 🔍 Test Kategorileri

- **Unit Testler**: Tekil fonksiyon testleri
- **Integration Testler**: Modüller arası iletişim
- **End-to-End Testler**: Tam sistem senaryoları
- **Performance Testler**: Yanıt süresi ve kaynak kullanımı

## 🚨 Sorun Giderme

### ❓ Sık Karşılaşılan Sorunlar

#### 1. Kamera Erişim Sorunu
```bash
# Kamera iznini kontrol edin
# macOS: Sistem Tercihleri > Güvenlik ve Gizlilik > Kamera
# Windows: Ayarlar > Gizlilik > Kamera
```

#### 2. Port Çakışması
```bash
# Kullanımda olan portları kontrol edin
lsof -i :5000  # Detection modülü
lsof -i :8000  # Backend API
lsof -i :3000  # Frontend

# Alternatif port kullanımı
python app.py --port 5001
```

#### 3. YOLO Model İndirme Sorunu
```bash
# Manuel model indirme
cd detection/models
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
```

#### 4. CORS Hatası
```bash
# Backend CORS ayarlarını kontrol edin
# app.py dosyasında origins listesini güncelleyin
```

### 📞 Destek

- **Backend Sorunları**: Backend takımı ile iletişime geçin
- **Detection Sorunları**: AI/ML takımı ile iletişime geçin  
- **Frontend Sorunları**: Frontend takımı ile iletişime geçin

## 🤝 Katkıda Bulunma

### 📝 Geliştirme İş Akışı

1. **Feature Branch Oluşturun**:
   ```bash
   git checkout -b feature/yeni-ozellik
   ```

2. **Kodunuzu Yazın ve Test Edin**:
   ```bash
   # Testleri çalıştırın
   python test_*.py
   npm test
   ```

3. **Commit ve Push**:
   ```bash
   git add .
   git commit -m "feat: yeni özellik eklendi"
   git push origin feature/yeni-ozellik
   ```

4. **Pull Request Oluşturun**:
   - Açıklayıcı başlık ve açıklama
   - Test sonuçları ekleyin
   - Code review bekleyin

### ✨ Kod Standartları

- **Python**: PEP 8 standardı
- **JavaScript**: ESLint kuralları
- **Commit Mesajları**: Conventional Commits formatı
- **Dokümantasyon**: Her yeni özellik için README güncellemesi

## 📋 Dokümantasyon Tamamlama Listesi

### 📝 Kalan Dokümantasyon Görevleri:

- [ ] **UX Tasarım Dokümanı**: Kullanıcı arayüzü tasarım prensipleri
- [ ] **Kullanıcı Kılavuzu**: Son kullanıcı için detaylı kullanım rehberi  
- [ ] **API Referans Dokümanı**: Geliştiriciler için endpoint detayları
- [ ] **Deployment Rehberi**: Production ortamı kurulum adımları
- [ ] **Güvenlik Dokümanı**: Güvenlik politikaları ve en iyi uygulamalar

## 🚀 Production Deployment

### ✅ Sistem Hazır:

- **Detection Modülü**: Gerçek zamanlı nesne algılama çalışıyor
- **Backend API**: RESTful servisler aktif  
- **Frontend**: Modern React arayüzü hazır
- **Testler**: Tüm test senaryoları geçiyor

### 🎯 Gelecek Geliştirmeler (Opsiyonel):

1. **Performance İyileştirmeleri**:
   - GPU desteği (CUDA)
   - Model optimizasyonu (TensorRT)
   - Caching sistemi (Redis)

2. **Ek Özellikler**:
   - WebSocket ile real-time updates
   - Mobile uygulama (React Native)
   - Çoklu kamera desteği
   - Gelişmiş analytics dashboard

3. **DevOps İyileştirmeleri**:
   - Docker containerization
   - CI/CD pipeline
   - Monitoring ve logging
   - Auto-scaling
=======

### ✅ Mevcut Testler

```bash
# Backend API testleri
cd backend
python test_api.py        # Unit testler
python test_endpoints.py  # Endpoint testleri

# Frontend testleri
cd frontend  
npm test                  # React component testleri
```

### 🔍 Test Kategorileri

- **Unit Testler**: Tekil fonksiyon testleri
- **Integration Testler**: Modüller arası iletişim
- **End-to-End Testler**: Tam sistem senaryoları
- **Performance Testler**: Yanıt süresi ve kaynak kullanımı

## 🚨 Sorun Giderme

### ❓ Sık Karşılaşılan Sorunlar

#### 1. Kamera Erişim Sorunu
```bash
# Kamera iznini kontrol edin
# macOS: Sistem Tercihleri > Güvenlik ve Gizlilik > Kamera
# Windows: Ayarlar > Gizlilik > Kamera
```

#### 2. Port Çakışması
```bash
# Kullanımda olan portları kontrol edin
lsof -i :5000  # Detection modülü
lsof -i :8000  # Backend API
lsof -i :3000  # Frontend

# Alternatif port kullanımı
python app.py --port 5001
```

#### 3. YOLO Model İndirme Sorunu
```bash
# Manuel model indirme
cd detection/models
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
```

#### 4. CORS Hatası
```bash
# Backend CORS ayarlarını kontrol edin
# app.py dosyasında origins listesini güncelleyin
```

### 📞 Destek

- **Backend Sorunları**: Backend takımı ile iletişime geçin
- **Detection Sorunları**: AI/ML takımı ile iletişime geçin  
- **Frontend Sorunları**: Frontend takımı ile iletişime geçin

## 🤝 Katkıda Bulunma

### 📝 Geliştirme İş Akışı

1. **Feature Branch Oluşturun**:
   ```bash
   git checkout -b feature/yeni-ozellik
   ```

2. **Kodunuzu Yazın ve Test Edin**:
   ```bash
   # Testleri çalıştırın
   python test_*.py
   npm test
   ```

3. **Commit ve Push**:
   ```bash
   git add .
   git commit -m "feat: yeni özellik eklendi"
   git push origin feature/yeni-ozellik
   ```

4. **Pull Request Oluşturun**:
   - Açıklayıcı başlık ve açıklama
   - Test sonuçları ekleyin
   - Code review bekleyin

### ✨ Kod Standartları

- **Python**: PEP 8 standardı
- **JavaScript**: ESLint kuralları
- **Commit Mesajları**: Conventional Commits formatı
- **Dokümantasyon**: Her yeni özellik için README güncellemesi

## 📈 Sonraki Adımlar

1. **Frontend Geliştirme**: React/Vue.js ile web arayüzü
2. **Kamera Feed Entegrasyonu**: Backend'den video stream
3. **Real-time Updates**: WebSocket veya Server-Sent Events
4. **Production Deployment**: Docker containerization
5. **Güvenlik**: Authentication ve rate limiting
6. **Monitoring**: Logging ve metrics sistemi
7. **CI/CD Pipeline**: Otomatik test ve deployment
8. **Mobile App**: React Native ile mobil uygulama
>>>>>>> Stashed changes
