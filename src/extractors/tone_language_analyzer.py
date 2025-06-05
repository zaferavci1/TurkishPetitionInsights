import re
from typing import Dict

class ToneLanguageAnalyzer:
    def __init__(self):
        self.ton_keywords = {
            "kibar_sikayet": [
                r"rica ederim", r"lütfen", r"mümkünse", r"yardımcı olursanız",
                r"sevinirim", r"nazikçe", r"anlayışınıza sığınıyorum"
            ],
            "ofkeli_tepkili": [
                r"rezalet", r"kabul edilemez", r"yeter artık", r"derhal", r"derhal çözüm",
                r"asla", r"kesinlikle", r"bıktım", r"şikayetçiyim", r"isyan ediyorum",
                r"skandal", r"sorumsuzluk", r"ihmal"
            ],
            "caresiz": [
                r"çaresizim", r"ne yapacağımı bilmiyorum", r"yardım edin", r"başka çarem kalmadı",
                r"umutsuzum", r"mağdurum", r"perişan oldum", r"zor durumdayım"
            ],
            "resmi_nesnel": [
                r"arz ederim", r"bilgilerinize sunulur", r"gereğini arz ederim",
                r"beyan ederim", r"tensip buyrulması"
            ]
        }
        self.formality_keywords = {
            "resmi": [
                r"arz ederim", r"saygılarımla arz ederim", r"bilgilerinize arz ederim",
                r"gereğini arz ederim", r"talep ve beyan ederim", r"mukteza",
                r"tensip", r"bilvekale", r"sayın başkanım", r"sayın valim", r"sayın müdürüm"
            ],
            "samimi": [
                r"merhaba", r"iyi günler", r"kolay gelsin", r"abicim", r"ablacım", r"hocam",
                r"şimdiden teşekkürler", r"sevgiler"
            ],
            "argo": []
        }

    def _analyze_tone(self, text: str) -> str:
        text_lower = text.lower()
        detected_tones = []

        # 1. Öfkeli / Tepkili Kontrolü
        exclamation_count = text.count('!')
        if exclamation_count >= 3 or any(re.search(p, text_lower) for p in self.ton_keywords["ofkeli_tepkili"]):
            if exclamation_count >= 2 and any(re.search(r"yeter|artık|derhal|rezalet|kabul edilemez", text_lower)):
                 detected_tones.append("Öfkeli / Tepkili")

        # 2. Çaresiz Kontrolü
        if any(re.search(p, text_lower) for p in self.ton_keywords["caresiz"]):
            detected_tones.append("Çaresiz")

        # 3. Kibar Şikayet Kontrolü (Eğer öfkeli değilse)
        if "Öfkeli / Tepkili" not in detected_tones:
            if any(re.search(p, text_lower) for p in self.ton_keywords["kibar_sikayet"]):
                detected_tones.append("Kibar Şikâyet")

        # 4. Resmi ve Nesnel Kontrolü
        if any(re.search(p, text_lower) for p in self.ton_keywords["resmi_nesnel"]):
            if not any(t in detected_tones for t in ["Öfkeli / Tepkili", "Çaresiz"]):
                detected_tones.append("Resmî ve Nesnel")

        # Önceliklendirme
        if "Öfkeli / Tepkili" in detected_tones: return "Öfkeli / Tepkili"
        if "Çaresiz" in detected_tones: return "Çaresiz"
        if "Kibar Şikâyet" in detected_tones: return "Kibar Şikâyet"
        if "Resmî ve Nesnel" in detected_tones: return "Resmî ve Nesnel"

        return "Sakin"

    def _analyze_formality(self, text: str) -> str:
        text_lower = text.lower()
        if any(re.search(p, text_lower) for p in self.formality_keywords["resmi"]):
            return "Resmî"
        if any(re.search(p, text_lower) for p in self.formality_keywords["samimi"]):
            return "Samimi"
        if text_lower.startswith("sayın") or "arz ederim" in text_lower:
            return "Resmî"
            
        return "Resmî" # Varsayılan

    def _analyze_grammar(self, text: str) -> str:
        error_score = 0
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len([s for s in sentences if s.strip()])

        if not sentence_count: return "Düşük"

        # Cümle Başı Büyük Harf Kontrolü
        invalid_start_count = 0
        for sentence in sentences:
            clean_sentence = sentence.strip()
            if clean_sentence and not clean_sentence[0].isupper() and clean_sentence[0].isalpha():
                invalid_start_count += 1
        
        if invalid_start_count > sentence_count / 3:
            error_score += 2

        # Noktalama İşareti Kullanımı
        if text.strip() and text.strip()[-1] not in ['.', '!', '?']:
            error_score += 1

        # Aşırı Ünlem veya Soru İşareti
        if text.count('!') > 5 or text.count('?') > 5:
            error_score += 1
        
        if error_score == 0: return "Yüksek"
        if error_score <= 2: return "Orta"
        return "Düşük"

    def extract(self, text: str) -> Dict[str, str]:
        if not text or not text.strip():
            return {
                "ton": "Belirlenemedi",
                "dil_resmiyeti": "Belirlenemedi",
                "yazim_uyumu": "Belirlenemedi"
            }
        
        tone = self._analyze_tone(text)
        formality = self._analyze_formality(text)
        grammar = self._analyze_grammar(text)

        return {
            "ton": tone,
            "dil_resmiyeti": formality,
            "yazim_uyumu": grammar
        } 