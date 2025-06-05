import json
from pathlib import Path
from src.extractors.text_extractor import TextExtractor
from src.extractors.name_extractor import NameExtractor
from src.extractors.address_extractor import AddressExtractor
from src.extractors.date_extractor import DateExtractor
from src.extractors.institution_extractor import InstitutionExtractor
from src.extractors.topic_extractor import TopicExtractor
from src.extractors.request_extractor import RequestExtractor
from src.extractors.inference_extractor import InferenceExtractor
from src.extractors.tone_language_analyzer import ToneLanguageAnalyzer
from config.config import PDF_DIR, OUTPUT_JSON

def main():
    # PDF'lerden metin çıkar
    print("PDF'lerden metin çıkarılıyor...")
    extracted_texts = TextExtractor.extract_from_directory(PDF_DIR)
    
    if not extracted_texts:
        print("İşlenecek PDF bulunamadı!")
        return
    
    # Çıkarıcıları başlat
    name_extractor = NameExtractor()
    address_extractor = AddressExtractor()
    date_extractor = DateExtractor()
    institution_extractor = InstitutionExtractor()
    topic_extractor = TopicExtractor()
    request_extractor = RequestExtractor()
    inference_extractor = InferenceExtractor()
    tone_analyzer = ToneLanguageAnalyzer()
    
    # Her PDF için bilgileri çıkar
    extracted_data = []
    
    for filename, text in extracted_texts.items():
        print(f"\n--- {filename} için bilgi çıkarımı yapılıyor ---")
        
        # Bilgileri çıkar
        name = name_extractor.extract(text)
        address = address_extractor.extract(text)
        dates = date_extractor.extract(text)
        institution = institution_extractor.extract(text)
        topic = topic_extractor.extract(text)
        request = request_extractor.extract(text)
        inferences = inference_extractor.extract(text)
        tone_language_analysis = tone_analyzer.extract(text)
        
        # Sonuçları yazdır
        print(f"  Ad Soyad: {name}")
        print(f"  Adres: {address}")
        print(f"  Tarih(ler): {dates}")
        print(f"  Kurum: {institution}")
        print(f"  Konu: {topic}")
        print(f"  Talep: {request}")
        print(f"  Çıkarımlar: {inferences}")
        print(f"  Ton ve Dil Analizi: {tone_language_analysis}")
        
        # Sonuçları kaydet
        extracted_data.append({
            "dosya_adi": filename,
            "Ad Soyad": name,
            "Adres": address,
            "Tarih(ler)": dates,
            "Kurum": institution,
            "Konu": topic,
            "Talep": request,
            "Çıkarımlar": inferences,
            "Ton ve Dil Analizi": tone_language_analysis
        })
    
    # Sonuçları JSON dosyasına kaydet
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=4)
    
    print(f"\nBilgi çıkarımı tamamlandı. Sonuçlar '{OUTPUT_JSON}' dosyasına kaydedildi.")

if __name__ == "__main__":
    main() 