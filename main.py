import os
import random
import asyncio
import google.generativeai as genai
from telegram import Bot

# Settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Gemini Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    generation_config={
        "temperature": 1.0, # အရမ်းကွဲပြားတဲ့ idea တွေရဖို့ ၁.၀ ထားပါ
        "top_p": 0.95,
    }
)

async def generate_script():
    # Content မထပ်အောင် Topic တွေကို ပိုစုံအောင် ထည့်ထားပေးပါ
    topics = [
        "Digital Privacy Secrets", "Smart Phone Myths", "AI Future", 
        "Data Tracking", "Social Media Algorithms", "Cyber Security"
    ]
    topic = random.choice(topics)
    
    prompt = f"""
    Create a high-quality video script in Myanmar language about: {topic}.
    Follow the professional structure:
    - Dramatic Hook
    - Relatable scenarios
    - Deep insight/The reveal
    - Call to action
    Use engaging tone and detailed visual descriptions.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini API Error: {str(e)}"

async def run_bot():
    script_content = await generate_script()
    bot = Bot(token=BOT_TOKEN)
    
    # Telegram message length limit (4096 chars) ကို မကျော်အောင် လိုအပ်ရင် ဖြတ်ပါ
    msg = f"🎬 **Daily Content Idea**\n\n{script_content}"
    
    await bot.send_message(chat_id=CHAT_ID, text=msg[:4000], parse_mode="Markdown")
    print("Sent to Telegram successfully!")

if __name__ == "__main__":
    asyncio.run(run_bot())
