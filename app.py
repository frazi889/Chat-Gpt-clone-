import os
import requests
from fastapi import FastAPI, Request

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")


def send_message(chat_id, text, reply_id=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    if reply_id:
        data["reply_to_message_id"] = reply_id
    requests.post(url, json=data)


# ✅ Home test
@app.get("/")
def home():
    return {"ok": True}


# ✅ Set webhook
@app.get("/set_webhook")
def set_webhook():
    url = f"{BASE_URL}/webhook/{WEBHOOK_SECRET}"
    res = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
        json={"url": url},
    )
    return res.json()


# ✅ Webhook
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

    # 🔥 reply-only logic
    chat_type = message["chat"]["type"]

    if chat_type in ["group", "supergroup"]:
        reply = message.get("reply_to_message")
        if not reply or not reply["from"].get("is_bot"):
            return {"ok": True}

    # ✅ TEST reply
    send_message(chat_id, f"rp ok: {text}", msg_id)

    return {"ok": True}
