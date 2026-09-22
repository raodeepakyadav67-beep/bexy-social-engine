import os
import random
import requests
import pytumblr

# 1. GitHub Secrets से क्रेडेंशियल्स लेना (यहाँ कोई बदलाव नहीं करना है)
CONSUMER_KEY = os.getenv("TUMBLR_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("TUMBLR_CONSUMER_SECRET")
OAUTH_TOKEN = os.getenv("TUMBLR_OAUTH_TOKEN")
OAUTH_SECRET = os.getenv("TUMBLR_OAUTH_SECRET")
BLOG_NAME = os.getenv("TUMBLR_BLOG_NAME", "bexyhub")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 2. क्लीनिकल टॉपिक्स
topics = [
    "Arterial Line Damping and Flush Test Pitfalls in ICU",
    "Noradrenaline vs Vasopressin Titration in Refractory Septic Shock",
    "Post-CABG Sudden Mediastinal Drain Cessation and Cardiac Tamponade",
    "Recognizing Patient-Ventilator Asynchrony: Double Triggering",
    "Neuro ICU: Cerebral Perfusion Pressure (CPP) vs ICP Spike Management",
    "Electrolyte Emergencies: Rapid Potassium Correction and Cardiac Arrhythmias",
    "Post-PCI Radial Artery Hematoma and Bedside Compartment Syndrome Watch",
    "Targeted Temperature Management (TTM) Post-Cardiac Arrest Pearls",
    "High PEEP Hazards: Right Ventricular Strain and Hemodynamic Collapse",
    "Bedside CVP Interpretation: Volume Responsiveness vs Fluid Overload"
]

topic = random.choice(topics)

prompt = (
    f"You are an expert ICU clinician. Write a concise bedside clinical pearl on: {topic}.\n"
    "Structure:\n"
    "1. Bedside observation vs theory.\n"
    "2. Critical drug/titration error to avoid.\n"
    "3. Immediate nursing intervention.\n"
    "4. Golden Rule.\n"
    "Rules: Plain text, exactly 4-5 sentences, punchy clinical style, under 100 words."
)

# 3. Gemini API Request (स्टेबल कोटा मॉडल)
gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent"
headers = {
    "Content-Type": "application/json; charset=utf-8",
    "x-goog-api-key": GEMINI_API_KEY
}
payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 800}
}

res = requests.post(gemini_url, json=payload, headers=headers)
res_data = res.json()

if "error" in res_data:
    print("Gemini API Error Detail:", res_data["error"]["message"])
    exit(1)

content = res_data["candidates"][0]["content"]["parts"][0]["text"].replace("*", "").replace("#", "").strip()

title = f"ICU Clinical Pearl: {topic}"
body = f"{content}\n\n— Deepak Kumar | ICU Specialist"

# 4. Tumblr पर पोस्ट पब्लिश करना
client = pytumblr.TumblrRestClient(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    OAUTH_TOKEN,
    OAUTH_SECRET
)

try:
    response = client.create_text(
        BLOG_NAME,
        state="published",
        title=title,
        body=body,
        tags=["ICU", "CriticalCare", "Nursing", "ClinicalPearls", "Bexyhub"]
    )
    print("Tumblr Response:", response)
    if "id" in response:
        print("Tumblr Post Sent Successfully!")
except Exception as e:
    print(f"Tumblr Error: {e}")
