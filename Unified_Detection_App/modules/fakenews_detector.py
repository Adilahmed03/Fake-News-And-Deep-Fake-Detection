import os
from transformers import pipeline

class FakeNewsDetector:
    """Fake News Detection Module using Transformers"""
    
    def __init__(self, model_path=None, train_data_path=None):
        """Initialize the detector with a pre-trained HuggingFace Transformer model"""
        # We ignore local model_path and use the remote HuggingFace checkpoint 
        # for zero-shot text classification, fetching the optimal fake news BERT.
        self.hf_model_id = "jy46604790/Fake-News-Bert-Detect"
        self.pipeline = None
        self._load_model()
    
    def _load_model(self):
        """Load the pre-trained transformer model"""
        try:
            print(f"[INFO] Initializing HuggingFace Pipeline: {self.hf_model_id}")
            # The pipeline automatically handles Tokenizer and Model mapping.
            self.pipeline = pipeline("text-classification", model=self.hf_model_id)
            print(f"[OK] Fake news transformer pipeline loaded successfully")
        except Exception as e:
            print(f"[ERROR] Error initializing transformer Pipeline: {str(e)}")
            raise
    
    def preprocess_text(self, text):
        """Preprocess the input text (Transformers handle their own extensive tokenization)"""
        # We preserve this method signature for API compatibility, but limit preprocessing.
        # Transformers perform best on raw, correctly punctuated text.
        return str(text).strip()
    
    def predict(self, news_text):
        """
        Predict if the news is fake or real using semantic context
        
        Args:
            news_text (str): The news text to analyze
            
        Returns:
            dict: Prediction results with label and confidence
        """
        if not news_text or not news_text.strip():
            return {
                'error': 'Please provide news text to analyze',
                'success': False
            }
        
        try:
            raw_text = self.preprocess_text(news_text)
            
            # Run inference through the pipeline (truncating to BERT's 512 token max config if necessary)
            result = self.pipeline(raw_text, truncation=True, max_length=512)[0]
            
            # jy46604790/Fake-News-Bert-Detect mapping: 
            # LABEL_0 usually represents "Fake" / "Unreliable"
            # LABEL_1 usually represents "Real" / "Reliable"
            # We'll map accordingly and cast confidence
            label_id = result['label']
            transformer_confidence = float(result['score']) * 100
            
            if label_id == 'LABEL_1':
                is_real = True
                confidence = transformer_confidence
                label = "Real News"
                status = "authentic"
            else:
                is_real = False
                confidence = transformer_confidence
                label = "Fake News"
                status = "fake"
            
            # For JSON probabilities dictionary
            prob_fake = 100 - confidence if is_real else confidence
            prob_real = confidence if is_real else 100 - confidence
            
            return {
                'success': True,
                'prediction': label,
                'status': status,
                'confidence': round(confidence, 2),
                'is_real': is_real,
                'probabilities': {
                    'fake': round(prob_fake, 2),
                    'real': round(prob_real, 2)
                }
            }
            
        except Exception as e:
            return {
                'error': f'Error during prediction: {str(e)}',
                'success': False
            }
    
    def get_model_info(self):
        """Get information about the loaded model"""
        if self.pipeline:
            return {
                'model_type': 'Transformer (jy46604790/Fake-News-Bert-Detect)',
                'loaded': True
            }
        return {'loaded': False}
