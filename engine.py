import os
import requests

GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "").strip()

# 1. Gemini API Call
gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"

payload = {
    "contents": [{
        "parts": [{
            "text": "Write a high-yield ICU Clinical Pearl for nurses under 100 words with bullet points and hashtags #ICU #CriticalCare #Bexyhub."
        }]
    }]
}

response = requests.post(gemini_url, json=payload)
data = response.json()

# अगर 2.5 पर कोई समस्या हो तो यह अपने आप बैकअप मॉडल चला लेगा
if "candidates" not in data:
    backup_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    response = requests.post(backup_url, json=payload)
    data = response.json()

if "candidates" not in data:
    raise Exception(f"Gemini API Error: {data}")

post_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
print("SUCCESS: AI Content Generated!")

# 2. Telegram Send Message
telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
tg_res = requests.post(telegram_url, json={"chat_id": CHANNEL_ID, "text": post_text})

print(f"Telegram Status: {tg_res.status_code}")
print(f"Telegram Response: {tg_res.text}")

if tg_res.status_code != 200:
    raise Exception(f"Failed to post to Telegram: {tg_res.text}")

print("SUCCESS: Post Published to Telegram Channel!")
