import os
import requests
from google import genai

# क्रेडेंशियल्स लेना
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID")

client = genai.Client(api_key=GEMINI_KEY)

# 1. AI से यूनिक क्लिनिकल पोस्ट लिखवाना
prompt = """
Write a high-yield, authentic ICU Clinical Pearl for critical care nurses.
Focus on real bedside practice (e.g., Arterial Line damping, Noradrenaline weaning, or ABG interpretation).
Format:
- 💡 Clinical Tip Title (Bold)
- 🩺 Real Bedside Rationale (Brief & punchy, 3-4 bullet points)
- ⚠️ Red Flag / Never Miss Rule
- #ICUNursing #CriticalCare #ClinicalPearls #Bexyhub
Keep it professional, crisp, and under 150 words.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)
post_text = response.text.strip()

# 2. टेलीग्राम चैनल पर भेजना
telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": CHANNEL_ID,
    "text": post_text,
    "parse_mode": "Markdown"
}

res = requests.post(telegram_url, json=payload)
if res.status_code == 200:
    print("SUCCESS: Post published to Telegram channel!")
else:
    print(f"FAILED: {res.text}")
