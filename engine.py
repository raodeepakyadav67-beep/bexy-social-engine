import os
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "").strip()

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data = {
    "chat_id": CHANNEL_ID,
    "text": "🔥 Bexy Social Engine: Connection Successful! Autonomous system is active."
}

res = requests.post(url, json=data)
print("Response:", res.text)

if res.status_code != 200:
    raise Exception(f"Failed: {res.text}")
