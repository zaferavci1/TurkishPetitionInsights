import os
import PyPDF2 # veya pdfplumber
import json
import re # Standart regex modülü
# import regex # Daha gelişmiş regex modülü (isteğe bağlı)
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from dateparser import parse as parse_date
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline

# NLTK gerekli verileri indir
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

# Model ve tokenizer'ı yükle (ilk çalıştırmada indirilecek)
try:
    tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-base-turkish-cased")
    model = AutoModelForSequenceClassification.from_pretrained("dbmdz/bert-base-turkish-cased", num_labels=10)
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)
except Exception as e:
    print(f"Model yüklenirken hata oluştu: {e}")
    print("Lütfen transformers ve torch kütüphanelerinin yüklü olduğundan emin olun.")
    print("pip install transformers torch")
    exit(1)

def extract_text_from_pdf(pdf_path):
    """Verilen PDF dosyasından metin içeriğini çıkarır."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Hata: {pdf_path} dosyasından metin okunurken sorun oluştu - {e}")
        return None

# Örnek PDF'lerinizin bulunduğu klasör
pdf_klasoru = "data" # Kendi klasör adınızı yazın
dilekce_metinleri = {}

if not os.path.exists(pdf_klasoru):
    print(f"'{pdf_klasoru}' adlı klasör bulunamadı. Lütfen PDF'lerinizin olduğu klasörün adını doğru girdiğinizden emin olun.")
else:
    for filename in os.listdir(pdf_klasoru):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_klasoru, filename)
            print(f"{filename} işleniyor...")
            metin = extract_text_from_pdf(pdf_path)
            if metin:
                dilekce_metinleri[filename] = metin
                # print(f"--- {filename} içeriği ---")
                # print(metin[:500] + "...") # İlk 500 karakteri göster
                # print("-" * 30)

print(f"\nToplam {len(dilekce_metinleri)} adet PDF dosyası başarıyla okundu.")



def kurum_adi_cikar(metin):
    """
    Dilekçenin hitap ettiği kurumu bulmaya çalışır.
    """
    if not metin or not metin.strip():
        # print("DEBUG: kurum_adi_cikar fonksiyonuna boş veya sadece boşluk içeren metin geldi.")
        return None

    # Genellikle ilk 7-10 satırda arama yapmak yeterlidir.
    # Satırları bölerken çeşitli satır sonu karakterlerini dikkate alalım
    lines = re.split(r'\r\n|\r|\n', metin)
    ilk_satirlar_liste = [line.strip() for line in lines[:10] if line.strip()] # Boş satırları atla
    ilk_satirlar_metin = "\n".join(ilk_satirlar_liste)

    # print(f"DEBUG: İşlenen İlk Satırlar:\n'{ilk_satirlar_metin}'") # Hata ayıklama için

    # 1. Doğrudan ve Tam Kurum Adı + Yönelme Eki
    pattern_name_with_affix = r"^\s*([\w\sÇŞĞÜÖİİçşğüöı\.\-]+?)\s*'?(?:NA|NE|Makamına| Müdürlüğüne| Başkanlığına| Valiliğine| Kaymakamlığına| Bakanlığına| Daire Başkanlığına| Genel Müdürlüğüne| Rektörlüğüne| Dekanlığına)\b"
    match = re.search(pattern_name_with_affix, ilk_satirlar_metin, re.IGNORECASE | re.MULTILINE)
    if match:
        kurum_adi = match.group(1).strip().upper()
        if kurum_adi.startswith("SAYIN "):
            kurum_adi = kurum_adi[len("SAYIN "):].strip()
        if kurum_adi: return kurum_adi # Boş string dönmesini engelle

    # 2. Tam Kurum Adı (Tek Başına veya belirli bir organizasyonel son ek ile biten)
    org_birimleri_liste = [
        "MÜDÜRLÜĞÜ", "BAŞKANLIĞI", "VALİLİĞİ", "KAYMAKAMLIĞI", "DAİRE BAŞKANLIĞI", "GENEL MÜDÜRLÜĞÜ",
        "BELEDİYESİ", "BAKANLIĞI", "DEKANLIĞI", "REKTÖRLÜĞÜ", "MÜFETTİŞLİĞİ", "TEMSİLCİLİĞİ",
        "KOMİSYONU", "KURULU", "AJANSI", "DAİRESİ", "MAKAMİ", "BİRİMİ", "MÜSTEŞARLIĞI", "GENEL SEKRETERLİĞİ"
    ]
    org_birimleri_regex_str = "|".join(org_birimleri_liste)
    # Bu regex, "XYZ BELEDİYESİ" gibi tam bir kurum adını veya sadece "BELEDİYESİ" gibi bir ifadeyi (öncesinde başka kelimelerle) yakalar.
    pattern_full_org_name = r"^\s*((?:[\w\sÇŞĞÜÖİİçşğüöı\.\-]+\s+)?(?:{org_birimleri_regex_str}))\b".format(org_birimleri_regex_str=org_birimleri_regex_str)
    match = re.search(pattern_full_org_name, ilk_satirlar_metin, re.IGNORECASE | re.MULTILINE)
    if match:
        kurum_adi = match.group(1).strip().upper()
        if kurum_adi.startswith("SAYIN "):
            kurum_adi = kurum_adi[len("SAYIN "):].strip()
        # Eğer sadece "BAŞKANLIĞI" gibi genel bir birim adı yakalandıysa ve metinde "Belediye Başkanı" gibi bir ifade varsa, daha spesifik olalım.
        if kurum_adi in org_birimleri_liste and "BELEDİYE BAŞKANI" in ilk_satirlar_metin.upper():
             return "BELEDİYE"
        if kurum_adi: return kurum_adi

    # 3. Özel Hitap Kalıpları ve Anahtar Kelimeler
    # "Sayın Valilik Makamına" (Bu aslında 1. kuralda da yakalanabilir)
    # "Sayın Belediye Başkanı", "Değerli Belediye Yetkilileri", "Belediyenin veya ilgili kurumun"
    if re.search(r"\bSayın\s+Belediye\s+Başkanı\b", ilk_satirlar_metin, re.IGNORECASE) or \
       re.search(r"\bDeğerli\s+Belediye\s+Yetkilileri\b", ilk_satirlar_metin, re.IGNORECASE) or \
       re.search(r"\bBelediye(?:nin|si)?\s+(?:veya\s+ilgili\s+kurumun)?", ilk_satirlar_metin, re.IGNORECASE):
        # Metinde "XYZ BELEDİYESİ" gibi daha spesifik bir ifade var mı diye kontrol edelim (yukarıdaki 2. kuralda yakalanmadıysa).
        spesifik_belediye_match = re.search(r"^\s*((?:[\w\sÇŞĞÜÖİİçşğüöı\.\-]+\s+)?BELEDİYE(?:Sİ)?)\b", ilk_satirlar_metin, re.IGNORECASE | re.MULTILINE)
        if spesifik_belediye_match:
            kurum_adi = spesifik_belediye_match.group(1).strip().upper()
            if kurum_adi: return kurum_adi
        return "BELEDİYE" # Genel ifade

    # "Sayın Müdürlük"
    if re.search(r"\bSayın\s+Müdürlük\b", ilk_satirlar_metin, re.IGNORECASE):
        spesifik_mudurluk_match = re.search(r"^\s*((?:[\w\sÇŞĞÜÖİİçşğüöı\.\-]+\s+)?MÜDÜRLÜĞ(?:Ü|ÜNE))\b", ilk_satirlar_metin, re.IGNORECASE | re.MULTILINE)
        if spesifik_mudurluk_match:
             kurum_adi = spesifik_mudurluk_match.group(1).strip().upper()
             if kurum_adi: return kurum_adi
        return "MÜDÜRLÜK"

    # 4. "İlgili Birime"
    if re.search(r"\bİlgili\s+Birime\b", ilk_satirlar_metin, re.IGNORECASE):
        return "İLGİLİ BİRİM"

    # 5. Genel Yetkili Hitapları: "Sayın Yetkili", "Sayın İlgili"
    if re.search(r"\bSayın\s+(?:Yetkili|İlgili)\b", ilk_satirlar_metin, re.IGNORECASE):
        return "YETKİLİ MAKAM"

    # 6. "Merhaba", "Merhabalar" gibi ifadeler doğrudan kurum adı vermez.
    # Eğer metnin içinde "Belediyenin veya ilgili kurumun" gibi bir ifade geçiyorsa (özellikle talep kısmında)
    if "BELEDİYENİN VEYA İLGİLİ KURUMUN" in metin.upper(): # Tüm metinde ara
        return "BELEDİYE / İLGİLİ KURUM"

    return "Belirsiz."
    """
    Dilekçenin hitap ettiği kurumu veya şikayet edilen kurumu bulmaya çalışır.
    Güncellenmiş mantıkla çalışır.
    """
    # Metni satırlara böl ve boş satırları temizle
    satirlar = [satir.strip() for satir in metin.split('\n') if satir.strip()]
    
    # İlk 7 satırı al ve birleştir
    ilk_satirlar = satirlar[:7]
    ilk_satirlar_metin = "\n".join(ilk_satirlar)

    # 1. Doğrudan ve Tam Kurum Adı + Yönelme Eki
    pattern_name_with_affix = r"([\w\sÇŞĞÜÖİİçşğüöı\.\-]+?)\s*'?(?:NA|NE|Makamına)\b"
    match = re.search(pattern_name_with_affix, ilk_satirlar_metin, re.IGNORECASE)
    if match:
        kurum_adi = match.group(1).strip().upper()
        if kurum_adi.startswith("SAYIN "):
            kurum_adi = kurum_adi[len("SAYIN "):].strip()
        return kurum_adi

    # 2. Tam Kurum Adı
    org_birimleri = (
        r"MÜDÜRLÜĞÜ|BAŞKANLIĞI|VALİLİĞİ|KAYMAKAMLIĞI|DAİRE BAŞKANLIĞI|GENEL MÜDÜRLÜĞÜ|"
        r"BELEDİYESİ|BAKANLIĞI|DEKANLIĞI|REKTÖRLÜĞÜ|MÜFETTİŞLİĞİ|TEMSİLCİLİĞİ|"
        r"KOMİSYONU|KURULU|AJANSI|DAİRESİ|Makamı|Birimi|Müsteşarlığı|Genel Sekreterliği"
    )
    pattern_full_org_name = r"((?:[\w\sÇŞĞÜÖİİçşğüöı\.\-]+\s+)?(?:{org_birimleri}))\b".format(org_birimleri=org_birimleri)
    match = re.search(pattern_full_org_name, ilk_satirlar_metin, re.IGNORECASE)
    if match:
        kurum_adi = match.group(1).strip().upper()
        if kurum_adi.startswith("SAYIN "):
            kurum_adi = kurum_adi[len("SAYIN "):].strip()
        return kurum_adi

    # 3. Özel Hitap Kalıpları
    # "Sayın Valilik Makamına"
    if re.search(r"Sayın\s+Valilik\s+Makamına", ilk_satirlar_metin, re.IGNORECASE):
        return "VALİLİK"

    # "Sayın Belediye Başkanı", "Değerli Belediye Yetkilileri"
    if re.search(r"(?:Sayın\s+Belediye\s+Başkanı|Değerli\s+Belediye\s+Yetkilileri)", ilk_satirlar_metin, re.IGNORECASE):
        return "BELEDİYE"

    # "Sayın Müdürlük"
    if re.search(r"Sayın\s+Müdürlük", ilk_satirlar_metin, re.IGNORECASE):
        return "MÜDÜRLÜK"

    # "İlgili Birime"
    if re.search(r"İlgili\s+Birime", ilk_satirlar_metin, re.IGNORECASE):
        return "İLGİLİ BİRİM"

    # "Sayın Yetkili", "Sayın İlgili"
    if re.search(r"Sayın\s+(?:Yetkili|İlgili)", ilk_satirlar_metin, re.IGNORECASE):
        return "YETKİLİ MAKAM"

    # 4. Metin içinde kurum isimlerini ara
    kurum_regex = r"(?:Belediyesi|Valiliği|Müdürlüğü|Başkanlığı|Makamı|Kurumu|Kuruluşu)"
    kurum_eslesmeleri = re.findall(kurum_regex, metin, re.IGNORECASE)
    
    if kurum_eslesmeleri:
        kurum_sayilari = {}
        for kurum in kurum_eslesmeleri:
            kurum = kurum.lower()
            if "belediye" in kurum:
                kurum_sayilari["BELEDİYE"] = kurum_sayilari.get("BELEDİYE", 0) + 1
            elif "valilik" in kurum:
                kurum_sayilari["VALİLİK"] = kurum_sayilari.get("VALİLİK", 0) + 1
            elif "müdürlük" in kurum:
                kurum_sayilari["MÜDÜRLÜK"] = kurum_sayilari.get("MÜDÜRLÜK", 0) + 1
            elif "başkanlık" in kurum:
                kurum_sayilari["BAŞKANLIK"] = kurum_sayilari.get("BAŞKANLIK", 0) + 1
            elif "kurum" in kurum:
                kurum_sayilari["KURUM"] = kurum_sayilari.get("KURUM", 0) + 1
        
        if kurum_sayilari:
            return max(kurum_sayilari.items(), key=lambda x: x[1])[0]

    # 5. Belediyenin veya ilgili kurumun ifadesi
    if re.search(r"Belediyenin\s+veya\s+ilgili\s+kurumun", metin, re.IGNORECASE):
        return "BELEDİYE"

    return "İLGİLİ KURUM"  # Hiçbir şey bulunamazsa varsayılan değer

# Hata ayıklama için çıkarılan verileri tutacak bir liste
debug_output = []

for filename, metin in dilekce_metinleri.items():
    print(f"\n--- {filename} İŞLENİYOR ---")
    print("--- PDF'DEN ÇIKARILAN HAM METİN (İLK 500 KARAKTER) ---")
    print(metin[:500]) # Ham metnin bir kısmını gör
    print("----------------------------------------------------")

    kurum = kurum_adi_cikar(metin)
    print(f"  -> Çıkarılan Kurum: {kurum}")

    # Hata ayıklama için daha detaylı bilgi saklayalım
    ilk_satirlar_debug = "\n".join(metin.split('\n')[:7])
    debug_output.append({
        "dosya_adi": filename,
        "ilk_7_satir": ilk_satirlar_debug,
        "bulunan_kurum": kurum
    })

# Hata ayıklama sonuçlarını daha sonra incelemek için yazdırabilir veya dosyaya kaydedebilirsiniz.
print("\n--- HATA AYIKLAMA ÇIKTILARI ---")
for item in debug_output:
    print(f"Dosya: {item['dosya_adi']}, Kurum: {item['bulunan_kurum']}")
    # print(f"  İlk 7 Satır:\n{item['ilk_7_satir']}\n") # Gerekirse bunu da açın

def tarih_araliklari_cikar(metin):
    """Dilekçe metnindeki tarihleri ve tarih aralıklarını bulur."""
    bulunan_tarihler = []
    
    # Göreceli zaman ifadeleri
    goreceli_zaman_regex = r"(?:Geçtiğimiz|Son|Önceki)\s+(?:ay|hafta|gün|yıl|hafta\s+sonu|hafta\s+içi)"
    goreceli_zaman_eslesmeleri = re.findall(goreceli_zaman_regex, metin, re.IGNORECASE)
    bulunan_tarihler.extend(goreceli_zaman_eslesmeleri)
    
    # Süre ifadeleri (aydır, gündür, haftadır vb.)
    sure_regex = r"(?:\d+\s+(?:ay|hafta|gün|yıl|saat)|(?:bir|iki|üç|dört|beş|altı|yedi|sekiz|dokuz|on)\s+(?:ay|hafta|gün|yıl|saat))(?:dır|dir|den\s+beri|süredir|dır\s+arızalı|dir\s+arızalı)"
    sure_eslesmeleri = re.findall(sure_regex, metin, re.IGNORECASE)
    bulunan_tarihler.extend(sure_eslesmeleri)
    
    # Günün belirli saatleri
    saat_regex = r"(?:her\s+(?:gün|akşam|sabah|öğlen|gece))\s+(?:saat\s+)?(\d{1,2}:\d{2})"
    saat_eslesmeleri = re.findall(saat_regex, metin, re.IGNORECASE)
    bulunan_tarihler.extend([f"Her gün {saat}" for saat in saat_eslesmeleri])
    
    # Mevsim ve dönem ifadeleri
    donem_regex = r"(?:Kış|Yaz|İlkbahar|Sonbahar)\s+(?:aylarında|mevsiminde|döneminde)"
    donem_eslesmeleri = re.findall(donem_regex, metin, re.IGNORECASE)
    bulunan_tarihler.extend(donem_eslesmeleri)
    
    # Haftanın belirli günleri (Hafta sonları, Hafta içi günleri vb.)
    hafta_gunleri_regex = r"\b(?:Hafta\s+(?:içi|sonu)(?:leri|de|da)?|(?:Pazartesi|Salı|Çarşamba|Perşembe|Cuma|Cumartesi|Pazar)\s*(?:günleri|günü)?)\b"
    hafta_gunleri_eslesmeleri = re.findall(hafta_gunleri_regex, metin, re.IGNORECASE)
    if hafta_gunleri_eslesmeleri:
        # Eşleşmeleri normalize et
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
    gun_zamani_eslesmeleri = re.findall(gun_zamani_regex, metin, re.IGNORECASE)
    bulunan_tarihler.extend(gun_zamani_eslesmeleri)
    
    # Standart tarih formatları ve ay isimleriyle tarihler
    tarih_regex_cesitleri = [
        r'\b(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})\b',  # 01/01/2023, 01.01.2023, 01-01-2023
        r'\b(\d{1,2}\s+(?:Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık)(?:\'da|\'de)?)\b',  # 1 Haziran'da, 15 Mayıs
        r'\b(?:Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık)(?:\'da|\'de)?\b'  # Haziran'da, Mayıs'ta
    ]
    
    for regex_pattern in tarih_regex_cesitleri:
        eslesmeler = re.findall(regex_pattern, metin, re.IGNORECASE)
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
    d_tarih_eslesme = re.search(dilekce_tarihi_regex, metin, re.IGNORECASE)
    if d_tarih_eslesme:
        parsed_date_obj = parse_date(d_tarih_eslesme.group(1).strip(), languages=['tr'])
        if parsed_date_obj:
            dt_str = parsed_date_obj.strftime('%Y-%m-%d')
            if dt_str not in bulunan_tarihler:
                bulunan_tarihler.append(dt_str)
        elif d_tarih_eslesme.group(1).strip() not in bulunan_tarihler:
            bulunan_tarihler.append(d_tarih_eslesme.group(1).strip())
    
    return list(set(bulunan_tarihler))  # Tekrarları kaldır

def ad_soyad_cikar(metin):
    """Ad Soyad bilgisini metinden çıkarmaya çalışır."""
    # T.C. Kimlik No'ya yakın isimleri bul
    tc_kimlik_regex = r"T\.?C\.?\s*Kimlik\s*No\s*:\s*(\d{11})"
    tc_eslesme = re.search(tc_kimlik_regex, metin, re.IGNORECASE)
    
    if tc_eslesme:
        # T.C. Kimlik No'nun etrafındaki metinde isim arayalım
        tc_index = metin.find(tc_eslesme.group(0))
        etraf_metin = metin[max(0, tc_index-100):min(len(metin), tc_index+100)]
        
        # İsim formatı: İlk harfi büyük, sonraki harfler küçük + Boşluk + İlk harfi büyük, sonraki harfler küçük
        isim_regex = r"\b([A-ZÇŞĞÜÖİ][a-zçşğüöı]+)\s+([A-ZÇŞĞÜÖİ][a-zçşğüöı]+)\b"
        isim_eslesme = re.search(isim_regex, etraf_metin)
        if isim_eslesme:
            return f"{isim_eslesme.group(1)} {isim_eslesme.group(2)}"
    
    # Dilekçenin sonunda, genellikle imzanın üzerinde yer alır
    son_kisim = metin[int(len(metin)*0.75):]
    
    # "Adı Soyadı:" formatında arama
    ad_soyad_eslesme = re.search(r"(?:Adı\s+Soyadı|Ad\s+Soyad)\s*:\s*([A-Za-zÇŞĞÜÖİçşğüöı\s]+)", son_kisim, re.IGNORECASE)
    if ad_soyad_eslesme:
        return ad_soyad_eslesme.group(1).strip()
    
    # İmza üstü isimler için arama
    # İsim formatı: İlk harfi büyük, sonraki harfler küçük + Boşluk + İlk harfi büyük, sonraki harfler küçük
    imza_ustu_regex = r"\b([A-ZÇŞĞÜÖİ][a-zçşğüöı]+)\s+([A-ZÇŞĞÜÖİ][a-zçşğüöı]+)\b"
    imza_ustu_eslesme = re.search(imza_ustu_regex, son_kisim)
    if imza_ustu_eslesme:
        return f"{imza_ustu_eslesme.group(1)} {imza_ustu_eslesme.group(2)}"
    
    # Tüm metinde isim arama
    tum_metin_eslesme = re.search(imza_ustu_regex, metin)
    if tum_metin_eslesme:
        return f"{tum_metin_eslesme.group(1)} {tum_metin_eslesme.group(2)}"
    
    return None


def adres_cikar(metin):
    """Adres veya bölge bilgisini çıkarmaya çalışır."""
    # "Adres:" anahtar kelimesiyle başlayan satırları arayalım
    adres_regex = r"(?:Adres|ADRES)\s*:\s*([^\n]+)"
    eslesme = re.search(adres_regex, metin, re.IGNORECASE)
    if eslesme:
        return eslesme.group(1).strip()

    # İlçe/il formatını arayalım
    # Örnek: Kadıköy/İstanbul, Beşiktaş/İstanbul
    ilce_il_regex = r"([A-ZÇŞĞÜÖİ][a-zçşğüöı]+)\s*/\s*([A-ZÇŞĞÜÖİ][a-zçşğüöı]+)"
    
    # Metnin son çeyreğinde arama yapalım (genellikle iletişim bilgileri burada olur)
    son_kisim = metin[int(len(metin)*0.75):]
    
    # Son kısımda ilçe/il formatını ara
    eslesmeler = re.findall(ilce_il_regex, son_kisim)
    if eslesmeler:
        # En son bulunan eşleşmeyi al (genellikle en doğru olanı)
        son_eslesme = eslesmeler[-1]
        return f"{son_eslesme[0]}/{son_eslesme[1]}"
    
    # Eğer son kısımda bulunamazsa, tüm metinde ara
    eslesmeler = re.findall(ilce_il_regex, metin)
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

def olay_konusu_cikar(metin):
    """
    Dilekçenin ana konusunu (örneğin: yol sorunu, su kesintisi) bulmaya çalışır.
    BERT tabanlı Türkçe model kullanarak metin sınıflandırması yapar.
    """
    if not metin or not metin.strip():
        return None

    # Metni ön işleme
    # İlk 500 karakteri al (genellikle konu burada olur)
    metin = metin[:500].strip()
    
    # Gereksiz boşlukları temizle
    metin = re.sub(r'\s+', ' ', metin)
    
    # Konu kategorileri ve anahtar kelimeleri
    konu_kategorileri = {
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

    try:
        # BERT modeli ile sınıflandırma yap
        sonuc = classifier(metin)
        
        # En yüksek skorlu kategoriyi bul
        en_yuksek_skor = 0
        en_uygun_konu = None
        
        for kategori, anahtar_kelimeler in konu_kategorileri.items():
            # Anahtar kelime kontrolü
            anahtar_kelime_skoru = sum(1 for kelime in anahtar_kelimeler if kelime.lower() in metin.lower())
            
            # BERT modelinin skoru ile anahtar kelime skorunu birleştir
            toplam_skor = anahtar_kelime_skoru * 0.3 + sonuc[0]['score'] * 0.7
            
            if toplam_skor > en_yuksek_skor:
                en_yuksek_skor = toplam_skor
                en_uygun_konu = kategori

        # Eğer yeterince güvenilir bir sonuç bulunamadıysa
        if en_yuksek_skor < 0.3:
            # Metinde "Konu:" veya "Özet:" ile başlayan kısmı ara
            konu_regex = r"(?:Konu|KONU|Özet|ÖZET)\s*:\s*([^\n]+)"
            eslesme = re.search(konu_regex, metin, re.IGNORECASE)
            if eslesme:
                return eslesme.group(1).strip()
            return "Belirsiz Konu"
            
        return en_uygun_konu

    except Exception as e:
        print(f"Model çalıştırılırken hata oluştu: {e}")
        # Hata durumunda basit anahtar kelime kontrolü yap
        for kategori, anahtar_kelimeler in konu_kategorileri.items():
            if any(kelime.lower() in metin.lower() for kelime in anahtar_kelimeler):
                return kategori
        return "Belirsiz Konu"

def talep_cikar(metin):
    """Dilekçedeki ana talebi (örneğin: açıklama istemi, çözüm talebi) bulmaya çalışır."""
    # Genellikle "arz ederim", "talep ederim", "gereğini" gibi ifadelerle biter.
    # Bu ifadelerin geçtiği cümleleri veya bir önceki/sonraki cümleleri alabiliriz.
    talep_ifadeleri = [
        r"gereğini\s+saygılarımla\s+arz\s+ederim",
        r"gereğinin\s+yapılmasını\s+arz\s+ederim",
        r"çözümünü\s+talep\s+ediyorum",
        r"bilgi\s+verilmesini\s+rica\s+ederim",
        r"konunun\s+incelenmesini\s+arz\s+ederim",
        r"mağduriyetimin\s+giderilmesini\s+talep\s+ederim",
        r"denetlenmesini\s+talep\s+ederim",
        r"yapılmasını\s+arz\s+ve\s+talep\s+ederim"
    ]
    
    # Metnin sonlarına doğru arama yapmak daha mantıklıdır.
    son_kisim = metin[int(len(metin)*0.5):] # Metnin son yarısına bakalım

    for ifade_regex in talep_ifadeleri:
        # İfadenin geçtiği cümleyi bulmaya çalışalım.
        # Regex'i biraz daha esnek hale getirelim: ifadeyi içeren ve nokta ile biten kısım.
        # (.*?) non-greedy match yapar.
        cumle_regex = r"([^.\n]*" + ifade_regex + r"[^.\n]*\.)"
        eslesme = re.search(cumle_regex, son_kisim, re.IGNORECASE | re.DOTALL)
        if eslesme:
            return eslesme.group(1).strip().replace("\n", " ") # Bulunan cümleyi temizle

    # Eğer yukarıdaki kalıplar bulunamazsa, "talep", "arz", "rica" içeren son cümleler
    son_cumle_adaylari = re.findall(r"([^\n.]*(?:talep|arz|rica|istediğimi|istiyorum|beklemekteyim|öneririm)[^\n.]*\.)", son_kisim, re.IGNORECASE)
    if son_cumle_adaylari:
        son_cumle = son_cumle_adaylari[-1].strip().replace("\n", " ")
        if son_cumle: # Cümlenin boş olmadığından emin olalım
            return son_cumle[0].upper() + son_cumle[1:]
        else:
            return son_cumle # Boşsa olduğu gibi döndür

    return "Talep net olarak belirlenemedi."

# Ana işlem döngüsü öncesinde listeyi tanımla
extracted_data_list = []

for filename, metin in dilekce_metinleri.items():
    print(f"\n--- {filename} için bilgi çıkarımı yapılıyor ---")
    
    kurum = kurum_adi_cikar(metin)
    tarihler = tarih_araliklari_cikar(metin)
    ad_soyad = ad_soyad_cikar(metin)
    adres = adres_cikar(metin)
    konu = olay_konusu_cikar(metin)
    talep = talep_cikar(metin)

    # Hata ayıklama için çıktıları yazdırabiliriz
    print(f"  Kurum Adı: {kurum}")
    print(f"  Tarih(ler): {tarihler}")
    print(f"  Ad Soyad: {ad_soyad}")
    print(f"  Adres: {adres}")
    print(f"  Olay Konusu: {konu}")
    print(f"  Talep: {talep}")

    extracted_info = {
        "dosya_adi": filename,
        "Ad Soyad": ad_soyad,
        "Adres veya bölge bilgisi": adres,
        "Tarih aralıkları": tarihler, # Bu bir liste olacak
        "Kurum ismi": kurum,
        "Olay konusu": konu,
        "Talep": talep
    }
    extracted_data_list.append(extracted_info)

# Sonuçları bir JSON dosyasına yazdır
output_json_path = "dilekce_bilgileri.json"
with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(extracted_data_list, f, ensure_ascii=False, indent=4)

print(f"\n\nBilgi çıkarımı tamamlandı. Sonuçlar '{output_json_path}' dosyasına kaydedildi.")