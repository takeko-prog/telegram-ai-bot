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

# Model နာမည်ကို အတိအကျ ပြန်ပြင်ထားပါတယ်
model = genai.GenerativeModel('gemini-1.5-flash')

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
        # Generation config ထည့်ခြင်းဖြင့် ပိုသေချာစေပါတယ်
        response = model.generate_content(prompt)
        if response.text:
            return response.text
        else:
            return "AI returned an empty response."
    except Exception as e:
        return f"Script generation failed: {str(e)}"

# Random ၃ ခုရွေးမယ်
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

for i, topic in enumerate(selected_topics, 1):
    script = generate_script(topic)
    final_text = f"🎬 *Video Idea {i}*\n\nTopic: {topic}\n\n{script}"
    
    # Message ရှည်လွန်းရင် (သို့) Markdown error တက်ရင် plain text နဲ့ ပြန်ပို့မယ်
    if not send_telegram(final_text):
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": final_text})
