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
    response = requests.post(url, json=data, timeout=30)
    return response.json()


def send_message(chat_id, text, reply_to_message_id=None):
    data = {
        "chat_id": chat_id,
        "text": str(text)[:4000]
    }
    if reply_to_message_id:
        data["reply_to_message_id"] = reply_to_message_id
    return tg_api("sendMessage", data)


def normalize_text(text):
    return (text or "").strip().lower()


def contains_any(text, words):
    return any(word in text for word in words)


INTRO_REPLIES = [
    "ဟေး bro 😎 ငါဒီမှာရှိတယ်",
    "yo bro 👀 ဘာ mood နဲ့လာတာလဲ",
    "မင်္ဂလာပါ bro 😄 စကားပြောရအောင်",
    "finally ပေါ်လာပြီလား bro 😏",
]

GREETING_REPLIES = [
    "ဟေး bro 😎 နေကောင်းလား",
    "hi bro 👋 ဒီနေ့ဘာ vibe လဲ",
    "yo bro 😏 ဘာလုပ်နေလဲ",
    "မင်္ဂလာပါ bro 😄",
    "ဟယ်လို bro 👀"
]

HOW_ARE_YOU_REPLIES = [
    "နေကောင်းတယ် bro 😎 မင်းရော",
    "အေးပြေတယ် bro 😌 မင်းဘက်ကော",
    "မဆိုးဘူး bro… မင်း message ပို့လို့ mood ကောင်းသွားတယ် 😏",
    "chill ပဲ bro 😎 မင်းနေကောင်းလား"
]

JOKE_REPLIES = [
    "😂 မင်းအချစ်ရေးက wifi လိုပဲ… connect ဖြစ်ရင်ပျော်၊ မဖြစ်ရင် sad",
    "🤣 မင်း life က charger မရှိတဲ့ phone လိုပဲ… low battery bro",
    "😆 crush က reply မပေးရင် airplane mode ချလိုက် bro",
    "😂 မင်းစိတ်ကူးနဲ့ reality က enemy တွေလိုဖြစ်နေတယ် bro",
    "🤣 အောင်မြင်ချင်တာနဲ့ အိပ်ချင်တာက မင်းထဲမှာ daily fight လုပ်နေတယ်"
] 

LOVE_REPLIES = [
    "အူးဟူး 😏 ဘယ်သူ့ကိုလွမ်းနေတာလဲ bro",
    "bro… crush ရှိရင်တန်းပြော 😆",
    "ဟာ 🥺 ဒီစကားက heart ထိတယ် bro",
    "ချစ်ရတာ easy ထင်ရပေမယ့် forget လုပ်ရတာ hard mode bro 😮‍💨",
    "မင်း tone က romance drama main character လေးလိုပဲ 😏",
    "love vibe ဝင်နေပြီ bro 👀"
]

MISS_REPLIES = [
    "လွမ်းနေတာလား bro 🥺",
    "အဲ့လို mood တွေကညဘက်ဆိုပိုဆိုးတတ်တယ်နော်",
    "မတွေ့ရတဲ့လူကိုပိုလွမ်းရတာ life ပဲ bro",
    "လွမ်းနေတယ်ဆိုရင် song ဖွင့်ပြီး feel ခံလိုက် bro 😔",
    "မပြောဖြစ်တဲ့စကားတွေရှိနေတာလား bro"
]

SAD_REPLIES = [
    "ဟာ bro 🥺 စိတ်မကောင်းမဖြစ်နဲ့… ငါရှိတယ်",
    "အို bro 😔 ဘာဖြစ်လဲ ပြောပါဦး",
    "တခါတလေ life က heavy ဖြစ်တတ်တယ် bro",
    "မင်း pain ကို joke နဲ့ဖုံးနေတာလား bro 🥲",
    "bro breathe လေးယူ… everything will pass"
]

FRIEND_REPLIES = [
    "bro mode on 😎",
    "ဟုတ်တယ် သူငယ်ချင်း vibe နဲ့ပြော bro",
    "ငါကတော့ bro side ပဲ 😌",
    "friend zone မဟုတ်ဘူး bro zone 😆",
    "ဟေ့ bro chill… ငါရှိတယ်",
    "မင်းဘက်ကနေ support လုပ်ပေးမယ် bro"
]

ANGRY_REPLIES = [
    "ဟာ bro 😤 mood က spicy နော်",
    "အေးကွာ စိတ်တိုနေရင် slowly ပြော bro",
    "rage mode ဝင်နေပြီလား bro 😤",
    "fight mode on လား 😏",
    "ဒေါသကို tea နဲ့ dilute လုပ်လိုက် bro 😂",
    "မင်းစိတ်တိုနေတာတောင် style ရှိနေတယ် bro"
]

ROAST_REPLIES = [
    "ဟာ bro 😏 မင်းကတော့ reply လုပ်မှအသက်ဝင်လာတဲ့ hero ပဲ",
    "မင်း confidence က free unlimited package လား bro 😆",
    "ဟေ့ spicy လေးပြောနေတာလား bro",
    "မင်း vibe က drama နဲ့ comedy mix ပဲ bro 😂",
    "မင်းကတော့ walking sarcasm ပဲ 😏",
    "အဲ့လိုပြောတာတောင် cute side နည်းနည်းပါသေးတယ် bro"
] 

SWEAR_SOFT_REPLIES = [
    "ဟာ bro 😅 စကားကြမ်းသွားပြီနော်",
    "ဆဲလို့ရတယ် bro… but chill လေး 😏",
    "မင်း mood က rough ဖြစ်နေတာပဲ bro",
    "အေးပါ bro language က spicy ဖြစ်နေပြီ 😂",
    "မင်းဆဲတာတောင် rhythm ရှိတယ် bro",
    "ဟာကွာ fire mode ဝင်နေပြီ 😆"
]

JEALOUS_REPLIES = [
    "ဟာ bro jealous ဖြစ်နေတာလား 😏",
    "မနာလိုနေတာလား bro… honest ဖြစ်နေတာပဲ",
    "jealous flavor နည်းနည်းပါနေတယ်နော် 😂",
    "အူးဟူး သဝန်တို mood ဝင်ပြီလား bro",
    "care လွန်းလို့ jealous ဖြစ်နေတာပဲ bro"
]

LONELY_REPLIES = [
    "lonely feel ဖြစ်နေလား bro 🥺",
    "တစ်ယောက်တည်း feel ဖြစ်တဲ့ညတွေက heavy တယ်နော်",
    "company လိုတာ normal ပဲ bro",
    "ငါနဲ့ပြော bro… silent မနေပါနဲ့",
    "lonely mood ကစိတ်ကိုဆွဲချတတ်တယ် bro"
]

FLIRTY_REPLIES = [
    "ဟာ bro 😏 ဒီ tone က flirting နည်းနည်းပါနေတယ်",
    "အူးဟူး မင်းစကားက smooth နော် 😆",
    "ဒီလိုပြောရင် heart ထိတယ် bro 😏",
    "မင်းကတော့ charm ကို casual သုံးတာပဲ",
    "ဒီ vibe နဲ့ဆို crush ပေါ်နိုင်တယ် bro"
]

SLEEP_REPLIES = [
    "အိပ်တော့ bro 😴 body က rest လိုတယ်",
    "late night overthinking မလုပ်နဲ့ bro",
    "sleep first bro… tomorrow version က better ဖြစ်မယ်",
    "ဖုန်းချ bro 😴 မနက်ကျ ပြန်ပြော",
    "အိပ်ရေးမဝရင် mood တောင် toxic ဖြစ်တတ်တယ် bro"
]

FOOD_REPLIES = [
    "ဘာစားထားလဲ bro 🍜",
    "ဗိုက်ဆာနေရင် first eat bro",
    "life problems တစ်ဝက်က food နဲ့ solve လို့ရတယ် bro 😆",
    "မစားရသေးရင် စားလိုက် bro 🍚",
    "tea + snack = emotional support combo bro"
]

MOTIVATION_REPLIES = [
    "မင်းထင်တာထက် မင်းပို strong တယ် bro 💪",
    "slow ပေမယ့် stop မလုပ်နဲ့ bro",
    "တစ်နေ့တည်းနဲ့မအောင်မြင်ရင်လည်း okay ပဲ",
    "မင်း pace နဲ့သွား bro… comparison မလုပ်နဲ့",
    "တစ်လှမ်းချင်းသွား bro, still progress ပဲ"
]

CONFUSED_REPLIES = [
    "ဟာ bro ဒီ topic ကနည်းနည်းရှုပ်တယ် 😂",
    "slowly ပြော bro… ငါလိုက်မမီသေးဘူး",
    "တစ်ချက်ပြန်ရှင်း bro 👀",
    "context လေးထပ်ပေး bro",
    "plot twist များနေပြီ 😆"
]

RANDOM_REPLIES = [
    "ဟုတ်တယ် bro 😎",
    "အဲ့လိုလား 😏",
    "အေးကွာ… interesting ပဲ",
    "bro မင်းစကားက vibe ရှိတယ် 😆",
    "ဟာ အဲ့တာကတော့ true တယ်",
    "ငါနားထောင်နေတယ် bro 👀",
    "ဆက်ပြော bro 😎",
    "အဲ့ဒီလိုဆို story က မိုက်နေပြီ",
    "ဒီစကားက heavy တယ်နော် bro",
    "မင်းပြောတာက logic ရှိတယ် 😌",
    "ဟာကွာ ဒီ topic ကမိုက်တယ်",
    "next ဘာဖြစ်သေးလဲ bro 👀"
] 

QUESTION_REPLIES = [
    "ဟာ bro မေးခွန်းကြီးလာပြီ 👀",
    "အဲ့ဒါကတော့ interesting question ပဲ bro",
    "ဖြေလို့ရတယ် bro… context လေးထပ်ပေး 😏",
    "ဒီမေးခွန်းက deep တယ်နော် bro"
]

SHORT_REPLIES = [
    "ဟင် bro 👀",
    "ဘာလဲ 😏",
    "အဲ့လောက်ပဲလား bro 😂",
    "ဆက်ပြော bro",
    "ဟာ short message killer ပဲ 😆"
]


def get_reply(user_text):
    text = normalize_text(user_text)

    if text in ["/start", "start"]:
        return (
            "ဟေး bro 😎\n"
            "ငါက human-style fallback bot ပဲ\n"
            "DM မှာ ဘာပြောပြောပြန်မယ်\n"
            "Group ထဲမှာတော့ ငါ့ message ကို reply လုပ်မှပြန်မယ် 😏\n"
            "love / miss / angry / joke / daily chat အကုန်ရတယ်"
        )

    if contains_any(text, ["hello", "hi", "hey", "မင်္ဂလာပါ", "ဟယ်လို"]):
        return random.choice(GREETING_REPLIES)

    if contains_any(text, ["နေကောင်း", "how are you", "how r u"]):
        return random.choice(HOW_ARE_YOU_REPLIES)

    if contains_any(text, ["joke", "ဟာသ", "ရီစရာ", "ဟာသပြော"]):
        return random.choice(JOKE_REPLIES)

    if contains_any(text, ["sad", "ဝမ်းနည်း", "စိတ်မကောင်း", "pain", "broken"]):
        return random.choice(SAD_REPLIES)

    if contains_any(text, ["လွမ်း", "အလွမ်း", "miss", "missing"]):
        return random.choice(MISS_REPLIES)

    if contains_any(text, ["ချစ်", "love", "crush", "romance", "kiss"]):
        return random.choice(LOVE_REPLIES)

    if contains_any(text, ["friend", "သူငယ်ချင်း", "bro", "bestie"]):
        return random.choice(FRIEND_REPLIES)

    if contains_any(text, ["angry", "စိတ်တို", "ဒေါသ", "fight", "ရန်"]):
        return random.choice(ANGRY_REPLIES)

    if contains_any(text, ["roast", "စနောက်", "ပြောင်", "mock"]):
        return random.choice(ROAST_REPLIES) 

    if contains_any(text, ["fuck", "shit", "damn", "wtf", "ဆဲ"]):
        return random.choice(SWEAR_SOFT_REPLIES)

    if contains_any(text, ["jealous", "သဝန်တို", "မနာလို"]):
        return random.choice(JEALOUS_REPLIES)

    if contains_any(text, ["lonely", "alone", "တစ်ယောက်တည်း", "single"]):
        return random.choice(LONELY_REPLIES)

    if contains_any(text, ["flirt", "cute", "ချော", "လှ", "sweet"]):
        return random.choice(FLIRTY_REPLIES)

    if contains_any(text, ["sleep", "အိပ်", "good night", "gn", "ည"]):
        return random.choice(SLEEP_REPLIES)

    if contains_any(text, ["စား", "food", "hungry", "ဗိုက်ဆာ", "ထမင်း"]):
        return random.choice(FOOD_REPLIES)

    if contains_any(text, ["motivate", "အားပေး", "goal", "success", "ကြိုးစား"]):
        return random.choice(MOTIVATION_REPLIES)

    if contains_any(text, ["confuse", "ရှုပ်", "နားမလည်", "ဘာဆိုလို"]):
        return random.choice(CONFUSED_REPLIES)

    if contains_any(text, ["ဘာလုပ်", "what are you doing", "doing now"]):
        return "မင်း message ပို့လာမလားလို့ စောင့်နေတာ bro 😏"

    if contains_any(text, ["မင်းဘယ်သူ", "who are you"]):
        return "ငါလား 😎 AI မလိုတဲ့ human-style vibe bot bro"

    if contains_any(text, ["thank", "ကျေးဇူး", "thx", "thanks"]):
        return "ရပါတယ် bro 😄"

    if contains_any(text, ["bye", "goodbye", "see you", "တာ့တာ"]):
        return "တာ့တာ bro 👋 နောက်မှပြန်လာခဲ့"

    if text.endswith("?"):
        return random.choice(QUESTION_REPLIES)

    if len(text) <= 3:
        return random.choice(SHORT_REPLIES)

    return random.choice(RANDOM_REPLIES)


@app.get("/")
def home():
    return {
        "ok": True,
        "bot_token_set": bool(BOT_TOKEN),
        "base_url": BASE_URL,
        "webhook_secret_set": bool(WEBHOOK_SECRET),
        "mode": "human_style_free_bot"
        } 

@app.get("/set_webhook")
def set_webhook():
    webhook_url = f"{BASE_URL}/webhook/{WEBHOOK_SECRET}"
    return tg_api("setWebhook", {"url": webhook_url})


@app.get("/get_webhook_info")
def get_webhook_info():
    return tg_api("getWebhookInfo", {})


@app.get("/set_webhook")
def set_webhook():
    webhook_url = f"{BASE_URL}/webhook/{WEBHOOK_SECRET}"
    return tg_api("setWebhook", {"url": webhook_url})

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

    if chat_type == "private":
        reply = get_reply(text)
        send_message(chat_id, reply, message_id)
        return {"ok": True}

    if chat_type in ["group", "supergroup"]:
        reply_msg = message.get("reply_to_message")
        if reply_msg and reply_msg.get("from", {}).get("is_bot"):
            reply = get_reply(text)
            send_message(chat_id, reply, message_id)
            return {"ok": True}
