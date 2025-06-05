import re
from typing import Optional

class NameExtractor:
    def extract(self, text: str) -> Optional[str]:
        """
        Ad Soyad bilgisini metinden çıkarmaya çalışır.
        """
        if not text:
            return None
            
        # T.C. Kimlik No'ya yakın isimleri bul
        tc_kimlik_regex = r"T\.?C\.?\s*Kimlik\s*No\s*:\s*(\d{11})"
        tc_eslesme = re.search(tc_kimlik_regex, text, re.IGNORECASE)
        
        if tc_eslesme:
            # T.C. Kimlik No'nun etrafındaki metinde isim arayalım
            tc_index = text.find(tc_eslesme.group(0))
            etraf_metin = text[max(0, tc_index-100):min(len(text), tc_index+100)]
            
            # İsim formatı: İlk harfi büyük, sonraki harfler küçük + Boşluk + İlk harfi büyük, sonraki harfler küçük
            isim_regex = r"\b([A-ZÇŞĞÜÖİ][a-zçşğüöı]+)\s+([A-ZÇŞĞÜÖİ][a-zçşğüöı]+)\b"
            isim_eslesme = re.search(isim_regex, etraf_metin)
            if isim_eslesme:
                return f"{isim_eslesme.group(1)} {isim_eslesme.group(2)}"
        
        # Dilekçenin sonunda, genellikle imzanın üzerinde yer alır
        son_kisim = text[int(len(text)*0.75):]
        
        # "Adı Soyadı:" formatında arama
        ad_soyad_eslesme = re.search(r"(?:Adı\s+Soyadı|Ad\s+Soyad)\s*:\s*([A-Za-zÇŞĞÜÖİçşğüöı\s]+)", son_kisim, re.IGNORECASE)
        if ad_soyad_eslesme:
            return ad_soyad_eslesme.group(1).strip()
        
        # İmza üstü isimler için arama
        imza_ustu_regex = r"\b([A-ZÇŞĞÜÖİ][a-zçşğüöı]+)\s+([A-ZÇŞĞÜÖİ][a-zçşğüöı]+)\b"
        imza_ustu_eslesme = re.search(imza_ustu_regex, son_kisim)
        if imza_ustu_eslesme:
            return f"{imza_ustu_eslesme.group(1)} {imza_ustu_eslesme.group(2)}"
        
        # Tüm metinde isim arama
        tum_metin_eslesme = re.search(imza_ustu_regex, text)
        if tum_metin_eslesme:
            return f"{tum_metin_eslesme.group(1)} {tum_metin_eslesme.group(2)}"
        
        return None 