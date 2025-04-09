import telebot
from telebot.types import Message
import random

API_TOKEN = "YOUR_BOT_TOKEN"
OWNER_USERNAME = "@YourUsername"

bot = telebot.TeleBot(API_TOKEN)

# نقاط اللاعبين
user_points = {}
# ألقاب مخصصة
user_titles = {}
# ردود "كت"
kat_responses = ["نصيحة 1", "نصيحة 2", "سؤال 1", "سؤال 2", "فزورة 1", "فزورة 2"]

# ترحيب تلقائي
@bot.message_handler(content_types=["new_chat_members"])
def welcome_new_member(message: Message):
    for new_user in message.new_chat_members:
        bot.reply_to(message, f"هلا والله يا @{new_user.username or new_user.first_name}، نورت المجموعة!
مالك القروب: {OWNER_USERNAME}")

# أمر الكت
@bot.message_handler(commands=["كت"])
def kat_game(message: Message):
    response = random.choice(kat_responses)
    bot.reply_to(message, f"{response}")

# إضافة لقب
@bot.message_handler(commands=["لقب"])
def set_title(message: Message):
    try:
        parts = message.text.split(" ", 2)
        username = parts[1].lstrip("@")
        title = parts[2]
        user_titles[username] = title
        bot.reply_to(message, f"تم تعيين اللقب لـ @{username}: {title}")
    except:
        bot.reply_to(message, "اكتب الأمر كذا: /لقب @المستخدم اللقب")

# عرض نقاطي
@bot.message_handler(commands=["نقاطي"])
def my_points(message: Message):
    points = user_points.get(message.from_user.id, 0)
    bot.reply_to(message, f"نقاطك: {points}")

# زيادة النقاط (مثال بسيط عند استخدام أمر معين)
@bot.message_handler(commands=["نقطة"])
def add_point(message: Message):
    uid = message.from_user.id
    user_points[uid] = user_points.get(uid, 0) + 1
    bot.reply_to(message, f"تمت إضافة نقطة! نقاطك: {user_points[uid]}")

bot.infinity_polling()
