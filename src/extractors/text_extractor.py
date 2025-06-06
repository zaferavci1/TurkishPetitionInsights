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
    def extract_from_directory(directory: Path, specific_file: Optional[str] = None) -> Dict[str, str]:
        """
        Belirtilen dizindeki tüm PDF dosyalarından veya belirli bir dosyadan metin çıkarır.
        """
        extracted_texts = {}
        
        if not directory.exists():
            print(f"'{directory}' adlı klasör bulunamadı.")
            return extracted_texts

        files_to_process = [directory / specific_file] if specific_file else list(directory.glob("*.pdf"))
            
        for pdf_file in files_to_process:
            if not pdf_file.exists():
                print(f"Hata: {pdf_file} bulunamadı.")
                continue

            print(f"{pdf_file.name} işleniyor...")
            text = TextExtractor.extract_from_pdf(pdf_file)
            if text:
                extracted_texts[pdf_file.name] = text
                
        if not specific_file:
            print(f"\nToplam {len(extracted_texts)} adet PDF dosyası başarıyla okundu.")
        return extracted_texts 