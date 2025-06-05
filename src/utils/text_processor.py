import re

def clean_text(text):
    """
    Metni temizler ve normalize eder.
    """
    if not text:
        return ""
    
    # Gereksiz boşlukları temizle
    text = re.sub(r'\s+', ' ', text)
    
    # Satır sonlarını normalize et
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Boş satırları temizle
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    return '\n'.join(lines)

def get_first_n_lines(text, n=10):
    """
    Metnin ilk n satırını döndürür.
    """
    lines = text.split('\n')
    return '\n'.join(lines[:n])

def normalize_turkish_chars(text):
    """
    Türkçe karakterleri normalize eder.
    """
    replacements = {
        'ı': 'i', 'İ': 'I',
        'ğ': 'g', 'Ğ': 'G',
        'ü': 'u', 'Ü': 'U',
        'ş': 's', 'Ş': 'S',
        'ö': 'o', 'Ö': 'O',
        'ç': 'c', 'Ç': 'C'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text 