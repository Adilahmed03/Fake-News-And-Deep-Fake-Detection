import os
import requests
import google.generativeai as genai


class NewsVerifier:
    """Real-time news verification using NewsAPI + Google Gemini"""

    def __init__(self, news_api_key=None, gemini_api_key=None):
        self.news_api_key = news_api_key or os.environ.get('NEWS_API_KEY')
        self.gemini_api_key = gemini_api_key or os.environ.get('GEMINI_API_KEY')
        self.gemini_model = None

        if self.gemini_api_key:
            try:
                genai.configure(api_key=self.gemini_api_key)
                # Try models in order of preference
                for model_name in ['gemini-2.5-flash-preview-04-17', 'gemini-2.0-flash', 'gemma-3-4b-it']:
                    try:
                        self.gemini_model = genai.GenerativeModel(model_name)
                        # Quick test to verify model works
                        self.gemini_model.generate_content('test')
                        print(f"[OK] Gemini verifier initialized ({model_name})")
                        break
                    except Exception:
                        continue
                else:
                    print("[WARNING] No Gemini model available — verification will use news-only fallback")
            except Exception as e:
                print(f"[WARNING] Gemini init failed: {e}")

        if self.news_api_key:
            print("[OK] NewsAPI key loaded")
        else:
            print("[WARNING] NEWS_API_KEY not set — fallback disabled")

    def _extract_keywords(self, text, max_words=4):
        """Extract key search terms from the claim text"""
        import re
        stop_words = {
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'has', 'have',
            'had', 'be', 'been', 'being', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'shall', 'can',
            'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
            'as', 'into', 'through', 'during', 'before', 'after', 'and',
            'but', 'or', 'nor', 'not', 'so', 'yet', 'both', 'either',
            'that', 'this', 'these', 'those', 'it', 'its', 'he', 'she',
            'they', 'them', 'his', 'her', 'their', 'my', 'your', 'our',
            'i', 'we', 'you', 'me', 'us', 'who', 'whom', 'which', 'what',
            'when', 'where', 'how', 'why', 'if', 'then', 'than', 'about',
            'just', 'also', 'very', 'really', 'all', 'any', 'some', 'no',
            'more', 'most', 'other', 'each', 'every', 'such', 'only',
            'own', 'same', 'too', 'up', 'out', 'off', 'over', 'under',
            'again', 'further', 'once', 'here', 'there', 'says', 'said',
            'new', 'now', 'many', 'much', 'get', 'got', 'make', 'made',
        }
        words = re.findall(r'[a-zA-Z]{3,}', text.lower())
        keywords = [w for w in words if w not in stop_words]
        # Deduplicate while preserving order
        seen = set()
        unique = []
        for w in keywords:
            if w not in seen:
                seen.add(w)
                unique.append(w)
        return ' '.join(unique[:max_words])

    def fetch_articles(self, text, top_n=5):
        """Fetch real-time news articles related to the claim"""
        if not self.news_api_key:
            return []

        query = self._extract_keywords(text)
        if not query:
            return []

        try:
            resp = requests.get(
                'https://newsapi.org/v2/everything',
                params={
                    'q': query,
                    'sortBy': 'relevancy',
                    'pageSize': top_n,
                    'language': 'en',
                    'apiKey': self.news_api_key,
                },
                timeout=5
            )
            data = resp.json()
            if data.get('status') != 'ok':
                print(f"[WARNING] NewsAPI error: {data.get('message', 'unknown')}")
                return []

            articles = []
            for art in data.get('articles', []):
                title = art.get('title', '').strip()
                desc = art.get('description', '').strip()
                if title and title != '[Removed]':
                    articles.append(f"{title}. {desc}" if desc else title)
            return articles

        except Exception as e:
            print(f"[WARNING] NewsAPI fetch failed: {e}")
            return []

    def verify_with_gemini(self, claim, articles):
        """Send claim + articles to Gemini for classification"""
        if not self.gemini_model:
            return None

        articles_text = '\n'.join(
            f"{i+1}. {a}" for i, a in enumerate(articles)
        )

        prompt = f"""You are a fact-checking assistant.

Claim: {claim}

Verified news articles:
{articles_text}

Task:
Compare the claim with the articles above and classify it as one of:
- Real
- Fake
- Misleading

Return ONLY a JSON object with two keys:
{{"label": "Real" or "Fake" or "Misleading", "reason": "one short sentence"}}
"""

        try:
            response = self.gemini_model.generate_content(prompt)
            text = response.text.strip()

            # Parse JSON from response
            import json
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                label = result.get('label', '').strip()
                reason = result.get('reason', '').strip()
                if label in ('Real', 'Fake', 'Misleading'):
                    return {'label': label, 'reason': reason}

            # Fallback: check for keywords in raw text
            text_lower = text.lower()
            if 'fake' in text_lower:
                return {'label': 'Fake', 'reason': text[:100]}
            elif 'real' in text_lower:
                return {'label': 'Real', 'reason': text[:100]}
            elif 'misleading' in text_lower:
                return {'label': 'Misleading', 'reason': text[:100]}

            return None

        except Exception as e:
            print(f"[WARNING] Gemini verification failed: {e}")
            return None

    def verify_with_gemini_standalone(self, claim):
        """Ask Gemini to classify a claim using its own knowledge (no articles)"""
        if not self.gemini_model:
            return None

        prompt = f"""You are a fact-checking assistant.

Claim: {claim}

No news articles were found for this claim. Use your own knowledge to classify it as one of:
- Real (if this is a well-known, verifiable fact)
- Fake (if this is clearly false or fabricated)
- Misleading (if partially true but distorted)

Return ONLY a JSON object with two keys:
{{"label": "Real" or "Fake" or "Misleading", "reason": "one short sentence"}}
"""
        try:
            response = self.gemini_model.generate_content(prompt)
            text = response.text.strip()
            import json as _json
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                result = _json.loads(json_match.group())
                label = result.get('label', '').strip()
                reason = result.get('reason', '').strip()
                if label in ('Real', 'Fake', 'Misleading'):
                    return {'label': label, 'reason': reason}
            text_lower = text.lower()
            if 'real' in text_lower:
                return {'label': 'Real', 'reason': text[:100]}
            elif 'fake' in text_lower:
                return {'label': 'Fake', 'reason': text[:100]}
            return None
        except Exception as e:
            print(f"[WARNING] Gemini standalone verification failed: {e}")
            return None

    def verify(self, claim):
        """Full verification pipeline: NewsAPI → Gemini"""
        # Step 1: Fetch articles
        articles = self.fetch_articles(claim)

        if not articles:
            # No articles found — try Gemini standalone (general knowledge)
            if self.gemini_model:
                gemini_result = self.verify_with_gemini_standalone(claim)
                if gemini_result:
                    return {
                        'label': gemini_result['label'],
                        'reason': gemini_result['reason'],
                        'source': 'gemini_standalone',
                        'articles_found': 0
                    }
            # Both failed
            return {
                'label': 'Fake',
                'reason': 'No matching news articles found from verified sources',
                'source': 'news_absence',
                'articles_found': 0
            }

        # Step 2: Verify with Gemini using articles
        gemini_result = self.verify_with_gemini(claim, articles)

        if gemini_result:
            return {
                'label': gemini_result['label'],
                'reason': gemini_result['reason'],
                'source': 'gemini_verification',
                'articles_found': len(articles)
            }

        # Gemini failed but articles exist — use news-presence heuristic
        return {
            'label': 'Real',
            'reason': f'Claim corroborated by {len(articles)} verified news source(s)',
            'source': 'news_presence',
            'articles_found': len(articles)
        }
