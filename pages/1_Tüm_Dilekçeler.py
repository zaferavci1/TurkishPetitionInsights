import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="Tüm Dilekçe Analizleri", layout="wide")

st.title("🗂️ Tüm Dilekçe Analizleri")
st.write("Bu sayfada, analiz edilmiş tüm dilekçelerin sonuçlarını toplu olarak görebilirsiniz.")

# Proje kök dizinini baz alarak JSON dosyasının yolunu oluştur
# Bu betik 'pages' klasöründe olduğu için üst dizine çıkıyoruz (../)
json_path = Path(__file__).parent.parent / "output" / "results" / "dilekce_bilgileri.json"

if json_path.exists():
    with open(json_path, 'r', encoding='utf-8') as f:
        all_petitions_data = json.load(f)

    if not all_petitions_data:
        st.warning("Analiz edilmiş dilekçe bulunamadı.")
    else:
        # Dilekçeleri ters sırada göster (en son eklenen en üstte)
        for petition in reversed(all_petitions_data):
            file_name = petition.get("dosya_adi", "İsimsiz Dilekçe")
            with st.expander(f"**{file_name}**"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Kimlik ve Adres Bilgileri")
                    ad_soyad = petition.get('Ad Soyad', 'Bulunamadı').replace('\\n', ' ')
                    st.info(f"**Ad Soyad:** {ad_soyad}")
                    st.info(f"**Adres:** {petition.get('Adres', 'Bulunamadı')}")
                    
                    st.subheader("Dilekçe Detayları")
                    dates = petition.get('Tarih(ler)')
                    if isinstance(dates, list) and dates:
                        st.info(f"**Tarih(ler):** {', '.join(dates)}")
                    else:
                        st.info(f"**Tarih(ler):** {dates or 'Bulunamadı'}")
                    
                    st.info(f"**Kurum:** {petition.get('Kurum', 'Bulunamadı')}")
                    st.info(f"**Konu:** {petition.get('Konu', 'Bulunamadı')}")
                    talep = petition.get('Talep', 'Bulunamadı').replace('\\n', ' ')
                    st.info(f"**Talep:** {talep}")

                with col2:
                    st.subheader("Metin Analizi")
                    tone_analysis = petition.get('Ton ve Dil Analizi')
                    if isinstance(tone_analysis, dict):
                        md_output = ""
                        if tone_analysis.get('ton'):
                            md_output += f"- **Ton:** {tone_analysis['ton']}\\n"
                        if tone_analysis.get('dil_resmiyeti'):
                            md_output += f"- **Dil Resmiyeti:** {tone_analysis['dil_resmiyeti']}\\n"
                        if tone_analysis.get('yazim_uyumu'):
                            md_output += f"- **Yazım Uyumu:** {tone_analysis['yazim_uyumu']}"
                        st.info(md_output)
                    else:
                        st.info(tone_analysis or 'Bulunamadı')

                    st.subheader("Anlamsal Çıkarımlar")
                    inferences = petition.get('Çıkarımlar')
                    if isinstance(inferences, list) and inferences:
                        md_output = ""
                        for inference in inferences:
                            kodu = inference.get('çıkarım_kodu', '').replace('_', ' ').title()
                            aciklama = inference.get('açıklama', 'Açıklama yok')
                            tetikleyen = inference.get('tetikleyen_ifade', '')
                            md_output += f"- **{kodu}:** {aciklama} *(Tetikleyen: \"{tetikleyen}\")*\\n"
                        st.info(md_output)
                    else:
                        st.info(inferences or 'Bulunamadı')
else:
    st.error(f"Analiz sonuçları dosyası bulunamadı: '{json_path}'") 