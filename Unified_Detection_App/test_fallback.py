import requests

tests = [
    ("Obviously Fake", "BREAKING: Aliens have landed in Washington DC and are meeting with the President"),
    ("Obviously Real", "The Federal Reserve announced a quarter-point interest rate cut in their latest meeting"),
    ("Ambiguous", "Scientists claim a new treatment could potentially cure cancer within five years"),
]

for name, text in tests:
    r = requests.post("http://127.0.0.1:5000/api/detect/fakenews", json={"text": text})
    d = r.json()
    pred = d.get("prediction", "?")
    conf = d.get("confidence", "?")
    src = d.get("verification_source", "?")
    reason = d.get("verification_reason", "")
    arts = d.get("articles_found", "")
    extra = f" | reason: {reason} | articles: {arts}" if reason else ""
    print(f"[{name}] {pred} @ {conf}% | source: {src}{extra}")
