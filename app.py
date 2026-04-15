import os
import requests
from fastapi import FastAPI, Request
from openai import OpenAI

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BASE_URL = os.getenv("BASE_URL", "")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

client = OpenAI(api_key=OPENAI_API_KEY)

# ---------------- Telegram API ----------------
def tg_api(method, data):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    r = requests.post(url, json=data, timeout=30)
    return r.json()

def send_message(chat_id, text, reply_to_message_id=None):
    data = {
        "chat_id": chat_id,
        "text": text
    }
    if reply_to_message_id:
        data["reply_to_message_id"] = reply_to_message_id
    return tg_api("sendMessage", data)

# ---------------- AI Reply ----------------
def ai_reply(user_text):
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a funny Myanmar chatbot. Mix Burmese and English. Be playful and natural."},
                {"role": "user", "content": user_text}
            ]
        )
        return res.choices[0].message.content
    except Exception as e:
        print("AI Error:", e)
        return "ဟာ bro bot brain ခဏ hang သွားတယ် 😵"

# ---------------- Routes ----------------
@app.get("/")
def home():
    return {
        "ok": True,
        "bot_token_set": bool(BOT_TOKEN),
        "base_url": BASE_URL,
        "webhook_secret_set": bool(WEBHOOK_SECRET),
        "openai_key_set": bool(OPENAI_API_KEY)
    }

@app.get("/set_webhook")
def set_webhook():
    webhook_url = f"{BASE_URL}/webhook/{WEBHOOK_SECRET}"
    return tg_api("setWebhook", {"url": webhook_url})

@app.post("/webhook/{secret}")
async def webhook(secret: str, request: Request):
    if secret != WEBHOOK_SECRET:
        return {"ok": False}

    data = await request.json()
    message = data.get("message")

    if not message:
        return {"ok": True}

    chat_id = message["chat"]["id"]
    message_id = message["message_id"]
    text = message.get("text", "")

    if not text:
        send_message(chat_id, "text ပို့ bro 😆", message_id)
        return {"ok": True}

    chat_type = message["chat"]["type"]

    # 🔥 PRIVATE CHAT
    if chat_type == "private":
        reply = ai_reply(text)
        send_message(chat_id, reply, message_id)
        return {"ok": True}

    # 🔥 GROUP CHAT (reply only if user replied to bot)
    if chat_type in ["group", "supergroup"]:
        reply_msg = message.get("reply_to_message")
        if reply_msg and reply_msg.get("from", {}).get("is_bot"):
            reply = ai_reply(text)
            send_message(chat_id, reply, message_id)
            return {"ok": True}

    return {"ok": True}
