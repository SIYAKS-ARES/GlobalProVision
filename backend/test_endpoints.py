#!/usr/bin/env python3
"""
GlobalProVision API Test Scripti - Hızlı Endpoint Kontrolü
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

def test_endpoint(endpoint, description):
    """Bir endpoint'i test eder"""
    print(f"\n🔍 {description}")
    print(f"📡 GET {BASE_URL}{endpoint}")
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ OK - Status: {response.status_code}")
            print(f"📄 Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ Error - Status: {response.status_code}")
            print(f"📄 Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error - API çalışmıyor!")
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    print("🚀 GlobalProVision API Endpoint Test")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Test ediliyor endpoint'ler
    endpoints = [
        ("/health", "Health Check"),
        ("/detected-objects", "Detected Objects (Ana Endpoint)"),
        ("/detected-objects/risk", "Risk Analysis"),
        ("/detected-objects/summary", "Detection Summary"),
        ("/detection-status", "Detection Status")
    ]
    
    for endpoint, description in endpoints:
        test_endpoint(endpoint, description)
    
    print("\n" + "="*60)
    print("✨ Test Tamamlandı!")
    print("\n💡 Eğer 'not found' hataları alıyorsan:")
    print("   1. Backend API'si çalışıyor mu? (python app.py)")
    print("   2. Detection modülü çalışıyor mu? (cd detection && python app.py)")
    print("   3. Port'lar doğru mu? (API:8000, Detection:5000)")

if __name__ == "__main__":
    main() 