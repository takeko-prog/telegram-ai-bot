import os
import random
import requests
from google import genai

# Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Gemini Client အသစ် (SDK အသစ် version)
client = genai.Client(api_key=GEMINI_API_KEY)

IDEAS = [
    "Your phone isn’t spying on you — but this is worse",
    "Why free apps are secretly more expensive than paid ones",
    "This setting controls your entire phone life",
    "The algorithm doesn’t hate you — it ignores you",
    "Where your deleted photos actually go"
]

def generate_script(topic):
    prompt = f"Write a full video script about: {topic}. Use simple English, include timestamps, hook, and body."
    try:
        # SDK အသစ်မှာ model နာမည်ကို 'gemini-1.5-flash' လို့ပဲ ရေးရပါတယ်
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Script generation failed: {str(e)}"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    r = requests.post(url, data=payload)
    return r.ok

# Topic ၃ ခု ရွေးပြီး Script ထုတ်မယ်
selected_topics = random.sample(IDEAS, 3)

for i, topic in enumerate(selected_topics, 1):
    script_content = generate_script(topic)
    
    # Telegram ပို့မယ့် Message format
    final_message = f"🎬 *Video Idea {i}*\n\n*Topic:* {topic}\n\n{script_content}"
    
    # Message အရမ်းရှည်ရင် (သို့) Markdown error တက်ရင် plain text နဲ့ ပြန်ပို့မယ်
    if not send_telegram(final_message):
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": final_message})
