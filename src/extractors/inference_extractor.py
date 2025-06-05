import re
from typing import List, Dict, Tuple

class InferenceExtractor:
    def __init__(self):
        self.inference_rules: Dict[str, Tuple[str, List[str]]] = {
            "TEKRARLAYAN_SORUN": (
                "Sorunun düzenli olarak tekrarlandığına işaret ediyor.",
                [
                    r"her\s+(gün|akşam|gece|sabah|hafta)",
                    r"sürekli",
                    r"defalarca",
                    r"tekrar",
                    r"yine",
                    r"hep\s+aynı"
                ]
            ),
            "ACİLİYET_VE_CİDDİYET": (
                "Sorunun ciddiyetini veya aciliyetini vurguluyor.",
                [
                    r"korku",
                    r"endişe",
                    r"tehlike",
                    r"risk",
                    r"sağlık",
                    r"güvenlik",
                    r"mağdur",
                    r"acil",
                    r"dayanılmaz",
                    r"yaşlı",
                    r"çocuk",
                    r"hasta"
                ]
            ),
            "UZUN_SÜREDİR_DEVAM_EDEN_SORUN": (
                "Sorunun uzun bir süredir devam ettiğini ve çözülmediğini gösteriyor.",
                [
                    r"defalarca\s+(bildirdik|söyledik|aradık)",
                    r"(aylar|yıllar)dır",
                    r"uzun\s+süredir",
                    r"hâlâ\s+(çözüm|cevap)\s+yok",
                    r"sonuç\s+alamadık"
                ]
            ),
            "TOPLUMSAL_ETKİ": (
                "Sorunun sadece bir kişiyi değil, bir topluluğu etkilediğini belirtiyor.",
                [
                    r"mahalleli",
                    r"komşular",
                    r"apartman\s+sakinleri",
                    r"tüm\s+bölge",
                    r"herkes"
                ]
            )
        }

    def extract(self, text: str) -> List[Dict[str, str]]:
        """
        Metinden kural tabanlı çıkarımlar yapar.
        """
        if not text:
            return []
            
        found_inferences = []
        
        for key, (description, patterns) in self.inference_rules.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    found_inferences.append({
                        "çıkarım_kodu": key,
                        "açıklama": description,
                        "tetikleyen_ifade": match.group(0)
                    })
                    # Bir kural tetiklendiğinde diğerlerine geç, aynı kuralın farklı desenlerini arama
                    break
                    
        return found_inferences 