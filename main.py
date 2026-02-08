import os
import random
import asyncio
import google.generativeai as genai
from telegram import Bot

# Settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN") # နာမည် ပြောင်းလိုက်ပြီ
CHAT_ID = os.getenv("CHAT_ID")

# Gemini Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    generation_config={
        "temperature": 1.0, 
        "top_p": 0.95,
    }
)

async def generate_script():
    topics = [
        "Digital Privacy Secrets", "Smart Phone Myths", "AI Future", 
        "Data Tracking", "Social Media Algorithms", "Cyber Security"
    ]
    topic = random.choice(topics)
    
    prompt = f"Create a high-quality video script in Myanmar language about: {topic}. Detailed visual descriptions and engaging tone are required."
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini API Error: {str(e)}"

async def run_bot():
    script_content = await generate_script()
    bot = Bot(token=BOT_TOKEN) # ဒီမှာလည်း BOT_TOKEN သုံးထားပါတယ်
    
    msg = f"🎬 **Daily Content Idea**\n\n{script_content}"
    
    await bot.send_message(chat_id=CHAT_ID, text=msg[:4000], parse_mode="Markdown")
    print("Sent to Telegram successfully!")

if __name__ == "__main__":
    asyncio.run(run_bot())
