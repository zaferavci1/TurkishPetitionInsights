import re
from typing import Optional

class InstitutionExtractor:
    def extract(self, text: str) -> Optional[str]:
        """
        Dilekçenin hitap edildiği kurumu çıkarmaya çalışır.
        """
        if not text:
            return None
            
        # Metni temizle ve boş satırları kaldır
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if not lines:
            return "İLGİLİ KURUM"
            
        # İlk birkaç satırda kurum adı arama
        ilk_satirlar = '\n'.join(lines[:5])
        
        # Doğrudan kurum adı eşleşmeleri
        kurum_patterns = [
            r"(?:Sayın|Değerli)\s+([A-ZÇŞĞÜÖİ][a-zçşğüöı]+(?:\s+[A-ZÇŞĞÜÖİ][a-zçşğüöı]+)*\s+(?:Belediyesi|Müdürlüğü|Başkanlığı|Valiliği|Kaymakamlığı|İlçe\s+Belediyesi|İl\s+Belediyesi))",
            r"(?:Sayın|Değerli)\s+([A-ZÇŞĞÜÖİ][a-zçşğüöı]+(?:\s+[A-ZÇŞĞÜÖİ][a-zçşğüöı]+)*\s+(?:Belediye|Müdürlük|Başkanlık|Valilik|Kaymakamlık))",
            r"(?:Sayın|Değerli)\s+([A-ZÇŞĞÜÖİ][a-zçşğüöı]+(?:\s+[A-ZÇŞĞÜÖİ][a-zçşğüöı]+)*\s+(?:Başkanı|Müdürü|Valisi|Kaymakamı))",
            r"(?:İlgili\s+Birim|Sayın\s+İlgili|Sayın\s+Yetkili|Sayın\s+Müdürlük|Sayın\s+Belediye\s+Başkanı|Sayın\s+Valilik\s+Makamına|Değerli\s+Belediye\s+Yetkilileri)"
        ]
        
        for pattern in kurum_patterns:
            eslesme = re.search(pattern, ilk_satirlar, re.IGNORECASE)
            if eslesme:
                if len(eslesme.groups()) > 0:
                    return eslesme.group(1).strip()
                return eslesme.group(0).strip()
        
        # Kurum türlerine göre arama
        kurum_turleri = {
            "BELEDİYE": ["belediye", "belediyesi", "belediye başkanı"],
            "VALİLİK": ["valilik", "valiliği", "vali"],
            "KAYMAKAMLIK": ["kaymakamlık", "kaymakamlığı", "kaymakam"],
            "MÜDÜRLÜK": ["müdürlük", "müdürlüğü", "müdür"],
            "BAŞKANLIK": ["başkanlık", "başkanlığı", "başkan"]
        }
        
        # Metinde kurum türlerinin geçme sayısını say
        kurum_sayilari = {}
        for kurum_turu, anahtar_kelimeler in kurum_turleri.items():
            sayac = 0
            for kelime in anahtar_kelimeler:
                sayac += len(re.findall(r'\b' + kelime + r'\b', text, re.IGNORECASE))
            if sayac > 0:
                kurum_sayilari[kurum_turu] = sayac
        
        # En çok geçen kurum türünü bul
        if kurum_sayilari:
            en_cok_gecen = max(kurum_sayilari.items(), key=lambda x: x[1])
            return en_cok_gecen[0]
        
        return "İLGİLİ KURUM" 