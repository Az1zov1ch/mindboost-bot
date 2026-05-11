from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
import json, os, logging

logging.basicConfig(level=logging.INFO)

TOKEN = "8738294425:AAHnZt6gaJAfYC1bQeztaf8saCEGIhalUvk"
BOT_USERNAME = "mindboost_uz_bot"
ADMIN_ID = 7324883893

DATA_FILE = os.environ.get("DATA_PATH", "data.json")

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
        "talim":        {"e": "🎓", "n": "Ta'lim yo'li",  "cats": {"top_univer": "Harvard, MIT, Oxford", "stipendiya": "Stipendiyalar", "ielts": "IELTS & SAT"}},
        "biznes":       {"e": "💼", "n": "Biznes",        "cats": {"startap": "Startap", "freelance": "Freelance", "intervyu": "CV & Intervyu"}},
        "rivojlanish":  {"e": "💪", "n": "Rivojlanish",   "cats": {"soglik": "Sog'lom hayot", "kitoblar": "Kitoblar", "vaqt": "Vaqt boshqarish"}},
        "global":       {"e": "🌍", "n": "Global yoshlar", "cats": {"chet_el": "Chet elda o'qish", "tajriba": "Xalqaro tajriba", "yoshlar": "Yoshlar tarixi"}},
    },
    "ru": {
        "uspeh":       {"e": "🔥", "n": "Успех",         "cats": {"lidery": "Мировые лидеры", "uzbeki": "Узбекские лидеры", "mindset": "Мышление"}},
        "obrazovanie": {"e": "🎓", "n": "Образование",   "cats": {"top_univer": "Harvard, MIT, Oxford", "stipendii": "Стипендии", "ielts": "IELTS & ЕГЭ"}},
        "biznes":      {"e": "💼", "n": "Бизнес",        "cats": {"startap": "Стартапы", "freelance": "Фриланс", "intervyu": "CV & Интервью"}},
        "razvitie":    {"e": "💪", "n": "Саморазвитие",  "cats": {"zdorove": "Здоровье", "knigi": "Книги", "vremya": "Тайм-менеджмент"}},
        "globalnyy":   {"e": "🌍", "n": "Молодёжь мира", "cats": {"zagranica": "Учёба за рубежом", "opyt": "Международный опыт", "istorii": "Истории успеха"}},
    },
    "en": {
        "success":   {"e": "🔥", "n": "Success",          "cats": {"world_leaders": "World Leaders", "mindset": "Mindset", "habits": "Habits & Discipline"}},
        "education": {"e": "🎓", "n": "Education",        "cats": {"top_univer": "Harvard, MIT, Oxford", "scholarships": "Scholarships", "ielts": "IELTS & SAT"}},
        "business":  {"e": "💼", "n": "Business",         "cats": {"startup": "Startups", "freelance": "Freelance", "career": "Career & CV"}},
        "selfdev":   {"e": "💪", "n": "Self-Development", "cats": {"health": "Health & Sport", "books": "Books", "productivity": "Productivity"}},
        "global":    {"e": "🌍", "n": "Global Youth",     "cats": {"study_abroad": "Study Abroad", "experience": "International", "stories": "Success Stories"}},
    },
    "tr": {
        "basari":  {"e": "🔥", "n": "Başarı",           "cats": {"dunya_liderleri": "Dünya Liderleri", "mindset": "Düşünce", "aliskanliklar": "Alışkanlıklar"}},
        "egitim":  {"e": "🎓", "n": "Eğitim",           "cats": {"top_univer": "Harvard, MIT, Oxford", "burslar": "Burslar", "dil_sinavlari": "Dil Sınavları"}},
        "is":      {"e": "💼", "n": "İş & Kariyer",     "cats": {"girisimcilik": "Girişimcilik", "freelance": "Freelance", "mulakat": "CV & Mülakat"}},
        "gelisim": {"e": "💪", "n": "Kişisel Gelişim",  "cats": {"saglik": "Sağlık", "kitaplar": "Kitaplar", "verimlilik": "Verimlilik"}},
        "genclik": {"e": "🌍", "n": "Dünya Gençliği",   "cats": {"yurt_disi": "Yurt Dışı", "deneyim": "Deneyim", "hikayeler": "Başarı Hikayeleri"}},
    },
    "ar": {
        "najah":    {"e": "🔥", "n": "النجاح",          "cats": {"qada": "قادة العالم", "mindset": "طريقة التفكير", "adat": "العادات"}},
        "talim":    {"e": "🎓", "n": "التعليم",         "cats": {"jamiat": "هارفارد وMIT", "manah": "المنح", "ielts": "IELTS"}},
        "amal":     {"e": "💼", "n": "الأعمال",         "cats": {"sharika": "الشركات الناشئة", "hurr": "العمل الحر", "wazifa": "السيرة الذاتية"}},
        "tatawwur": {"e": "💪", "n": "التطوير الذاتي",  "cats": {"sihha": "الصحة", "kutub": "الكتب", "waqt": "إدارة الوقت"}},
        "shabab":   {"e": "🌍", "n": "شباب العالم",     "cats": {"kharij": "الدراسة في الخارج", "tajriba": "التجربة", "qisas": "قصص النجاح"}},
    },
}

def empty_db():
    db = {"clips": {}, "users": {}, "stats": {"total": 0, "by_lang": {}, "by_topic": {}}}
    for lang in TOPICS:
        db["clips"][lang] = {}
        for t in TOPICS[lang]:
            db["clips"][lang][t] = {}
            for c in TOPICS[lang][t]["cats"]:
                db["clips"][lang][t][c] = []
    return db

def load():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return empty_db()

def save(db):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error("Save error: " + str(e))

DB = load()
pending = {}

def get_lang(uid):
    return DB["users"].get(str(uid), {}).get("lang", "uz")

def main_menu_kb(lang):
    kb = []
    for tkey, tval in TOPICS[lang].items():
        total = sum(len(DB["clips"].get(lang, {}).get(tkey, {}).get(c, [])) for c in tval["cats"])
        kb.append([InlineKeyboardButton(tval["e"] + " " + tval["n"] + " (" + str(total) + ")", callback_data="t_" + lang + "_" + tkey)])
    kb.append([InlineKeyboardButton("🌍 Tilni o'zgartir", callback_data="main_lang")])
    return InlineKeyboardMarkup(kb)

def topic_menu_kb(lang, tkey):
    tval = TOPICS[lang][tkey]
    kb = []
    for ckey, cname in tval["cats"].items():
        count = len(DB["clips"].get(lang, {}).get(tkey, {}).get(ckey, []))
        kb.append([InlineKeyboardButton(cname + " (" + str(count) + ")", callback_data="c_" + lang + "_" + tkey + "_" + ckey)])
    kb.append([InlineKeyboardButton("🌍 Tilni o'zgartir", callback_data="change_lang_" + tkey)])
    kb.append([InlineKeyboardButton("⬅️ Bosh menyu", callback_data="main_menu")])
    return InlineKeyboardMarkup(kb)

def lang_select_kb(back_data):
    kb = []
    row = []
    for i, (lkey, lname) in enumerate(LANGS.items()):
        row.append(InlineKeyboardButton(lname, callback_data="setlang_" + lkey + "_" + back_data))
        if len(row) == 2:
            kb.append(row)
            row = []
    if row:
        kb.append(row)
    kb.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="back_" + back_data)])
    return InlineKeyboardMarkup(kb)

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    DB["users"].setdefault(str(uid), {"lang": "uz", "name": update.effective_user.full_name})
    save(DB)
    lang = get_lang(uid)

    args = ctx.args
    if args:
        param = args[0]
        parts = param.split("_", 1)
        req_lang = parts[0] if parts[0] in TOPICS else None
        req_tkey = parts[1] if len(parts) > 1 else None

        if not req_lang:
            for l in TOPICS:
                if param in TOPICS[l]:
                    req_lang = l
                    req_tkey = param
                    break

        if req_lang and req_tkey and req_tkey in TOPICS.get(req_lang, {}):
            DB["users"][str(uid)]["lang"] = req_lang
            save(DB)
            tval = TOPICS[req_lang][req_tkey]
            await update.message.reply_text(
                tval["e"] + " " + tval["n"],
                reply_markup=topic_menu_kb(req_lang, req_tkey)
            )
            return

    await update.message.reply_text(
        "🎧 MindBoost\n\nYo'nalish tanlang:",
        reply_markup=main_menu_kb(lang)
    )

