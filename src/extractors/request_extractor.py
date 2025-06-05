import re
from typing import Optional

class RequestExtractor:
    def extract(self, text: str) -> Optional[str]:
        """
        Dilekçedeki talepleri çıkarmaya çalışır.
        """
        if not text:
            return None
            
        # Talep kalıpları
        talep_patterns = [
            r"(?:talep|rica|istirham)(?:\s+ediyorum|ediyoruz|ederim|ederiz|etmekteyim|etmekteyiz)[\s\S]*?[.!?]",
            r"(?:lütfen|rica\s+olunur|rica\s+ederim|rica\s+ederiz)[\s\S]*?[.!?]",
            r"(?:gerekli\s+(?:işlemlerin|tedbirlerin|çalışmaların)[\s\S]*?yapılmasını)[\s\S]*?[.!?]",
            r"(?:bilgilerinize\s+(?:sunar|arz|rica)\s+ederim)[\s\S]*?[.!?]",
            r"(?:saygılarımla\s+(?:arz\s+ederim|sunarım))[\s\S]*?[.!?]"
        ]
        
        # Metni cümlelere böl
        cumleler = re.split(r'[.!?]+', text)
        cumleler = [cumle.strip() for cumle in cumleler if cumle.strip()]
        
        # Her cümlede talep kalıplarını ara
        talepler = []
        for cumle in cumleler:
            for pattern in talep_patterns:
                eslesme = re.search(pattern, cumle, re.IGNORECASE)
                if eslesme:
                    talep = eslesme.group(0).strip()
                    if talep not in talepler:
                        talepler.append(talep)
        
        # Eğer talep bulunamazsa, son birkaç cümleye bak
        if not talepler and cumleler:
            son_cumleler = cumleler[-3:]  # Son 3 cümle
            for cumle in son_cumleler:
                # Talep içeren anahtar kelimeleri ara
                talep_kelimeleri = ["talep", "rica", "istirham", "lütfen", "gerekli", "bilgilerinize", "saygılarımla"]
                for kelime in talep_kelimeleri:
                    if kelime.lower() in cumle.lower():
                        if cumle not in talepler:
                            talepler.append(cumle)
                        break
        
        # Talepleri birleştir
        if talepler:
            return " | ".join(talepler)
        
        return "TALEP BELİRTİLMEMİŞ" 