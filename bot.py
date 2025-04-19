# bot.py
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
import logging
import asyncio

API_TOKEN = "7695148598:AAFoPXKcPlZV6e63Puu5vdPO1EKG_0Tvdj0"
WEBAPP_URL = "https://gif1ka.github.io/casebotapp/webapp/"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# В памяти: user_id → звёзды
user_stars = {}

@dp.message(Command("start"))
async def start(msg: types.Message):
    user_id = msg.from_user.id
    user_stars[user_id] = user_stars.get(user_id, 0) + 20
    await msg.answer("👋 Привет! У тебя 20 ⭐️. Напиши /wheel чтобы крутить!")

@dp.message(Command("wheel"))
async def wheel(msg: types.Message):
    user_id = msg.from_user.id
    if user_stars.get(user_id, 0) < 15:
        await msg.answer("❌ Не хватает звёзд. Нужно 15 ⭐️")
        return
    user_stars[user_id] -= 15

    markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🎰 Крутить!", web_app=WebAppInfo(url=WEBAPP_URL))
    ]])
    await msg.answer("🎉 Готов? Жми кнопку!", reply_markup=markup)

@dp.message(F.content_type == "web_app_data")
async def handle_webapp_data(msg: types.Message):
    prize = msg.web_app_data.data
    await msg.answer(f"🎁 Ты выиграл: {prize}")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())