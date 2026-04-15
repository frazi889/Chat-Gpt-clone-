import os
import requests
from fastapi import FastAPI, Request

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BASE_URL = os.getenv("BASE_URL", "")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")

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

@app.get("/")
def home():
    return {
        "ok": True,
        "bot_token_set": bool(BOT_TOKEN),
        "base_url": BASE_URL,
        "webhook_secret_set": bool(WEBHOOK_SECRET)
    }

@app.get("/set_webhook")
def set_webhook():
    webhook_url = f"{BASE_URL}/webhook/{WEBHOOK_SECRET}"
    return tg_api("setWebhook", {"url": webhook_url})

@app.get("/get_webhook_info")
def get_webhook_info():
    return tg_api("getWebhookInfo", {})

@app.get("/delete_webhook")
def delete_webhook():
    return tg_api("deleteWebhook", {})

@app.post("/webhook/{secret}")
async def webhook(secret: str, request: Request):
    print("=== WEBHOOK HIT ===")

    if secret != WEBHOOK_SECRET:
        print("bad secret")
        return {"ok": False, "error": "bad secret"}

    data = await request.json()
    print("update:", data)

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

    # private chat => always reply
    if chat_type == "private":
       reply = ai_reply(text)
send_message(chat_id, reply, message_id)
        return {"ok": True}

    # group / supergroup => reply only if user replied to bot
    if chat_type in ["group", "supergroup"]:
        reply = message.get("reply_to_message")
        if reply and reply.get("from", {}).get("is_bot"):
            send_message(chat_id, f"ok reply: {text}", message_id)

    return {"ok": True}
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ai_reply(user_text):
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a funny Myanmar chatbot. Mix Burmese and English. Be playful, emotional, sometimes teasing."},
                {"role": "user", "content": user_text}
            ]
        )
        return res.choices[0].message.content
    except:
        return "😆 စကားမပြောနိုင်ဘူး bro"
