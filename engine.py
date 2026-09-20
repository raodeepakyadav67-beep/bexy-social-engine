import os
import requests

GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "").strip()

# 1. Gemini API Direct Call
gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"

payload = {
    "contents": [{
        "parts": [{
            "text": "Write a high-yield ICU Clinical Pearl for critical care nurses under 80 words with bullet points and #ICUNursing #Bexyhub."
        }]
    }]
}

res = requests.post(gemini_url, json=payload)
data = res.json()

if "candidates" not in data:
    print(f"Gemini API Response: {data}")
    raise Exception("Gemini Content Generation Failed!")

post_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
print("SUCCESS: AI Content Generated!")

# 2. Telegram Send Message
telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
tg_res = requests.post(telegram_url, json={"chat_id": CHANNEL_ID, "text": post_text})

print(f"Telegram Status: {tg_res.status_code}")
if tg_res.status_code != 200:
    print(f"Telegram Response: {tg_res.text}")
    raise Exception("Telegram Posting Failed!")

print("SUCCESS: Post Published to Telegram Channel!")
