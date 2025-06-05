import os
from pathlib import Path

# Proje kök dizini
ROOT_DIR = Path(__file__).parent.parent

# Veri dizinleri
DATA_DIR = ROOT_DIR / "data"
PDF_DIR = DATA_DIR / "pdfs"
OUTPUT_DIR = ROOT_DIR / "output"
RESULTS_DIR = OUTPUT_DIR / "results"

# Model ayarları
MODEL_NAME = "dbmdz/bert-base-turkish-cased"
NUM_LABELS = 10

# Çıktı dosyası
OUTPUT_JSON = RESULTS_DIR / "dilekce_bilgileri.json"

# Dizinleri oluştur
for directory in [PDF_DIR, RESULTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Konu kategorileri
TOPIC_CATEGORIES = {
    "YOL SORUNU": ["yol", "asfalt", "bozuk", "çukur", "kasis", "yol yapımı", "yol bakımı"],
    "SU KESİNTİSİ": ["su", "kesinti", "akmıyor", "susuz", "su basıncı", "su kaçağı"],
    "GÜRÜLTÜ": ["gürültü", "ses", "rahatsız", "yüksek ses", "müzik", "bağırma"],
    "ÇÖP SORUNU": ["çöp", "konteyner", "atık", "pislik", "temizlik", "koku"],
    "PARK SORUNU": ["park", "araç", "otopark", "yasak park", "park yeri"],
    "ELEKTRİK KESİNTİSİ": ["elektrik", "kesinti", "enerji", "sigorta", "arıza"],
    "DOĞALGAZ SORUNU": ["doğalgaz", "gaz kaçağı", "ısıtma", "kalorifer"],
    "AĞAÇ KESİMİ": ["ağaç", "kesim", "yeşil alan", "park", "bahçe"],
    "BAŞIBOŞ HAYVAN": ["başıboş", "köpek", "kedi", "sokak hayvanı", "hayvan"],
    "KAÇAK YAPI": ["kaçak", "izinsiz", "inşaat", "yapı", "bina"]
} 