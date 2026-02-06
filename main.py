import os
import random
import requests
from google import genai

# Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Gemini Client (SDK အသစ် version)
client = genai.Client(api_key=GEMINI_API_KEY)

IDEAS = [
    "Your phone isn’t spying on you — but this is worse",
    "Why free apps are secretly more expensive than paid ones",
    "This setting controls your entire phone life",
    "The algorithm doesn’t hate you — it ignores you",
    "Where your deleted photos actually go"
]

def generate_script(topic):
    prompt = f"Write a professional video script for: {topic}. Include Hook, Relatable moment, and call to action. Use simple English."
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
        # Markdown error တက်တတ်လို့ အပိုင်းအစတွေကို ရှင်းဖို့ parse_mode ကို ခဏဖြုတ်ထားပါမယ်
    }
    r = requests.post(url, data=payload)
    return r.ok

# Topic ၃ ခု ရွေးမယ်
selected_topics = random.sample(IDEAS, 3)

for i, topic in enumerate(selected_topics, 1):
    script_content = generate_script(topic)
    final_message = f"🎬 Video Idea {i}\n\nTopic: {topic}\n\n{script_content}"
    
    # Telegram ပို့မယ်
    success = send_telegram(final_message)
    if not success:
        print(f"Failed to send Idea {i}")
