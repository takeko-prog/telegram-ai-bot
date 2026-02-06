import os
import random
import requests
import google.generativeai as genai

# Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Gemini Configuration
genai.configure(api_key=GEMINI_API_KEY)

# Model ကို flash သုံးတာ ပိုမြန်ပြီး free ပိုရပါတယ်
model = genai.GenerativeModel('gemini-1.5-flash')

IDEAS = [
    "Your phone isn’t spying on you — but this is worse",
    "Why free apps are secretly more expensive than paid ones",
    "This setting controls your entire phone life",
    "The algorithm doesn’t hate you — it ignores you",
    "Where your deleted photos actually go"
]

def generate_script(topic):
    prompt = f"""
    Write a detailed YouTube/TikTok video script for the topic: "{topic}"
    Format it exactly like this:
    🎬 Video Title: ...
    ⏱️ 0:00–0:10 — Hook: ...
    ⏱️ 0:10–0:40 — Content: ...
    ... (continue with simple English)
    """
    try:
        # safety_settings ကို block_none ထားမှ script တွေက block မခံရမှာပါ
        response = model.generate_content(
            prompt,
            safety_settings={
                "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
            }
        )
        return response.text
    except Exception as e:
        return f"Script generation failed: {str(e)}"

# တစ်ခုချင်းစီအတွက် Script ရေးခိုင်းမယ် (Idea ၃ ခုလုံး)
selected_topics = random.sample(IDEAS, 3)

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    r = requests.post(url, data=payload)
    return r.ok

# စုစုပေါင်း ၃ ခု ပို့ပေးမှာပါ
for i, topic in enumerate(selected_topics, 1):
    script = generate_script(topic)
    final_text = f"📌 *Video Idea {i}*\n\n{script}"
    
    # စာသားအရမ်းရှည်ရင် Markdown Error တက်တတ်လို့ error ဖြစ်ရင် plain text နဲ့ ပြန်ပို့မယ်
    if not send_telegram(final_text):
        payload = {"chat_id": CHAT_ID, "text": final_text}
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data=payload)
