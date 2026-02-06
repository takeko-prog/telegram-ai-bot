import os
import random
import requests
from google import genai
from google.genai import types

# Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Gemini Client အသစ်
client = genai.Client(api_key=GEMINI_API_KEY)

IDEAS = [
    "Your phone isn’t spying on you — but this is worse",
    "Why free apps are secretly more expensive than paid ones",
    "This setting controls your entire phone life",
    "The algorithm doesn’t hate you — it ignores you",
    "Where your deleted photos actually go"
]

def generate_script(topic):
    prompt = f"Write a full video script about: {topic}. Include Hook, Body, and Outro."
    try:
        # Model နာမည်ကို အတိုပဲ ရေးရပါတယ်
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

# Random ၃ ခုရွေးပြီး ပို့မယ်
selected_topics = random.sample(IDEAS, 3)

for i, topic in enumerate(selected_topics, 1):
    script = generate_script(topic)
    final_text = f"🎬 *Video Idea {i}*\n\nTopic: {topic}\n\n{script}"
    
    if not send_telegram(final_text):
        # Markdown error တက်ရင် plain text နဲ့ ပို့မယ်
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": final_text})
