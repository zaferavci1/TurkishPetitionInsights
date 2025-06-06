import streamlit as st
import tempfile
from pathlib import Path
import os
import sys

# Proje kök dizinini sys.path'e ekle
sys.path.append(str(Path(__file__).parent))

from src.extractors.text_extractor import TextExtractor
from src.extractors.name_extractor import NameExtractor
from src.extractors.address_extractor import AddressExtractor
from src.extractors.date_extractor import DateExtractor
from src.extractors.institution_extractor import InstitutionExtractor
from src.extractors.topic_extractor import TopicExtractor
from src.extractors.request_extractor import RequestExtractor
from src.extractors.inference_extractor import InferenceExtractor
from src.extractors.tone_language_analyzer import ToneLanguageAnalyzer

def analyze_petition(pdf_path):
    """Verilen PDF dosyasını analiz eder ve sonuçları döndürür."""
    
    # PDF'ten metin çıkar
    extracted_texts = TextExtractor.extract_from_directory(pdf_path.parent, specific_file=pdf_path.name)
    if not extracted_texts:
        return None
    
    # Sadece ilk dosyanın metnini al
    text = list(extracted_texts.values())[0]

    # Çıkarıcıları başlat
    extractors = {
        "Ad Soyad": NameExtractor(),
        "Adres": AddressExtractor(),
        "Tarih(ler)": DateExtractor(),
        "Kurum": InstitutionExtractor(),
        "Konu": TopicExtractor(),
        "Talep": RequestExtractor(),
        "Çıkarımlar": InferenceExtractor(),
        "Ton ve Dil Analizi": ToneLanguageAnalyzer()
    }

    # Bilgileri çıkar ve sakla
    results = {}
    for key, extractor in extractors.items():
        results[key] = extractor.extract(text)
        
    results["Metin"] = text
    return results

# Streamlit Arayüzü
st.set_page_config(page_title="Dilekçe Analiz Aracı", layout="wide")
st.title("📄 Dilekçe Analiz Aracı")
st.write("Lütfen analiz etmek istediğiniz dilekçe dosyasını (PDF formatında) yükleyin.")

uploaded_file = st.file_uploader("PDF Dosyanızı Buraya Sürükleyip Bırakın", type="pdf")

if uploaded_file is not None:
    # Geçici bir dosyaya yaz
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_pdf_path = Path(temp_dir) / uploaded_file.name
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner(f"**{uploaded_file.name}** analiz ediliyor... Lütfen bekleyin."):
            analysis_results = analyze_petition(temp_pdf_path)

    if analysis_results:
        st.success("Analiz başarıyla tamamlandı!")
        
        st.header("🔍 Analiz Sonuçları")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Kimlik ve Adres Bilgileri")
            st.info(f"**Ad Soyad:** {analysis_results.get('Ad Soyad', 'Bulunamadı')}")
            st.info(f"**Adres:** {analysis_results.get('Adres', 'Bulunamadı')}")

            st.subheader("Dilekçe Detayları")
            
            dates = analysis_results.get('Tarih(ler)')
            if isinstance(dates, list) and dates:
                st.info(f"**Tarih(ler):** {', '.join(dates)}")
            else:
                st.info(f"**Tarih(ler):** {dates or 'Bulunamadı'}")

            st.info(f"**Kurum:** {analysis_results.get('Kurum', 'Bulunamadı')}")
            st.info(f"**Konu:** {analysis_results.get('Konu', 'Bulunamadı')}")
            st.info(f"**Talep:** {analysis_results.get('Talep', 'Bulunamadı')}")

        with col2:
            st.subheader("Metin Analizi")
            tone_analysis = analysis_results.get('Ton ve Dil Analizi')
            if isinstance(tone_analysis, dict):
                md_output = ""
                if tone_analysis.get('ton'):
                    md_output += f"- **Ton:** {tone_analysis['ton']}\n"
                if tone_analysis.get('dil_resmiyeti'):
                    md_output += f"- **Dil Resmiyeti:** {tone_analysis['dil_resmiyeti']}\n"
                if tone_analysis.get('yazim_uyumu'):
                    md_output += f"- **Yazım Uyumu:** {tone_analysis['yazim_uyumu']}"
                st.info(md_output)
            else:
                st.info(tone_analysis or 'Bulunamadı')

            st.subheader("Anlamsal Çıkarımlar")
            inferences = analysis_results.get('Çıkarımlar')
            if isinstance(inferences, list) and inferences:
                md_output = ""
                for inference in inferences:
                    kodu = inference.get('çıkarım_kodu', '').replace('_', ' ').title()
                    aciklama = inference.get('açıklama', 'Açıklama yok')
                    tetikleyen = inference.get('tetikleyen_ifade', '')
                    md_output += f"- **{kodu}:** {aciklama} *(Tetikleyen: \"{tetikleyen}\")*\n"
                st.info(md_output)
            else:
                st.info(inferences or 'Bulunamadı')

        with st.expander("Dilekçe Metnini Görüntüle"):
            st.text_area("Metin", analysis_results.get('Metin', 'Metin çıkarılamadı.'), height=300)

    else:
        st.error("PDF dosyasından metin çıkarılamadı veya analiz sırasında bir hata oluştu.") 