async def button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data
    uid = q.from_user.id
    lang = get_lang(uid)

    if d == "main_menu":
        await q.edit_message_text("🎧 MindBoost\n\nYo'nalish tanlang:", reply_markup=main_menu_kb(lang))

    elif d == "main_lang":
        await q.edit_message_text("🌍 Til tanlang:", reply_markup=lang_select_kb("main"))

    elif d.startswith("mainlang_"):
        new_lang = d[9:]
        if new_lang in TOPICS:
            DB["users"][str(uid)]["lang"] = new_lang
            save(DB)
            await q.edit_message_text("🎧 MindBoost\n\nYo'nalish tanlang:", reply_markup=main_menu_kb(new_lang))

    elif d.startswith("t_"):
        parts = d.split("_", 2)
        l, tkey = parts[1], parts[2]
        if l not in TOPICS or tkey not in TOPICS[l]:
            return
        tval = TOPICS[l][tkey]
        await q.edit_message_text(tval["e"] + " " + tval["n"], reply_markup=topic_menu_kb(l, tkey))

    elif d.startswith("change_lang_"):
        tkey = d[12:]
        await q.edit_message_text("🌍 Til tanlang:", reply_markup=lang_select_kb(tkey))

    elif d.startswith("setlang_"):
        parts = d.split("_", 2)
        new_lang, back = parts[1], parts[2]
        if new_lang not in TOPICS:
            return
        DB["users"][str(uid)]["lang"] = new_lang
        save(DB)
        if back == "main":
            await q.edit_message_text("🎧 MindBoost\n\nYo'nalish tanlang:", reply_markup=main_menu_kb(new_lang))
        elif back in TOPICS.get(new_lang, {}):
            tval = TOPICS[new_lang][back]
            await q.edit_message_text(tval["e"] + " " + tval["n"], reply_markup=topic_menu_kb(new_lang, back))
        else:
            first = list(TOPICS[new_lang].keys())[0]
            tval = TOPICS[new_lang][first]
            await q.edit_message_text(tval["e"] + " " + tval["n"], reply_markup=topic_menu_kb(new_lang, first))

    elif d.startswith("back_"):
        back = d[5:]
        if back == "main":
            await q.edit_message_text("🎧 MindBoost\n\nYo'nalish tanlang:", reply_markup=main_menu_kb(lang))
        elif back in TOPICS.get(lang, {}):
            tval = TOPICS[lang][back]
            await q.edit_message_text(tval["e"] + " " + tval["n"], reply_markup=topic_menu_kb(lang, back))

    elif d.startswith("c_"):
        parts = d.split("_", 3)
        l, tkey, ckey = parts[1], parts[2], parts[3]
        if l not in TOPICS or tkey not in TOPICS[l] or ckey not in TOPICS[l][tkey]["cats"]:
            return
        clips = DB["clips"].get(l, {}).get(tkey, {}).get(ckey, [])
        cname = TOPICS[l][tkey]["cats"][ckey]
        if not clips:
            await q.edit_message_text(
                "📭 " + cname + "\n\nHali klip qo'shilmagan. Tez orada! 🚀",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Orqaga", callback_data="t_" + l + "_" + tkey)]])
            )
            return
        kb = []
        for i, clip in enumerate(clips):
            kb.append([InlineKeyboardButton("🎧 " + clip["name"], callback_data="k_" + l + "_" + tkey + "_" + ckey + "_" + str(i))])
        kb.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="t_" + l + "_" + tkey)])
        await q.edit_message_text(cname + " — " + str(len(clips)) + " ta klip:", reply_markup=InlineKeyboardMarkup(kb))

    elif d.startswith("k_"):
        parts = d.split("_", 4)
        l, tkey, ckey, idx = parts[1], parts[2], parts[3], int(parts[4])
        clips = DB["clips"].get(l, {}).get(tkey, {}).get(ckey, [])
        if idx >= len(clips):
            return
        clip = clips[idx]
        DB["stats"]["total"] = DB["stats"].get("total", 0) + 1
        DB["stats"]["by_lang"][l] = DB["stats"]["by_lang"].get(l, 0) + 1
        save(DB)
        await q.message.reply_audio(
            audio=clip["file_id"],
            title=clip["name"],
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Orqaga", callback_data="c_" + l + "_" + tkey + "_" + ckey)]])
        )
        await q.edit_message_text(
            "▶️ " + clip["name"],
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Orqaga", callback_data="c_" + l + "_" + tkey + "_" + ckey)]])
        )

async def media_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return
    uid = msg.from_user.id
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
            DB["clips"].setdefault(lang, {}).setdefault(tkey, {}).setdefault(ckey, []).append({"name": name, "file_id": file_id})
            save(DB)
            cname = TOPICS[lang][tkey]["cats"][ckey]
            await msg.reply_text("✅ " + name + "\n📂 " + TOPICS[lang][tkey]["n"] + " > " + cname)
        else:
            pending[uid] = file_id
            await msg.reply_text(
                "✅ Fayl qabul qilindi!\n\n"
                "Endi yozing:\n"
                "<til> <topic> <kategoriya> <nom>\n\n"
                "Misol:\n"
                "uz muvaffaqiyat dunyo_liderlari Elon Musk\n"
                "en success habits David Goggins\n"
                "ru uspeh mindset Илон Маск"
            )
        return

    if msg.text and uid in pending:
        parts = msg.text.strip().split(" ", 3)
        if len(parts) < 4:
            await msg.reply_text("Format: <til> <topic> <kategoriya> <nom>")
            return
        lang, tkey, ckey, name = parts[0], parts[1], parts[2], parts[3]
        if lang not in TOPICS or tkey not in TOPICS[lang] or ckey not in TOPICS[lang][tkey]["cats"]:
            await msg.reply_text("❌ Noto'g'ri!\n\nMisol:\nuz muvaffaqiyat dunyo_liderlari Elon Musk")
            return
        file_id = pending.pop(uid)
        DB["clips"].setdefault(lang, {}).setdefault(tkey, {}).setdefault(ckey, []).append({"name": name, "file_id": file_id})
        save(DB)
        cname = TOPICS[lang][tkey]["cats"][ckey]
        await msg.reply_text("✅ " + name + "\n📂 " + TOPICS[lang][tkey]["n"] + " > " + cname)

async def admin_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    total = sum(len(DB["clips"].get(l, {}).get(t, {}).get(c, [])) for l in TOPICS for t in TOPICS[l] for c in TOPICS[l][t]["cats"])
    by_lang = DB["stats"].get("by_lang", {})
    lang_stats = "\n".join(LANGS[l] + ": " + str(by_lang.get(l, 0)) for l in LANGS)
    await update.message.reply_text(
        "👑 Admin Panel\n\n"
        "👥 Foydalanuvchilar: " + str(len(DB["users"])) + "\n"
        "🎧 Jami kliplar: " + str(total) + "\n"
        "▶️ Jami tinglashlar: " + str(DB["stats"].get("total", 0)) + "\n\n"
        "Tinglashlar:\n" + lang_stats + "\n\n"
        "Buyruqlar:\n"
        "/qr — QR URLlar\n"
        "/broadcast <xabar> — Hammaga yuborish\n\n"
        "Audio yuklash:\n"
        "uz muvaffaqiyat dunyo_liderlari Elon Musk\n"
        "en success habits David Goggins"
    )

async def qr_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    text = "📱 QR URLlar:\n\n"
    for lang, topics in TOPICS.items():
        text += LANGS[lang] + ":\n"
        for tkey, tval in topics.items():
            url = "https://t.me/" + BOT_USERNAME + "?start=" + lang + "_" + tkey
            text += tval["e"] + " " + tval["n"] + ":\n" + url + "\n"
        text += "\n"
    await update.message.reply_text(text)

async def broadcast_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
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

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin_cmd))
app.add_handler(CommandHandler("qr", qr_cmd))
app.add_handler(CommandHandler("broadcast", broadcast_cmd))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.ALL, media_handler))
print("Bot ishlamoqda... @mindboost_uz_bot")
app.run_polling()