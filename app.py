import json
import os
import re
from pathlib import Path

import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("BASE_URL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

client = OpenAI(api_key=OPENAI_API_KEY)
app = FastAPI()

MEMORY_FILE = Path("memory.json")

def load_memory():
    if MEMORY_FILE.exists():
        return json.load(open(MEMORY_FILE, "r", encoding="utf-8"))
    return {}

def save_memory(data):
    json.dump(data, open(MEMORY_FILE, "w", encoding="utf-8"), ensure_ascii=False)

user_memory = load_memory()

def telegram_api(method, data):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    return requests.post(url, json=data).json()

def send_message(chat_id, text, reply_id=None):
    payload = {"chat_id": chat_id, "text": text}
    if reply_id:
        payload["reply_to_message_id"] = reply_id
    telegram_api("sendMessage", payload)


def should_reply(message):
    chat_type = message["chat"]["type"]

    if chat_type == "private":
        return True

    if chat_type in ["group", "supergroup"]:
        reply = message.get("reply_to_message")
        if reply and reply["from"].get("is_bot"):
            return True

    return False


def detect_name(user_id, text):
    match = re.search(r"(?:my name is|i am)\s+(.+)", text.lower())
    if match:
        name = match.group(1)
        user_memory[user_id] = name
        save_memory(user_memory)
        return name 

@app.post("/webhook/{secret}")
async def webhook(secret: str, request: Request):
    if secret != WEBHOOK_SECRET:
        return {"ok": False}

    data = await request.json()
    message = data.get("message")

    if not message:
        return {"ok": True}

    chat_id = message["chat"]["id"]
    msg_id = message["message_id"]
    text = message.get("text", "")

    if not text:
        return {"ok": True}

    if not should_reply(message):
        return {"ok": True}

    user_id = str(message["from"]["id"])

    # name save
    name = detect_name(user_id, text)
    if name:
        send_message(chat_id, f"မှတ်ထားပြီ {name} 😎", msg_id)
        return {"ok": True}

    username = user_memory.get(user_id, "bro")

    # AI reply
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a fun Myanmar bot. Speak Burmese + English mix, funny, emotional, teasing."
            },
            {
                "role": "user",
                "content": f"{username}: {text}"
            }
        ]
    )

    reply = response.choices[0].message.content
    send_message(chat_id, reply, msg_id)

    return {"ok": True}


@app.get("/set_webhook")
def set_webhook():
    url = f"{BASE_URL}/webhook/{WEBHOOK_SECRET}"
    return telegram_api("setWebhook", {"url": url}) 
