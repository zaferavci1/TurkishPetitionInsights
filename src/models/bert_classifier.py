import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from config.config import MODEL_NAME, NUM_LABELS

class BertClassifier:
    def __init__(self):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                MODEL_NAME, 
                num_labels=NUM_LABELS
            )
            self.classifier = pipeline(
                "text-classification", 
                model=self.model, 
                tokenizer=self.tokenizer
            )
        except Exception as e:
            print(f"Model yüklenirken hata oluştu: {e}")
            print("Lütfen transformers ve torch kütüphanelerinin yüklü olduğundan emin olun.")
            print("pip install transformers torch")
            raise

    def classify_text(self, text):
        """
        Verilen metni sınıflandırır.
        """
        try:
            result = self.classifier(text)
            return result[0]
        except Exception as e:
            print(f"Sınıflandırma sırasında hata oluştu: {e}")
            return None 