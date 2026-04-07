import requests, json

text = "pm modi is prime mininster of india"
print(f"Input: '{text}'")
print()

r = requests.post("http://127.0.0.1:5000/api/detect/fakenews", json={"text": text})
d = r.json()
print(f"  prediction:  {d.get('prediction')}")
print(f"  confidence:  {d.get('confidence')}%")
print(f"  is_real:     {d.get('is_real')}")
print(f"  source:      {d.get('verification_source')}")
print(f"  reason:      {d.get('verification_reason', 'N/A')}")
print(f"  articles:    {d.get('articles_found', 'N/A')}")
