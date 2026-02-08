import os
import random
import asyncio
import google.generativeai as genai
from telegram import Bot

# Setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def run_bot():
    try:
        # Model ကို ဒီလိုလေးပဲ ခေါ်ကြည့်ပါ
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Content ထပ်မနေအောင် random topic ထည့်ပါ
        topic = random.choice(["Privacy", "AI Future", "Tech Myths"])
        prompt = f"Create a short video script in Myanmar about {topic}."

        # Response တောင်းခြင်း
        response = model.generate_content(prompt)
        content = response.text

        # Telegram ပို့ခြင်း
        bot = Bot(token=os.getenv("BOT_TOKEN"))
        await bot.send_message(chat_id=os.getenv("CHAT_ID"), text=content)
        print("Success!")

    except Exception as e:
        # ဘယ်နေရာမှာ Error တက်လဲဆိုတာ ပိုသိသာအောင် debug လုပ်မယ်
        print(f"Debug Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_bot())
