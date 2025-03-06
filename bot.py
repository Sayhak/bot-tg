import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# Получаем токен из переменных окружения
TOKEN = os.getenv("BOT_TOKEN")

# Настройка бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Логирование
logging.basicConfig(level=logging.INFO)

# Клавиатура
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("📋 Список турниров"))
keyboard.add(KeyboardButton("ℹ️ О боте"))

# Список турниров
tournaments = [
    {"name": "PUBG Mobile Cup", "date": "10 марта", "organizer": "@ТвойКонтакт"},
    {"name": "Battle Royale Championship", "date": "15 марта", "organizer": "@ТвойКонтакт"}
]

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("Привет! Я бот для записи на турниры по PUBG Mobile.", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "📋 Список турниров")
async def list_tournaments(message: types.Message):
    text = "Доступные турниры:\n\n"
    for t in tournaments:
        text += f"🏆 {t['name']}\n📅 {t['date']}\n💰 Оплата: {t['organizer']}\n\n"
    text += "Для записи отправь мне свой никнейм и номер телефона."
    await message.answer(text)

@dp.message_handler()
async def collect_info(message: types.Message):
    user_info = f"👤 Игрок: {message.from_user.full_name}\n🔰 Никнейм: {message.text}\n📞 Контакт: @{message.from_user.username or 'не указан'}"
    await message.answer("✅ Ты записан! Напиши организатору для оплаты.")
    await bot.send_message(tournaments[0]["organizer"], user_info)

if name == "__main__":
    executor.start_polling(dp, skip_updates=True)