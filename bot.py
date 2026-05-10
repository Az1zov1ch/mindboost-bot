from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
import json, os

TOKEN = "8738294425:AAHnZt6gaJAfYC1bQeztaf8saCEGIhalUvk"
BOT_USERNAME = "@mindboost_uz_bot"
ADMIN_ID = None
DATA_FILE = "data.json"

LANGS = {
    "uz": "🇺🇿 O'zbek",
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
    "tr": "🇹🇷 Türkçe",
    "ar": "🇸🇦 العربية",
}

TOPICS = {
    "uz": {
        "muvaffaqiyat": {"e": "🔥", "n": "Muvaffaqiyat", "cats": {"dunyo_liderlari": "Dunyo liderlari", "ozbeklar": "O'zbek yetakchilar", "mindset": "Mindset & Psixologiya"}},
        "talim":        {"e": "🎓", "n": "Ta'lim yo'li",  "cats": {"top_univer": "Harvard, MIT, Oxford", "stipendiya": "Stipendiyalar", "ielts": "IELTS & SAT sirlari"}},
        "biznes":       {"e": "💼", "n": "Biznes",        "cats": {"startap": "Startap g'oyalari", "freelance": "Freelance & Remote", "intervyu": "CV & Intervyu"}},
        "rivojlanish":  {"e": "💪", "n": "Rivojlanish",   "cats": {"soglik": "Sog'lom hayot", "kitoblar": "Kitob tahlillari", "vaqt": "Vaqtni boshqarish"}},
        "global":       {"e": "🌍", "n": "Global yoshlar", "cats": {"chet_el": "Chet elda o'qish", "tajriba": "Xalqaro tajriba", "yoshlar": "Yoshlar tarixi"}},
    },
    "ru": {
        "uspeh":        {"e": "🔥", "n": "Успех",         "cats": {"lidery": "Мировые лидеры", "uzbeki": "Узбекские лидеры", "mindset": "Мышление"}},
        "obrazovanie":  {"e": "🎓", "n": "Образование",   "cats": {"top_univer": "Harvard, MIT, Oxford", "stipendii": "Стипендии", "ielts": "IELTS & ЕГЭ"}},
        "biznes":       {"e": "💼", "n": "Бизнес",        "cats": {"startap": "Стартапы", "freelance": "Фриланс", "intervyu": "CV & Интервью"}},
        "razvitie":     {"e": "💪", "n": "Саморазвитие",  "cats": {"zdorove": "Здоровье", "knigi": "Обзоры книг", "vremya": "Тайм-менеджмент"}},
        "globalnyy":    {"e": "🌍", "n": "Молодёжь мира", "cats": {"zagranica": "Учёба за рубежом", "opyt": "Международный опыт", "istorii": "Истории успеха"}},
    },
    "en": {
        "success":      {"e": "🔥", "n": "Success",       "cats": {"world_leaders": "World Leaders", "mindset": "Mindset & Psychology", "habits": "Habits & Discipline"}},
        "education":    {"e": "🎓", "n": "Education",     "cats": {"top_univer": "Harvard, MIT, Oxford", "scholarships": "Scholarships", "ielts": "IELTS & SAT"}},
        "business":     {"e": "💼", "n": "Business",      "cats": {"startup": "Startups", "freelance": "Freelance & Remote", "career": "Career & CV"}},
        "selfdev":      {"e": "💪", "n": "Self-Development", "cats": {"health": "Health & Sport", "books": "Book Reviews", "productivity": "Productivity"}},
        "global":       {"e": "🌍", "n": "Global Youth",  "cats": {"study_abroad": "Study Abroad", "experience": "International Experience", "stories": "Success Stories"}},
    },
    "tr": {
        "basari":       {"e": "🔥", "n": "Başarı",        "cats": {"dunya_liderleri": "Dünya Liderleri", "mindset": "Düşünce Yapısı", "aliskanliklar": "Alışkanlıklar"}},
        "egitim":       {"e": "🎓", "n": "Eğitim",        "cats": {"top_univer": "Harvard, MIT, Oxford", "burslar": "Burslar", "dil_sinavlari": "Dil Sınavları"}},
        "is":           {"e": "💼", "n": "İş & Kariyer",  "cats": {"girisimcilik": "Girişimcilik", "freelance": "Freelance", "mulakat": "CV & Mülakat"}},
        "gelisim":      {"e": "💪", "n": "Kişisel Gelişim", "cats": {"saglik": "Sağlık & Spor", "kitaplar": "Kitap Yorumları", "verimlilik": "Verimlilik"}},
        "genclik":      {"e": "🌍", "n": "Dünya Gençliği", "cats": {"yurt_disi": "Yurt Dışı Eğitim", "deneyim": "Uluslararası Deneyim", "hikayeler": "Başarı Hikayeleri"}},
    },
    "ar": {
        "najah":        {"e": "🔥", "n": "النجاح",        "cats": {"qada": "قادة العالم", "mindset": "طريقة التفكير", "adat": "العادات والانضباط"}},
        "talim":        {"e": "🎓", "n": "التعليم",       "cats": {"jamiat": "هارفارد وMIT وأكسفورد", "manah": "المنح الدراسية", "ielts": "IELTS والاختبارات"}},
        "amal":         {"e": "💼", "n": "الأعمال",       "cats": {"sharika": "الشركات الناشئة", "hurr": "العمل الحر", "wazifa": "السيرة الذاتية"}},
        "tatawwur":     {"e": "💪", "n": "التطوير الذاتي", "cats": {"sihha": "الصحة والرياضة", "kutub": "مراجعات الكتب", "waqt": "إدارة الوقت"}},
        "shabab":       {"e": "🌍", "n": "شباب العالم",   "cats": {"kharij": "الدراسة في الخارج", "tajriba": "التجربة الدولية", "qisas": "قصص النجاح"}},
    },
}

WELCOME = {
    "uz": "Assalomu alaykum! 🎧\n\nO'zbekiston yoshlari uchun eng yaxshi podcast kliplari.\n\nTil tanlang:",
    "ru": "Добро пожаловать! 🎧\n\nЛучшие подкасты для молодёжи.\n\nВыберите язык:",
    "en": "Welcome! 🎧\n\nThe best podcast clips for youth.\n\nChoose your language:",
    "tr": "Hoş geldiniz! 🎧\n\nGençler için en iyi podcast klipler.\n\nDil seçin:",
    "ar": "!أهلاً وسهلاً 🎧\n\nأفضل مقاطع البودكاست للشباب.\n\nاختر لغتك:",
}

BACK_BTN = {"uz": "⬅️ Orqaga", "ru": "⬅️ Назад", "en": "⬅️ Back", "tr": "⬅️ Geri", "ar": "⬅️ رجوع"}
STATS_BTN = {"uz": "📊 Statistika", "ru": "📊 Статистика", "en": "📊 Statistics", "tr": "📊 İstatistik", "ar": "📊 إحصائيات"}
SAVE_BTN  = {"uz": "🔖 Saqlash", "ru": "🔖 Сохранить", "en": "🔖 Save", "tr": "🔖 Kaydet", "ar": "🔖 حفظ"}
NO_CLIPS  = {"uz": "Hali klip yo'q. Tez orada! 🚀", "ru": "Клипов пока нет. Скоро! 🚀", "en": "No clips yet. Coming soon! 🚀", "tr": "Henüz klip yok. Yakında! 🚀", "ar": "لا توجد مقاطع بعد. قريباً! 🚀"}

def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    db = {"clips": {}, "users": {}, "saved": {}, "stats": {"total": 0, "by_lang": {}, "by_topic": {}}}
    for lang in TOPICS:
        db["clips"][lang] = {}
        for t in TOPICS[lang]:
            db["clips"][lang][t] = {}
            for c in TOPICS[lang][t]["cats"]:
                db["clips"][lang][t][c] = []
    return db

def save(db):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

DB = load()
pending = {}

def get_lang(uid):
    return DB["users"].get(str(uid), {}).get("lang", "uz")

def set_lang(uid, lang):
    DB["users"].setdefault(str(uid), {})["lang"] = lang
    save(DB)

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    global ADMIN_ID
    uid = update.effective_user.id
    if ADMIN_ID is None:
        ADMIN_ID = uid
    DB["users"].setdefault(str(uid), {"lang": "uz", "name": update.effective_user.full_name})
    save(DB)

    args = ctx.args
    if args:
        p = args[0]
        parts = p.split("_")
        if len(parts) >= 2 and parts[0] in LANGS:
            set_lang(uid, parts[0])
            if len(parts) >= 3 and parts[1] in TOPICS.get(parts[0], {}):
                await show_topic(update, ctx, parts[0], parts[1])
                return

    kb = [[InlineKeyboardButton(v, callback_data="lang_" + k)] for k, v in LANGS.items()]
    await update.message.reply_text(
        "🎧 Yoshlar Podcast\n\nTil tanlang / Choose language:",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def show_topics(update, ctx, lang):
    uid = update.effective_user.id
    set_lang(uid, lang)
    kb = []
    for tkey, tval in TOPICS[lang].items():
        total = sum(len(DB["clips"][lang][tkey].get(c, [])) for c in tval["cats"])
        kb.append([InlineKeyboardButton(tval["e"] + " " + tval["n"] + " (" + str(total) + ")", callback_data="t_" + lang + "_" + tkey)])
    kb.append([InlineKeyboardButton(STATS_BTN[lang], callback_data="stats_" + lang)])
    msg = update.callback_query.message if update.callback_query else update.message
    text = WELCOME[lang]
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    else:
        await msg.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))

