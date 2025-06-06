# TurkishPetitionInsights: Türkçe Dilekçe Metinlerinin NLP Tabanlı Analizi

Bu proje, Türkiye'deki dilekçe metinlerini anlama ve analiz etme üzerine odaklanmış bir doğal dil işleme (NLP) projesidir. Proje, dilekçe metinlerini derinlemesine inceleyerek, metinlerden anlamlı bilgiler çıkarmayı ve bu bilgileri görselleştirmeyi amaçlamaktadır.

## Özellikler

* **Veri Toplama ve İşleme:** Farklı kaynaklardan toplanan dilekçe metinlerinin temizlenmesi, ön işlenmesi ve yapılandırılması.
* **Doğal Dil İşleme (NLP):** Metinler üzerinde konu modellemesi, duygu analizi, anahtar kelime çıkarma gibi NLP tekniklerinin uygulanması.
* **Görselleştirme:** Analiz sonuçlarının etkileşimli grafikler ve tablolar ile sunulması.
* **Web Uygulaması:** Streamlit tabanlı arayüz ile kullanıcıların analizleri kolayca inceleyebilmesi.

## Kurulum

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları takip edebilirsiniz.

**1. Projeyi Klonlayın:**

İlk olarak, projeyi GitHub'dan yerel makinenize klonlayın:

```bash
git clone [https://github.com/zaferavci1/TurkishPetitionInsights.git](https://github.com/zaferavci1/TurkishPetitionInsights.git)
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
├── config/                  # Konfigürasyon dosyaları
├── data/                    # Ham ve işlenmiş veriler
├── output/                  # Analiz sonuçları ve çıktılar
│   └── results/
├── src/                     # Kaynak kodlar
│
├── .gitattributes
├── app.py                   # Streamlit web uygulaması
├── case_study_kornext.pdf   # Proje ile ilgili vaka çalışması
├── dilekce_bilgileri.json   # Dilekçe bilgileri
├── load_data.py             # Veri yükleme betiği
├── main.py                  # Ana analiz betiği
└── requirements.txt         # Gerekli kütüphaneler
```

## Katkıda Bulunma

Projeye katkıda bulunmak isterseniz, lütfen bir "issue" açın veya "pull request" gönderin. Her türlü katkıya açığız!

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakabilirsiniz.