import os
import random
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
        "text": text[:4000]
    }
    if reply_to_message_id:
        data["reply_to_message_id"] = reply_to_message_id
    return tg_api("sendMessage", data)


def normalize_text(text):
    return (text or "").strip().lower()


def contains_any(text, words):
    return any(word in text for word in words)


greetings = [
    "ဟေး bro 😎 နေကောင်းလား",
    "yo bro 😏 ဘာလုပ်နေလဲ",
    "မင်္ဂလာပါ bro 😄",
    "ဟေ့ 😎 finally ပေါ်လာပြီလား",
    "hi bro 👀 ငါစောင့်နေတာ"
]

how_are_you_replies = [
    "နေကောင်းတယ် bro 😎 မင်းရော",
    "အေးပြေတယ် bro 😌 မင်းကော",
    "မဆိုးဘူး bro… မင်း message ပို့လို့ပိုကောင်းသွားတယ် 😏",
    "chill ပဲ bro 😎 မင်းနေကောင်းလား"
]

jokes = [
    "😂 မင်းအချစ်ရေးက wifi လိုပဲ… connect ဖြစ်ရင်ပျော်၊ မဖြစ်ရင် sad",
    "🤣 မင်း life က charger မရှိတဲ့ phone လိုပဲ… low battery bro",
    "😆 အချစ်ရေးမအောင်မြင်ရင် tea သောက် bro… tea ကတော့ မပစ်သွားဘူး",
    "😂 crush က reply မပေးရင် airplane mode ချလိုက် bro… pain လျော့တယ်",
    "🤣 မင်းအိပ်ချင်တာနဲ့ success ရချင်တာ fight ဖြစ်နေတာ bro"
]

random_replies = [
    "ဟုတ်တယ် bro 😎",
    "အဲ့လိုလား 😏",
    "အေးကွာ… interesting ပဲ",
    "bro မင်းစကားက vibe ရှိတယ် 😆",
    "ဟာ အဲ့တာကတော့ true တယ်",
    "ငါနားထောင်နေတယ် bro 👀",
    "ဆက်ပြော bro 😎",
    "အဲ့ဒီလိုဆို story က မိုက်နေပြီ",
    "bro ဒီစကားက heavy တယ်နော်",
    "မင်းပြောတာက logic ရှိတယ် 😌",
    "ဟာကွာ ဒီ topic ကမိုက်တယ်",
    "အဲ့လိုဆို next ဘာဖြစ်သေးလဲ 👀"
] 
love_replies = [
    "အူးဟူး 😏 ဘယ်သူ့ကိုလွမ်းနေတာလဲ bro",
    "bro… crush ရှိရင်တန်းပြော 😆",
    "ဟာ 🥺 ဒီစကားက heart ထိတယ် bro",
    "ချစ်ရတာလွယ်ပေမယ့် forget လုပ်ရတာ hard mode bro 😮‍💨",
    "မင်းကတော့ love story main character ပဲ 😏",
    "ဟာ bro ဒီ mood က romance drama ကြီးပဲ",
    "ဘယ်သူ့ကြောင့် heart soft ဖြစ်နေတာလဲ 😏"
]

sad_replies = [
    "ဟာ bro 🥺 စိတ်မကောင်းမဖြစ်နဲ့… ငါရှိတယ်",
    "အို bro 😔 ဘာဖြစ်လဲ ပြောပါဦး",
    "အေးကွာ… တခါတလေ life က heavy ဖြစ်တတ်တယ် bro",
    "လေးနက်နေလား bro… breathe လေး first 😔",
    "မင်းကို နားထောင်ပေးမယ့်သူလိုရင် ငါရှိတယ်",
    "pain တွေကို တစ်ယောက်တည်းမခံနဲ့ bro",
    "အဲ့လိုနေ့တွေမှာ quiet ဖြစ်ချင်တာ normal ပဲ bro"
]

friend_replies = [
    "bro mode on 😎",
    "ဟုတ်တယ် သူငယ်ချင်း vibe နဲ့ပြော bro",
    "ငါကတော့ bro side ပဲ 😌",
    "friend zone မဟုတ်ဘူး bro zone 😆",
    "ဟေ့ bro chill… ငါရှိတယ်",
    "မင်းဘက်ကနေ support လုပ်ပေးမယ် bro",
    "bro to bro ပြောရရင် မင်းမဆိုးဘူး"
]

angry_replies = [
    "ဟာ bro 😤 မင်း mood က spicy နော်",
    "အေးကွာ စိတ်တိုနေရင် slowly ပြော bro",
    "bro rage mode ဝင်နေပြီလား 😤",
    "ဟာ… fight mode on လား 😏",
    "မင်းစိတ်တိုနေတာကိုတောင် style ရှိနေတယ် bro",
    "အေးပါ bro ဒေါသမကြီးနဲ့… but continue 😆"
]

roast_replies = [
    "ဟာ bro 😏 မင်းကတော့ reply လုပ်မှအသက်ဝင်လာတဲ့ hero ပဲ",
    "😆 မင်းပြောတာလေးက confidence ပြည့်နေတာပဲ bro",
    "ဟေ့ 😏 spicy လေးပြောနေတာလား bro",
    "bro မင်းက clap မပေးရင်တောင် self-hype ပေးနိုင်တဲ့ type 😆",
    "မင်း attitude က VIP queue လိုပဲ bro… straight front 😏",
    "မင်းကိုကြည့်ရင် drama နဲ့ comedy mix တူတယ် bro 😂",
    "ဟာ မင်းကတော့ walking sarcasm ပဲ"
]

swear_soft_replies = [
    "ဟာ bro 😅 စကားကြမ်းသွားပြီနော်",
    "ဆဲလို့ရတယ် bro… but chill လေး 😏",
    "မင်း mood က rough ဖြစ်နေတာပဲ bro",
    "ဟာကွာ မင်းကတော့ fire ပဲ 😆",
    "အေးပါ bro… language က spicy ဖြစ်နေပြီ",
    "မင်းဆဲတာတောင် rhythm ရှိတယ် bro 😂"
] 

jealous_replies = [
    "ဟာ bro jealous ဖြစ်နေတာလား 😏",
    "မနာလိုနေတာလား bro… honest ဖြစ်နေတာပဲ",
    "bro မင်း tone ထဲမှာ jealous flavor နည်းနည်းပါနော် 😂",
    "အူးဟူး jealous mode ဝင်ပြီလား",
    "မင်းက care လွန်းလို့ jealous ဖြစ်နေတာပဲ bro"
]

lonely_replies = [
    "lonely feel ဖြစ်နေလား bro 🥺",
    "တစ်ယောက်တည်း feel ဖြစ်တဲ့ညတွေက heavy တယ်နော်",
    "bro တစ်ခါတလေ company လိုတာ normal ပဲ",
    "ငါနဲ့ပြော bro… silent မနေပါနဲ့",
    "အေးကွာ lonely mood ကစိတ်ကိုဆွဲချတတ်တယ်"
]

flirty_replies = [
    "ဟာ bro 😏 ဒီ tone က flirting နည်းနည်းပါနေတယ်",
    "အူးဟူး မင်းစကားက smooth နော် 😆",
    "ဒီလိုပြောရင် heart ထိတယ် bro 😏",
    "မင်းကတော့ charm ကို casual သုံးတာပဲ",
    "bro ဒီ vibe နဲ့ဆို crush ပေါ်နိုင်တယ် 😌"
]

sleep_replies = [
    "အိပ်တော့ bro 😴 body က rest လိုတယ်",
    "bro late night overthinking မလုပ်နဲ့ အိပ်လိုက်",
    "sleep first bro… tomorrow version က better ဖြစ်မယ်",
    "ဖုန်းချ bro 😴 မနက်ကျ ပြန်ပြော",
    "အိပ်ရေးမဝရင် mood တောင် toxic ဖြစ်တတ်တယ် bro"
]

food_replies = [
    "ဘာစားထားလဲ bro 🍜",
    "ဗိုက်ဆာနေရင် first eat bro",
    "life problems တစ်ဝက်က food နဲ့ solve လို့ရတယ် bro 😆",
    "မစားရသေးရင် စားလိုက် bro 🍚",
    "tea + snack = emotional support combo bro"
]

motivation_replies = [
    "မင်းထင်တာထက် မင်းပို strong တယ် bro 💪",
    "slow ပေမယ့် stop မလုပ်နဲ့ bro",
    "တစ်နေ့တည်းနဲ့မအောင်မြင်ရင်လည်း okay ပဲ",
    "မင်း pace နဲ့သွား bro… comparison မလုပ်နဲ့",
    "တစ်လှမ်းချင်းသွား bro, still progress ပဲ"
]

confused_replies = [
    "ဟာ bro ဒီ topic ကနည်းနည်းရှုပ်တယ် 😂",
    "slowly ပြော bro… ငါလိုက်မမီသေးဘူး",
    "တစ်ချက်ပြန်ရှင်း bro 👀",
    "အဲဒီလိုဆို context လေးထပ်ပေး bro",
    "bro plot twist များနေပြီ 😆"
] 

def get_reply(user_text):
    text = normalize_text(user_text)

    if text in ["/start", "start"]:
        return (
            "ဟေး bro 😎\n"
            "ငါက free human-style fallback bot ပဲ\n"
            "DM မှာ ဘာပြောပြောပြန်မယ်\n"
            "Group ထဲမှာတော့ ငါ့ message ကို reply လုပ်မှပြန်မယ် 😏\n"
            "ဟာသ / အလွမ်း / love / spicy chat / casual talk အကုန်ရတယ်"
        )

    if contains_any(text, ["hello", "hi", "hey", "မင်္ဂလာပါ", "ဟယ်လို"]):
        return random.choice(greetings)

    if contains_any(text, ["နေကောင်း", "how are you", "how r u"]):
        return random.choice(how_are_you_replies)

    if contains_any(text, ["joke", "ဟာသ", "ရီစရာ", "ဟာသပြော"]):
        return random.choice(jokes)

    if contains_any(text, ["sad", "ဝမ်းနည်း", "အလွမ်း", "လွမ်း", "pain", "heartbroken"]):
        return random.choice(sad_replies)

    if contains_any(text, ["friend", "သူငယ်ချင်း", "bro", "bestie"]):
        return random.choice(friend_replies)

    if contains_any(text, ["angry", "စိတ်တို", "ဒေါသ", "fight", "ရန်"]):
        return random.choice(angry_replies)

    if contains_any(text, ["roast", "စနောက်", "ပြောင်", "mock"]):
        return random.choice(roast_replies)

    if contains_any(text, ["ချစ်", "love", "crush", "kiss", "romance"]):
        return random.choice(love_replies)

    if contains_any(text, ["jealous", "မနာလို", "သဝန်တို"]):
        return random.choice(jealous_replies)

    if contains_any(text, ["lonely", "တစ်ယောက်တည်း", "alone", "single"]):
        return random.choice(lonely_replies)

    if contains_any(text, ["flirt", "cute", "ချော", "လှ", "sweet"]):
        return random.choice(flirty_replies) 

if contains_any(text, ["sleep", "အိပ်", "ည", "good night", "gn"]):
        return random.choice(sleep_replies)

    if contains_any(text, ["စား", "food", "ဗိုက်ဆာ", "hungry", "ထမင်း"]):
        return random.choice(food_replies)

    if contains_any(text, ["motivate", "အားပေး", "ကြိုးစား", "success", "goal"]):
        return random.choice(motivation_replies)

    if contains_any(text, ["confuse", "ရှုပ်", "နားမလည်", "ဘာဆိုလို"]):
        return random.choice(confused_replies)

    if contains_any(text, ["ဘာလုပ်", "what are you doing", "doing"]):
        return "မင်း message ပို့လာမလားလို့ စောင့်နေတာ bro 😏"

    if contains_any(text, ["မင်းဘယ်သူ", "who are you"]):
        return "ငါလား 😎 free fallback bot bro… but vibe ကတော့ human style"

    if contains_any(text, ["thank", "ကျေးဇူး", "thx"]):
        return "ရပါတယ် bro 😄"

    if contains_any(text, ["bye", "တာ့တာ", "see you", "goodbye"]):
        return "တာ့တာ bro 👋 နောက်မှပြန်လာခဲ့"

    if contains_any(text, ["fuck", "shit", "damn", "ဆဲ", "fuck you", "wtf"]):
        return random.choice(swear_soft_replies)

    if text.endswith("?"):
        return random.choice([
            "ဟာ bro မေးခွန်းကြီးလာပြီ 👀",
            "အဲ့ဒါကတော့ interesting question ပဲ bro",
            "ဖြေလို့ရတယ် bro… context လေးထပ်ပေး 😏",
            "bro ဒီမေးခွန်းက deep တယ်နော်"
        ])

    if len(text) <= 3:
        return random.choice([
            "ဟင် bro 👀",
            "ဘာလဲ 😏",
            "အဲ့လောက်ပဲလား bro 😂",
            "ဆက်ပြော bro"
        ])

    return random.choice(random_replies)


@app.get("/")
def home():
    return {
        "ok": True,
        "bot_token_set": bool(BOT_TOKEN),
        "base_url": BASE_URL,
        "webhook_secret_set": bool(WEBHOOK_SECRET),
        "mode": "free_human_style_fallback"
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
        reply = get_reply(text)
        send_message(chat_id, reply, message_id)
        return {"ok": True}

    # group / supergroup => reply only if user replied to bot
    if chat_type in ["group", "supergroup"]:
        reply_msg = message.get("reply_to_message")
        if reply_msg and reply_msg.get("from", {}).get("is_bot"):
            reply = get_reply(text)
            send_message(chat_id, reply, message_id)
            return {"ok": True}

    return {"ok": True} 

