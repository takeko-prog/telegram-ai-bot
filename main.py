import os
import random
import asyncio
import google.generativeai as genai
from telegram import Bot

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Gemini Setup
genai.configure(api_key=GEMINI_API_KEY)

# Model နာမည်ကို ဒီလိုလေးပဲ ရေးလိုက်ပါ
model = genai.GenerativeModel('gemini-1.5-flash')

async def generate_script():
    topics = [
        "Digital Privacy", "AI Secrets", "Phone Security", 
        "Data Tracking", "Algorithm Secrets"
    ]
    topic = random.choice(topics)
    
    prompt = f"Create a short viral video script in Myanmar language about: {topic}. Include Hook, Body, and Reveal."
    
    try:
        # SDK က version တွေကို သူ့ဘာသာ အကောင်းဆုံး ချိန်ညှိသွားပါလိမ့်မယ်
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini Error: {str(e)}"

async def run_bot():
    script_content = await generate_script()
    bot = Bot(token=BOT_TOKEN)
    
    msg = f"🎬 **Daily Content Idea**\n\n{script_content}"
    
    try:
        await bot.send_message(chat_id=CHAT_ID, text=msg[:4000], parse_mode="Markdown")
        print("Success: Sent to Telegram")
    except Exception as e:
        print(f"Telegram Error: {e}")

if __name__ == "__main__":
    asyncio.run(run_bot())
