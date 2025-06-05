import re
from typing import Optional

class AddressExtractor:
    def extract(self, text: str) -> Optional[str]:
        """
        Adres veya bölge bilgisini çıkarmaya çalışır.
        """
        if not text:
            return None
            
        # "Adres:" anahtar kelimesiyle başlayan satırları arayalım
        adres_regex = r"(?:Adres|ADRES)\s*:\s*([^\n]+)"
        eslesme = re.search(adres_regex, text, re.IGNORECASE)
        if eslesme:
            return eslesme.group(1).strip()

        # İlçe/il formatını arayalım
        # Örnek: Kadıköy/İstanbul, Beşiktaş/İstanbul
        ilce_il_regex = r"([A-ZÇŞĞÜÖİ][a-zçşğüöı]+)\s*/\s*([A-ZÇŞĞÜÖİ][a-zçşğüöı]+)"
        
        # Metnin son çeyreğinde arama yapalım (genellikle iletişim bilgileri burada olur)
        son_kisim = text[int(len(text)*0.75):]
        
        # Son kısımda ilçe/il formatını ara
        eslesmeler = re.findall(ilce_il_regex, son_kisim)
        if eslesmeler:
            # En son bulunan eşleşmeyi al (genellikle en doğru olanı)
            son_eslesme = eslesmeler[-1]
            return f"{son_eslesme[0]}/{son_eslesme[1]}"
        
        # Eğer son kısımda bulunamazsa, tüm metinde ara
        eslesmeler = re.findall(ilce_il_regex, text)
        if eslesmeler:
            # En son bulunan eşleşmeyi al
            son_eslesme = eslesmeler[-1]
            return f"{son_eslesme[0]}/{son_eslesme[1]}"
        
        # Eğer ilçe/il formatı bulunamazsa, sadece ilçe veya il arayalım
        ilce_regex = r"\b([A-ZÇŞĞÜÖİ][a-zçşğüöı]+(?:İlçesi|İlçe))\b"
        il_regex = r"\b([A-ZÇŞĞÜÖİ][a-zçşğüöı]+(?:İli|İl))\b"
        
        # Önce ilçe ara
        ilce_eslesme = re.search(ilce_regex, son_kisim)
        if ilce_eslesme:
            ilce = ilce_eslesme.group(1)
            # İlçenin yanında il var mı diye bak
            il_eslesme = re.search(il_regex, son_kisim)
            if il_eslesme:
                return f"{ilce}/{il_eslesme.group(1)}"
            return ilce
        
        # Sadece il ara
        il_eslesme = re.search(il_regex, son_kisim)
        if il_eslesme:
            return il_eslesme.group(1)
        
        return None 