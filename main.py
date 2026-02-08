import os
import random
import asyncio
import google.generativeai as genai
from telegram import Bot

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Gemini Setup - နာမည်ကို ရိုးရိုးပဲ ထားပါ
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

async def generate_script():
    topics = ["Digital Privacy", "AI Secrets", "Phone Security", "Social Media Hacks"]
    topic = random.choice(topics)
    
    prompt = f"Create a viral short video script in Myanmar language about: {topic}. Must include a Hook, Body, and a Mind-blowing Reveal."
    
    try:
        # SDK က version တွေကို သူ့ဘာသာ ကိုင်တွယ်သွားပါလိမ့်မယ်
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini API Error: {str(e)}"

async def run_bot():
    script_content = await generate_script()
    bot = Bot(token=BOT_TOKEN)
    
    msg = f"🎬 **Daily Content Idea**\n\n{script_content}"
    
    try:
        await bot.send_message(chat_id=CHAT_ID, text=msg[:4000], parse_mode="Markdown")
        print("Done! Message sent to Telegram.")
    except Exception as e:
        print(f"Telegram Error: {e}")

if __name__ == "__main__":
    asyncio.run(run_bot())
