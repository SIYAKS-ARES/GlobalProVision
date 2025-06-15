#!/usr/bin/env python3
"""
GlobalProVision API Test Scripti
Bu script API'nin çalışıp çalışmadığını test eder.
"""

import requests
import json
import time
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def test_endpoint(endpoint, description):
    """Bir endpoint'i test eder"""
    print(f"\n🔍 Test: {description}")
    print(f"📡 Endpoint: {endpoint}")

    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Başarılı! Status: {response.status_code}")
            print(f"📄 Yanıt: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ Hata! Status: {response.status_code}")
            print(f"📄 Yanıt: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Bağlantı hatası! API çalışmıyor olabilir.")
    except requests.exceptions.Timeout:
        print("❌ Zaman aşımı! API yavaş yanıt veriyor.")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")

def main():
    print("🚀 GlobalProVision API Test Başlatılıyor...")
    print(f"⏰ Test Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Ana endpoint testi
    test_endpoint("", "Ana Sayfa")

    # Health check testi
    test_endpoint("/health", "Sağlık Kontrolü")

    # Detection status testi
    test_endpoint("/detection-status", "Detection Modül Durumu")

    # Ana detection endpoint testi
    test_endpoint("/detected-objects", "Algılanan Nesneler")

    # Risk analizi testi
    test_endpoint("/detected-objects/risk", "Risk Analizi")

    # Özet veri testi
    test_endpoint("/detected-objects/summary", "Detection Özeti")

    print("\n" + "="*50)
    print("📊 GERÇEK ZAMANLI TEST (10 saniye)")
    print("="*50)

    # 10 saniye boyunca gerçek zamanlı veri çek
    for i in range(10):
        try:
            response = requests.get(f"{BASE_URL}/detected-objects", timeout=5)
            if response.status_code == 200:
                data = response.json()
                detected = data.get('detected', [])
                danger = data.get('danger_percentage', 0)
                timestamp = data.get('timestamp', '')

                print(f"[{i+1:2d}/10] {timestamp} | Nesneler: {detected} | Risk: %{danger:.1f}")
            else:
                print(f"[{i+1:2d}/10] ❌ HTTP {response.status_code}")

        except Exception as e:
            print(f"[{i+1:2d}/10] ❌ Hata: {e}")

        time.sleep(1)

    print("\n✨ Test tamamlandı!")

if __name__ == "__main__":
    main()
