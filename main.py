import os
import random
import asyncio
import google.generativeai as genai
from telegram import Bot

# Settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Gemini Setup
genai.configure(api_key=GEMINI_API_KEY)

# ဒီနေရာမှာ နာမည်အပြည့်အစုံ ပြောင်းလိုက်ပါ
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash-latest", 
    generation_config={
        "temperature": 1.0,
        "top_p": 0.95,
    }
)

async def generate_script():
    topics = [
        "Digital Privacy", "Phone Spying Myths", "AI Future", 
        "Data Tracking", "Social Media Secrets"
    ]
    topic = random.choice(topics)
    
    prompt = f"Create a viral short video script in Myanmar language about: {topic}. Include Hook, Body, and Reveal."
    
    try:
        # generate_content ကို သေချာခေါ်ထားပါတယ်
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
        print("Success!")
    except Exception as e:
        print(f"Telegram Error: {e}")

if __name__ == "__main__":
    asyncio.run(run_bot())
