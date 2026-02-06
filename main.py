import requests
import random
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

IDEAS = [
    "Your phone isn’t spying on you — but this is worse",
    "Why free apps are secretly more expensive than paid ones",
    "This setting controls your entire phone life",
    "The algorithm doesn’t hate you — it ignores you",
    "Where your deleted photos actually go"
]

selected = random.sample(IDEAS, 3)

message = "📌 *Today's Video Ideas*\n\n"
for i, idea in enumerate(selected, 1):
    message += f"{i}. {idea}\n"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": message,
    "parse_mode": "Markdown"
}

requests.post(url, data=payload)