async def show_topic(update, ctx, lang, tkey):
    tval = TOPICS[lang][tkey]
    kb = []
    for ckey, cname in tval["cats"].items():
        count = len(DB["clips"][lang][tkey].get(ckey, []))
        kb.append([InlineKeyboardButton(cname + " (" + str(count) + ")", callback_data="c_" + lang + "_" + tkey + "_" + ckey)])
    kb.append([InlineKeyboardButton(BACK_BTN[lang], callback_data="lang_" + lang)])
    text = tval["e"] + " " + tval["n"]
    msg = update.callback_query.message if update.callback_query else update.message
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    else:
        await msg.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))

async def button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data
    uid = q.from_user.id
    lang = get_lang(uid)

    if d.startswith("lang_"):
        l = d[5:]
        await show_topics(update, ctx, l)

    elif d.startswith("t_"):
        parts = d.split("_", 2)
        await show_topic(update, ctx, parts[1], parts[2])

    elif d.startswith("c_"):
        parts = d.split("_", 3)
        l, tkey, ckey = parts[1], parts[2], parts[3]
        clips = DB["clips"][l][tkey].get(ckey, [])
        cname = TOPICS[l][tkey]["cats"][ckey]
        if not clips:
            await q.edit_message_text(
                NO_CLIPS[l],
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(BACK_BTN[l], callback_data="t_" + l + "_" + tkey)]])
            )
            return
        kb = []
        for i, clip in enumerate(clips):
            kb.append([InlineKeyboardButton("🎧 " + clip["name"], callback_data="k_" + l + "_" + tkey + "_" + ckey + "_" + str(i))])
        kb.append([InlineKeyboardButton(BACK_BTN[l], callback_data="t_" + l + "_" + tkey)])
        await q.edit_message_text(cname + " — " + str(len(clips)) + " klip:", reply_markup=InlineKeyboardMarkup(kb))

    elif d.startswith("k_"):
        parts = d.split("_", 4)
        l, tkey, ckey, idx = parts[1], parts[2], parts[3], int(parts[4])
        clips = DB["clips"][l][tkey].get(ckey, [])
        if idx >= len(clips):
            return
        clip = clips[idx]
        DB["stats"]["total"] = DB["stats"].get("total", 0) + 1
        DB["stats"]["by_lang"][l] = DB["stats"]["by_lang"].get(l, 0) + 1
        save(DB)
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(SAVE_BTN[l], callback_data="save_" + l + "_" + tkey + "_" + ckey + "_" + str(idx))],
            [InlineKeyboardButton(BACK_BTN[l], callback_data="c_" + l + "_" + tkey + "_" + ckey)]
        ])
        await q.message.reply_audio(audio=clip["file_id"], title=clip["name"], reply_markup=kb)
        await q.edit_message_text("▶️ " + clip["name"], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(BACK_BTN[l], callback_data="c_" + l + "_" + tkey + "_" + ckey)]]))

    elif d.startswith("save_"):
        parts = d.split("_", 4)
        l, tkey, ckey, idx = parts[1], parts[2], parts[3], int(parts[4])
        key = l + "_" + tkey + "_" + ckey + "_" + str(idx)
        saved = DB["saved"].setdefault(str(uid), [])
        if key not in saved:
            saved.append(key)
            save(DB)
            await q.answer("✅ Saqlandi!" if lang == "uz" else "✅ Saved!")
        else:
            await q.answer("Allaqachon saqlangan!" if lang == "uz" else "Already saved!")

    elif d.startswith("stats_"):
        l = d[6:]
        total = DB["stats"].get("total", 0)
        by_lang = DB["stats"].get("by_lang", {})
        text = "📊 Statistika\n\nJami tinglashlar: " + str(total) + "\n\n"
        for ln, lname in LANGS.items():
            cnt = by_lang.get(ln, 0)
            text += lname + ": " + str(cnt) + "\n"
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(BACK_BTN[l], callback_data="lang_" + l)]]))

