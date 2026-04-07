import os
from transformers import pipeline


class FakeNewsDetector:
    """Fake News Detection with BERT + Real-Time Fallback Verification"""

    # Confidence thresholds for fallback gating
    HIGH_CONFIDENCE = 70  # Above this → trust BERT
    LOW_CONFIDENCE = 30   # Below this → trust BERT (opposite label is strong)

    def __init__(self, model_path=None, train_data_path=None, verifier=None):
        """Initialize with a pre-trained HuggingFace Transformer + optional verifier"""
        self.hf_model_id = "jy46604790/Fake-News-Bert-Detect"
        self.pipeline = None
        self.verifier = verifier  # NewsVerifier instance (always-on when provided)
        self._load_model()

    def _load_model(self):
        """Load the pre-trained transformer model"""
        try:
            print(f"[INFO] Initializing HuggingFace Pipeline: {self.hf_model_id}")
            self.pipeline = pipeline("text-classification", model=self.hf_model_id)
            print(f"[OK] Fake news transformer pipeline loaded successfully")
            if self.verifier:
                print("[OK] Real-time fallback verification: ENABLED (always-on)")
            else:
                print("[INFO] Real-time fallback verification: DISABLED (no verifier)")
        except Exception as e:
            print(f"[ERROR] Error initializing transformer Pipeline: {str(e)}")
            raise

    def preprocess_text(self, text):
        """Preprocess the input text"""
        return str(text).strip()

    def predict(self, news_text):
        """
        Predict if the news is fake or real.
        Uses BERT as primary, with NewsAPI+Gemini fallback for ambiguous cases.
        """
        if not news_text or not news_text.strip():
            return {
                'error': 'Please provide news text to analyze',
                'success': False
            }

        try:
            raw_text = self.preprocess_text(news_text)

            # ── Step 1: BERT Primary Prediction ──
            result = self.pipeline(raw_text, truncation=True, max_length=512)[0]

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

            prob_fake = 100 - confidence if is_real else confidence
            prob_real = confidence if is_real else 100 - confidence

            bert_result = {
                'success': True,
                'prediction': label,
                'status': status,
                'confidence': round(confidence, 2),
                'is_real': is_real,
                'probabilities': {
                    'fake': round(prob_fake, 2),
                    'real': round(prob_real, 2)
                },
                'verification_source': 'bert_model'
            }

            # ── Step 2: Confidence Gating ──
            # If BERT says Real with high confidence → trust it
            if is_real and confidence >= self.HIGH_CONFIDENCE:
                return bert_result
            
            # If BERT says Fake → ALWAYS verify (BERT is often wrong on factual statements)
            # If BERT is ambiguous (30-70%) → also verify
            if not self.verifier:
                # No verifier available → return BERT result as-is
                return bert_result

            trigger = "Fake prediction" if not is_real else f"ambiguous ({confidence:.1f}%)"
            print(f"[INFO] BERT {trigger} — triggering fallback verification")

            try:
                fallback = self.verifier.verify(raw_text)
                fallback_label = fallback.get('label', 'Uncertain')
                fallback_reason = fallback.get('reason', '')
                articles_found = fallback.get('articles_found', 0)

                # Map fallback result
                if fallback_label == 'Real':
                    return {
                        'success': True,
                        'prediction': 'Real News',
                        'status': 'authentic',
                        'confidence': 92.0,
                        'is_real': True,
                        'probabilities': {'fake': 8.0, 'real': 92.0},
                        'verification_source': 'gemini_verified',
                        'verification_reason': fallback_reason,
                        'articles_found': articles_found
                    }
                elif fallback_label == 'Fake':
                    return {
                        'success': True,
                        'prediction': 'Fake News',
                        'status': 'fake',
                        'confidence': 95.0,
                        'is_real': False,
                        'probabilities': {'fake': 95.0, 'real': 5.0},
                        'verification_source': 'gemini_verified',
                        'verification_reason': fallback_reason,
                        'articles_found': articles_found
                    }
                elif fallback_label == 'Misleading':
                    return {
                        'success': True,
                        'prediction': 'Misleading',
                        'status': 'misleading',
                        'confidence': 88.0,
                        'is_real': False,
                        'probabilities': {'fake': 70.0, 'real': 30.0},
                        'verification_source': 'gemini_verified',
                        'verification_reason': fallback_reason,
                        'articles_found': articles_found
                    }
                else:
                    # Uncertain — return original BERT result
                    bert_result['verification_source'] = 'bert_model (gemini_uncertain)'
                    return bert_result

            except Exception as e:
                print(f"[WARNING] Fallback verification failed: {e}")
                bert_result['verification_source'] = 'bert_model (fallback_error)'
                return bert_result

        except Exception as e:
            return {
                'error': f'Error during prediction: {str(e)}',
                'success': False
            }

    def get_model_info(self):
        """Get information about the loaded model"""
        info = {
            'model_type': 'Transformer (jy46604790/Fake-News-Bert-Detect)',
            'loaded': self.pipeline is not None,
            'realtime_verification': self.verifier is not None
        }
        return info
