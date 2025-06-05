import re
from typing import List
from dateparser import parse as parse_date

class DateExtractor:
    def extract(self, text: str) -> List[str]:
        """
        Dilekçe metnindeki tarihleri ve tarih aralıklarını bulur.
        """
        if not text:
            return []
            
        bulunan_tarihler = []
        
        # Göreceli zaman ifadeleri
        goreceli_zaman_regex = r"(?:Geçtiğimiz|Son|Önceki)\s+(?:ay|hafta|gün|yıl|hafta\s+sonu|hafta\s+içi)"
        goreceli_zaman_eslesmeleri = re.findall(goreceli_zaman_regex, text, re.IGNORECASE)
        bulunan_tarihler.extend(goreceli_zaman_eslesmeleri)
        
        # Süre ifadeleri (aydır, gündür, haftadır vb.)
        sure_regex = r"(?:\d+\s+(?:ay|hafta|gün|yıl|saat)|(?:bir|iki|üç|dört|beş|altı|yedi|sekiz|dokuz|on)\s+(?:ay|hafta|gün|yıl|saat))(?:dır|dir|den\s+beri|süredir|dır\s+arızalı|dir\s+arızalı)"
        sure_eslesmeleri = re.findall(sure_regex, text, re.IGNORECASE)
        bulunan_tarihler.extend(sure_eslesmeleri)
        
        # Günün belirli saatleri
        saat_regex = r"(?:her\s+(?:gün|akşam|sabah|öğlen|gece))\s+(?:saat\s+)?(\d{1,2}:\d{2})"
        saat_eslesmeleri = re.findall(saat_regex, text, re.IGNORECASE)
        bulunan_tarihler.extend([f"Her gün {saat}" for saat in saat_eslesmeleri])
        
        # Mevsim ve dönem ifadeleri
        donem_regex = r"(?:Kış|Yaz|İlkbahar|Sonbahar)\s+(?:aylarında|mevsiminde|döneminde)"
        donem_eslesmeleri = re.findall(donem_regex, text, re.IGNORECASE)
        bulunan_tarihler.extend(donem_eslesmeleri)
        
        # Haftanın belirli günleri
        hafta_gunleri_regex = r"\b(?:Hafta\s+(?:içi|sonu)(?:leri|de|da)?|(?:Pazartesi|Salı|Çarşamba|Perşembe|Cuma|Cumartesi|Pazar)\s*(?:günleri|günü)?)\b"
        hafta_gunleri_eslesmeleri = re.findall(hafta_gunleri_regex, text, re.IGNORECASE)
        if hafta_gunleri_eslesmeleri:
            normalized_eslesmeler = []
            for eslesme in hafta_gunleri_eslesmeleri:
                if "sonu" in eslesme.lower():
                    normalized_eslesmeler.append("Hafta sonu")
                elif "içi" in eslesme.lower():
                    normalized_eslesmeler.append("Hafta içi")
                else:
                    normalized_eslesmeler.append(eslesme.strip())
            bulunan_tarihler.extend(normalized_eslesmeler)
        
        # Günün belirli zamanları
        gun_zamani_regex = r"(?:geceleri|sabahları|öğlenleri|akşamları|gündüzleri)"
        gun_zamani_eslesmeleri = re.findall(gun_zamani_regex, text, re.IGNORECASE)
        bulunan_tarihler.extend(gun_zamani_eslesmeleri)
        
        # Standart tarih formatları ve ay isimleriyle tarihler
        tarih_regex_cesitleri = [
            r'\b(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})\b',  # 01/01/2023, 01.01.2023, 01-01-2023
            r'\b(\d{1,2}\s+(?:Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık)(?:\'da|\'de)?)\b',  # 1 Haziran'da, 15 Mayıs
            r'\b(?:Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık)(?:\'da|\'de)?\b'  # Haziran'da, Mayıs'ta
        ]
        
        for regex_pattern in tarih_regex_cesitleri:
            eslesmeler = re.findall(regex_pattern, text, re.IGNORECASE)
            for eslesme in eslesmeler:
                if isinstance(eslesme, tuple):
                    eslesme = eslesme[0]  # tuple ise ilk elemanı al
                parsed_date_obj = parse_date(eslesme, languages=['tr'])
                if parsed_date_obj:
                    bulunan_tarihler.append(parsed_date_obj.strftime('%Y-%m-%d'))
                else:
                    bulunan_tarihler.append(eslesme)
        
        # "Tarih:" anahtar kelimesiyle arama
        dilekce_tarihi_regex = r'(?:Tarih\s*:\s*|TARİH\s*:\s*)(\d{1,2}[./-]\d{1,2}[./-]\d{2,4}|\d{1,2}\s+(?:Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık)(?:\'da|\'de)?)'
        d_tarih_eslesme = re.search(dilekce_tarihi_regex, text, re.IGNORECASE)
        if d_tarih_eslesme:
            parsed_date_obj = parse_date(d_tarih_eslesme.group(1).strip(), languages=['tr'])
            if parsed_date_obj:
                dt_str = parsed_date_obj.strftime('%Y-%m-%d')
                if dt_str not in bulunan_tarihler:
                    bulunan_tarihler.append(dt_str)
            elif d_tarih_eslesme.group(1).strip() not in bulunan_tarihler:
                bulunan_tarihler.append(d_tarih_eslesme.group(1).strip())
        
        return list(set(bulunan_tarihler))  # Tekrarları kaldır 