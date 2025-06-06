# TurkishPetitionInsights: Türkçe Dilekçe Metinlerinin NLP Tabanlı Analizi

Bu proje, Türkiye'deki dilekçe metinlerini anlama ve analiz etme üzerine odaklanmış bir doğal dil işleme (NLP) projesidir. Proje, dilekçe metinlerini derinlemesine inceleyerek, metinlerden anlamlı bilgiler çıkarmayı ve bu bilgileri görselleştirmeyi amaçlamaktadır.

## Özellikler

* **Veri Toplama ve İşleme:** Farklı kaynaklardan toplanan dilekçe metinlerinin temizlenmesi, ön işlenmesi ve yapılandırılması.
* **Doğal Dil İşleme (NLP):** Metinler üzerinde konu modellemesi, duygu analizi, anahtar kelime çıkarma gibi NLP tekniklerinin uygulanması.
* **Görselleştirme:** Analiz sonuçlarının etkileşimli grafikler ve tablolar ile sunulması.
* **Web Uygulaması:** Streamlit tabanlı arayüz ile kullanıcıların analizleri kolayca inceleyebilmesi.

## Teknik Detaylar

### Yaklaşım ve Mimari
Proje, yapısal olmayan dilekçe metinlerinden (PDF) yapısal veriler (isim, tarih, konu, talep vb.) çıkarmak için modüler bir mimari kullanır. Her bir bilgi türü, `src/extractors` altında kendi özel "Extractor" sınıfı tarafından işlenir. Bu yaklaşım, sistemin bakımını ve yeni analiz yetenekleri eklenmesini kolaylaştırır.

### Kullanılan Kütüphaneler ve Yöntemler
- **Metin Çıkarma:** PDF dosyalarından metin içeriğini okumak için `PyPDF2` kütüphanesi kullanılmıştır.
- **Kural Tabanlı Bilgi Çıkarımı:** İsim, adres, kurum, belirli tarihler ve açık talepler gibi net ifadeleri metinden ayıklamak için **Düzenli İfadeler (Regular Expressions - RegEx)** yoğun olarak kullanılmıştır. `RequestExtractor` ve `AddressExtractor` gibi sınıflar bu yönteme dayanır.
- **Tarih Analizi:** Metin içinde geçen çeşitli formatlardaki tarih ifadelerini ("iki hafta önce", "01.01.2024" vb.) tanımak ve normalleştirmek için `dateparser` kütüphanesinden yararlanılmıştır.
- **Derin Öğrenme ile Anlamsal Çıkarım:** Metnin tonu, dilin resmiyeti ve alt metinde yatan imalar gibi daha karmaşık ve yoruma dayalı bilgileri çıkarmak için **Hugging Face Transformers** ve `PyTorch` tabanlı önceden eğitilmiş bağlamsal dil modelleri kullanılmıştır. `ToneLanguageAnalyzer` ve `InferenceExtractor` bu modern NLP yaklaşımını uygular.
- **Web Arayüzü:** Analiz sonuçlarını kullanıcı dostu bir arayüzde sunmak, dosya yükleme ve sonuçları görselleştirmek için `Streamlit` tercih edilmiştir.

## Kurulum

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları takip edebilirsiniz.

**1. Projeyi Klonlayın:**

İlk olarak, projeyi GitHub'dan yerel makinenize klonlayın:

```bash
git clone https://github.com/zaferavci1/TurkishPetitionInsights.git
```

**2. Proje Dizinine Gidin:**

Klonladığınız proje dizinine girin:

```bash
cd TurkishPetitionInsights
```

**3. Gerekli Kütüphaneleri Yükleyin:**

Projenin çalışması için gerekli olan Python kütüphanelerini `requirements.txt` dosyasını kullanarak yükleyin:

```bash
pip install -r requirements.txt
```

## Kullanım

Projenin web arayüzünü başlatmak için aşağıdaki komutu çalıştırın:

```bash
streamlit run app.py
```

