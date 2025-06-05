from typing import Optional
from src.models.bert_classifier import BertClassifier
from config.config import TOPIC_CATEGORIES

class TopicExtractor:
    def __init__(self):
        self.classifier = BertClassifier()
        
    def extract(self, text: str) -> Optional[str]:
        """
        Dilekçenin konusunu belirler.
        """
        if not text:
            return None
            
        try:
            # BERT modeli ile sınıflandırma yap
            classification_result = self.classifier.classify_text(text[:500])  # İlk 500 karakteri al
            
            if classification_result:
                # Model çıktısını ve anahtar kelime eşleşmelerini birleştir
                konu_skorlari = {}
                
                # Model çıktısına göre skor ver
                for konu in TOPIC_CATEGORIES.keys():
                    if konu.lower() in classification_result['label'].lower():
                        konu_skorlari[konu] = classification_result['score'] * 2
                    else:
                        konu_skorlari[konu] = 0
                
                # Anahtar kelime eşleşmelerine göre skor ekle
                for konu, anahtar_kelimeler in TOPIC_CATEGORIES.items():
                    for kelime in anahtar_kelimeler:
                        if kelime.lower() in text.lower():
                            konu_skorlari[konu] = konu_skorlari.get(konu, 0) + 0.1
                
                # En yüksek skorlu konuyu bul
                if konu_skorlari:
                    en_yuksek_skorlu_konu = max(konu_skorlari.items(), key=lambda x: x[1])
                    if en_yuksek_skorlu_konu[1] > 0:
                        return en_yuksek_skorlu_konu[0]
            
            # Eğer model güvenilir bir sonuç vermediyse, anahtar kelime eşleşmelerine bak
            for konu, anahtar_kelimeler in TOPIC_CATEGORIES.items():
                for kelime in anahtar_kelimeler:
                    if kelime.lower() in text.lower():
                        return konu
            
            return "DİĞER"
            
        except Exception as e:
            print(f"Konu belirleme sırasında hata oluştu: {e}")
            return "DİĞER" 