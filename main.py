import os
import random
import requests
import google.generativeai as genai

# Environment Variables
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# Gemini Configuration
genai.configure(api_key=GEMINI_API_KEY)
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
    The script should include:
    - A catchy Title
    - Timestamps (e.g., 0:00-0:10)
    - Hook, Relatable Moment, Big Reveal, and a Sticky Ending.
    - Use simple, engaging English.
    """
    response = model.generate_content(prompt)
    return response.text

# Random Idea တစ်ခုကို ရွေးပြီး Script ရေးခိုင်းမယ်
selected_topic = random.choice(IDEAS)
full_script = generate_script(selected_topic)

# Telegram ကို ပို့မယ့် Message (Title + Script)
message = f"🎬 *Today's Full Script*\n\nTopic: {selected_topic}\n\n{full_script}"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    # Telegram ရဲ့ Character limit 4096 ကျော်ရင် ခွဲပို့ဖို့ လိုအပ်နိုင်ပါတယ်
    # အခြေခံအားဖြင့် အပိုင်းလိုက်ခွဲပို့ခြင်း (Chunking)
    if len(text) > 4000:
        for x in range(0, len(text), 4000):
            payload = {
                "chat_id": CHAT_ID,
                "text": text[x:x+4000],
                "parse_mode": "Markdown"
            }
            requests.post(url, data=payload)
    else:
        payload = {
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        }
        requests.post(url, data=payload)

send_telegram(message)
