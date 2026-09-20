import os
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "").strip()

# सीधा टेलीग्राम टेस्ट
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": CHANNEL_ID,
    "text": "🔥 Bexy Social Engine: Connection Successful! Live test active."
}

res = requests.post(url, json=payload)
print("Telegram Status:", res.status_code)
print("Telegram Response:", res.text)

if res.status_code != 200:
    raise Exception(f"Posting failed: {res.text}")
