import PyPDF2
from pathlib import Path
from typing import Dict, Optional

class TextExtractor:
    @staticmethod
    def extract_from_pdf(pdf_path: Path) -> Optional[str]:
        """
        PDF dosyasından metin içeriğini çıkarır.
        """
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            print(f"Hata: {pdf_path} dosyasından metin okunurken sorun oluştu - {e}")
            return None

    @staticmethod
    def extract_from_directory(directory: Path) -> Dict[str, str]:
        """
        Belirtilen dizindeki tüm PDF dosyalarından metin çıkarır.
        """
        extracted_texts = {}
        
        if not directory.exists():
            print(f"'{directory}' adlı klasör bulunamadı.")
            return extracted_texts
            
        for pdf_file in directory.glob("*.pdf"):
            print(f"{pdf_file.name} işleniyor...")
            text = TextExtractor.extract_from_pdf(pdf_file)
            if text:
                extracted_texts[pdf_file.name] = text
                
        print(f"\nToplam {len(extracted_texts)} adet PDF dosyası başarıyla okundu.")
        return extracted_texts 