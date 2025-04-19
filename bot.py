# bot.py
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
import logging

API_TOKEN = "ТОКЕН_ТВОЕГО_БОТА"
WEBAPP_URL = "https://gif1ka.github.io/casebotapp/webapp/"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# В памяти: user_id → звёзды
user_stars = {}

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    user_id = msg.from_user.id
    user_stars[user_id] = user_stars.get(user_id, 0) + 20
    await msg.answer("👋 Привет! У тебя 20 ⭐️. Напиши /wheel чтобы крутить!")

@dp.message_handler(commands=["wheel"])
async def wheel(msg: types.Message):
    user_id = msg.from_user.id
    if user_stars.get(user_id, 0) < 15:
        await msg.answer("❌ Не хватает звёзд. Нужно 15 ⭐️")
        return
    user_stars[user_id] -= 15

    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton("🎰 Крутить!", web_app=WebAppInfo(url=WEBAPP_URL))
    )
    await msg.answer("🎉 Готов? Жми кнопку!", reply_markup=markup)

@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def handle_webapp_data(msg: types.Message):
    prize = msg.web_app_data.data
    await msg.answer(f"🎁 Ты выиграл: {prize}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp)
