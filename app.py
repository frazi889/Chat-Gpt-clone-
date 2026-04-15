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


def fallback_reply(user_text):
    text = user_text.lower()

    if "hello" in text or "hi" in text or "ဟယ်လို" in text or "မင်္ဂလာပါ" in text:
        return "ဟေး bro 😎 နေကောင်းလား"

    if "sad" in text or "ဝမ်းနည်း" in text or "အလွမ်း" in text:
        return "ဟာ bro 🥺 စိတ်မကောင်းမဖြစ်နဲ့… ငါရှိတယ်"

    if "joke" in text or "ဟာသ" in text or "ရီစရာ" in text:
        return "😂 မင်းအချစ်ရေးက wifi လိုပဲ… connect ဖြစ်ရင်ပျော်၊ မဖြစ်ရင် sad"

    if "ဘာလုပ်" in text or "what are you doing" in text:
        return "မင်း message ပို့လာမလားလို့ စောင့်နေတာ bro 😏"

    return "ဟာ bro 😵 AI credits ကုန်နေလို့ smart reply မပေးနိုင်သေးဘူး" 

def ai_reply(user_text):
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly Myanmar chatbot. "
                        "Speak naturally in Burmese and English mix. "
                        "Be fun, casual, emotional, and conversational. "
                        "Keep replies short like a real chat friend."
                    )
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ],
            max_tokens=150
        )
        return res.choices[0].message.content

    except Exception as e:
        error_text = str(e)
        print("OPENAI_ERROR:", error_text)

        if "insufficient_quota" in error_text or "429" in error_text:
            return fallback_reply(user_text)

        return "ဟာ bro bot brain ခဏ hang သွားတယ် 😵"


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


@app.get("/get_webhook_info")
def get_webhook_info():
    return tg_api("getWebhookInfo", {}) 

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

    # private chat => always reply
    if chat_type == "private":
        reply = ai_reply(text)
        send_message(chat_id, reply, message_id)
        return {"ok": True}

    # group / supergroup => reply only if user replied to bot
    if chat_type in ["group", "supergroup"]:
        reply_msg = message.get("reply_to_message")
        if reply_msg and reply_msg.get("from", {}).get("is_bot"):
            reply = ai_reply(text)
            send_message(chat_id, reply, message_id)
            return {"ok": True}

    return {"ok": True}