async def media_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    global ADMIN_ID
    msg = update.message
    if not msg:
        return
    uid = msg.from_user.id
    if ADMIN_ID is None:
        ADMIN_ID = uid
    if uid != ADMIN_ID:
        return

    file_id = None
    if msg.audio:
        file_id = msg.audio.file_id
    elif msg.voice:
        file_id = msg.voice.file_id
    elif msg.document:
        file_id = msg.document.file_id

    if file_id:
        caption = msg.caption or ""
        parts = caption.strip().split(" ", 3)
        if len(parts) >= 4 and parts[0] in TOPICS and parts[1] in TOPICS[parts[0]] and parts[2] in TOPICS[parts[0]][parts[1]]["cats"]:
            lang, tkey, ckey, name = parts[0], parts[1], parts[2], parts[3]
            DB["clips"][lang][tkey].setdefault(ckey, []).append({"name": name, "file_id": file_id})
            save(DB)
            await msg.reply_text("✅ Qo'shildi: " + name)
        else:
            pending[uid] = file_id
            tips = ""
            for lang in list(TOPICS.keys())[:2]:
                for tkey in list(TOPICS[lang].keys())[:1]:
                    for ckey in list(TOPICS[lang][tkey]["cats"].keys())[:1]:
                        tips += lang + " " + tkey + " " + ckey + " Klip nomi\n"
            await msg.reply_text("✅ Fayl qabul qilindi!\n\nFormat:\n<til> <topic> <kategoriya> <nom>\n\nMisol:\n" + tips)
        return

    if msg.text and uid in pending:
        parts = msg.text.strip().split(" ", 3)
        if len(parts) < 4:
            await msg.reply_text("Format: <til> <topic> <kategoriya> <nom>")
            return
        lang, tkey, ckey, name = parts[0], parts[1], parts[2], parts[3]
        if lang not in TOPICS or tkey not in TOPICS[lang] or ckey not in TOPICS[lang][tkey]["cats"]:
            await msg.reply_text("Noto'g'ri til/topic/kategoriya!")
            return
        file_id = pending.pop(uid)
        DB["clips"][lang][tkey].setdefault(ckey, []).append({"name": name, "file_id": file_id})
        save(DB)
        await msg.reply_text("✅ Qo'shildi: " + name)

async def broadcast(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not ctx.args:
        await update.message.reply_text("Format: /broadcast <xabar>")
        return
    text = " ".join(ctx.args)
    sent = 0
    for uid in DB["users"]:
        try:
            await ctx.bot.send_message(int(uid), "📢 " + text)
            sent += 1
        except:
            pass
    await update.message.reply_text("✅ " + str(sent) + " ta foydalanuvchiga yuborildi!")

async def qr_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not ctx.args:
        await update.message.reply_text(
            "QR URL yaratish:\n/qr <joy> <til> <topic>\n\nMisol:\n/qr avtobus_001 uz muvaffaqiyat\n/qr maktab_14 en education\n/qr metro_yunusobod ru uspeh"
        )
        return
    parts = ctx.args
    joy = parts[0] if len(parts) > 0 else "joy"
    lang = parts[1] if len(parts) > 1 else "uz"
    topic = parts[2] if len(parts) > 2 else ""
    param = lang + "_" + joy + ("_" + topic if topic else "")
    url = "https://t.me/" + BOT_USERNAME + "?start=" + param
    await update.message.reply_text(
        "📱 QR URL:\n\n" + url + "\n\n📌 Bu URLni qr-code-generator.com da QR kodga aylantiring!"
    )

async def admin_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    total_clips = sum(
        len(DB["clips"].get(l, {}).get(t, {}).get(c, []))
        for l in TOPICS for t in TOPICS[l] for c in TOPICS[l][t]["cats"]
    )
    text = (
        "👑 Admin Panel\n\n"
        "👥 Foydalanuvchilar: " + str(len(DB["users"])) + "\n"
        "🎧 Jami kliplar: " + str(total_clips) + "\n"
        "▶️ Jami tinglashlar: " + str(DB["stats"].get("total", 0)) + "\n\n"
        "Buyruqlar:\n"
        "/broadcast <xabar> — Hammaga yuborish\n"
        "/qr <joy> <til> <topic> — QR URL\n\n"
        "Audio yuklash formati:\n"
        "<til> <topic> <kategoriya> <nom>\n\n"
        "Misol:\n"
        "uz muvaffaqiyat dunyo_liderlari Elon Musk\n"
        "en success mindset David Goggins\n"
        "ru uspeh mindset Илон Маск"
    )
    await update.message.reply_text(text)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin_cmd))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(CommandHandler("qr", qr_cmd))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.ALL, media_handler))
print("Bot ishlamoqda... @mindboost_uz_bot")
app.run_polling()