Bu komutu çalıştırdıktan sonra, web tarayıcınızda otomatik olarak bir sayfa açılacak ve uygulamayı kullanmaya başlayabileceksiniz.

## Proje Yapısı

```
TurkishPetitionInsights/
│
├── config/                  # Konfigürasyon dosyaları / Configuration files
├── data/                    # Ham ve işlenmiş veriler / Raw and processed data
├── output/                  # Analiz sonuçları ve çıktılar / Analysis results and outputs
│   └── results/
├── src/                     # Kaynak kodlar / Source code
│
├── .gitattributes
├── app.py                   # Streamlit web uygulaması / Streamlit web application
├── case_study_kornext.pdf   # Proje ile ilgili vaka çalışması / Case study related to the project
├── dilekce_bilgileri.json   # Dilekçe bilgileri / Petition information
├── load_data.py             # Veri yükleme betiği / Data loading script
├── main.py                  # Ana analiz betiği / Main analysis script
└── requirements.txt         # Gerekli kütüphaneler / Required libraries
```

## Katkıda Bulunma

Projeye katkıda bulunmak isterseniz, lütfen bir "issue" açın veya "pull request" gönderin. Her türlü katkıya açığız!

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakabilirsiniz.

---

# TurkishPetitionInsights: NLP-Based Analysis of Turkish Petition Texts

This project is a Natural Language Processing (NLP) project focused on understanding and analyzing petition texts in Turkey. The project aims to perform an in-depth analysis of petition texts to extract meaningful information and visualize this data.

## Features

*   **Data Collection and Processing:** Cleaning, preprocessing, and structuring petition texts collected from various sources.
*   **Natural Language Processing (NLP):** Applying NLP techniques such as topic modeling, sentiment analysis, and keyword extraction on the texts.
*   **Visualization:** Presenting analysis results with interactive charts and tables.
*   **Web Application:** A Streamlit-based interface for users to easily review the analysis.

## Technical Details

### Approach and Architecture
The project uses a modular architecture to extract structured data (name, date, subject, request, etc.) from unstructured petition texts (PDFs). Each type of information is processed by its own dedicated "Extractor" class under `src/extractors`. This approach simplifies system maintenance and the addition of new analysis capabilities.

### Libraries and Methods Used
- **Text Extraction:** The `PyPDF2` library is used to read text content from PDF files.
- **Rule-Based Information Extraction:** **Regular Expressions (RegEx)** are heavily used to extract clear statements from the text, such as names, addresses, institutions, specific dates, and explicit requests. Classes like `RequestExtractor` and `AddressExtractor` rely on this method.
- **Date Analysis:** The `dateparser` library is utilized to recognize and normalize date expressions in various formats found in the text (e.g., "two weeks ago," "01.01.2024").
- **Semantic Extraction with Deep Learning:** Pre-trained language models based on **Hugging Face Transformers** and `PyTorch` are used to extract more complex and interpretive information, such as the tone of the text, language formality, and underlying implications. `ToneLanguageAnalyzer` and `InferenceExtractor` implement this modern NLP approach.
- **Web Interface:** `Streamlit` was chosen to present the analysis results in a user-friendly interface, handle file uploads, and visualize the outcomes.

## Installation

You can follow the steps below to run the project on your local machine.

**1. Clone the Project:**

First, clone the project from GitHub to your local machine:

```bash
git clone https://github.com/zaferavci1/TurkishPetitionInsights.git
```

**2. Navigate to the Project Directory:**

Enter the cloned project directory:

```bash
cd TurkishPetitionInsights
```

**3. Install Required Libraries:**

Install the necessary Python libraries for the project using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Usage

Run the following command to launch the project's web interface:

```bash
streamlit run app.py
```

After running this command, a page will automatically open in your web browser, and you can start using the application.

## Project Structure

The project structure is detailed in the Turkish section above.

## Contributing

If you would like to contribute to the project, please open an "issue" or submit a "pull request". All contributions are welcome!

## License

This project is licensed under the MIT License. For more information, see the `LICENSE` file.