import os
import requests

GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID")

# 1. Gemini API Call (Official v1beta endpoint)
gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"

payload = {
    "contents": [{
        "parts": [{
            "text": "Write a high-yield ICU Clinical Pearl for nurses under 100 words with bullet points and hashtags #ICU #CriticalCare #Bexyhub."
        }]
    }]
}

response = requests.post(gemini_url, json=payload)
data = response.json()

if "candidates" not in data:
    raise Exception(f"Gemini API Error: {data}")

post_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
print("AI Content Generated Successfully!")

# 2. Telegram Send Message
telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
tg_payload = {
    "chat_id": CHANNEL_ID,
    "text": post_text
}

tg_res = requests.post(telegram_url, json=tg_payload)
print(f"Telegram Status: {tg_res.status_code}")
print(f"Telegram Response: {tg_res.text}")

if tg_res.status_code != 200:
    raise Exception(f"Failed to post to Telegram: {tg_res.text}")
