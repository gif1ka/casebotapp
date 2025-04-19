from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import logging
import asyncio

API_TOKEN = "8150418145:AAEkmDih5f1rRA-Jvcbopsk158dv7YKFtWY"
WEBAPP_URL = "https://github.com/gif1ka/casebotapp.git"

# Для примера храним звезды в памяти (лучше использовать БД)
user_stars = {}

# Задай ID админа, если хочешь
ADMIN_ID = 6839682552

# Включаем логирование
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# /start - приветствие и начисление начальных звёзд
@dp.message(F.command == "start")
async def start(message: types.Message):
    user_id = message.from_user.id
    user_stars[user_id] = user_stars.get(user_id, 0) + 20  # дарим 20 звёзд
    await message.answer("Привет! У тебя 20 ⭐️. Напиши /wheel чтобы испытать удачу!")

# /wheel - запускает мини-приложение
@dp.message(F.command == "wheel")
async def wheel(message: types.Message):
    user_id = message.from_user.id
    stars = user_stars.get(user_id, 0)

    if stars < 15:
        await message.answer("Недостаточно звёзд 😔 Нужно 15 ⭐️")
        return

    user_stars[user_id] -= 15  # списываем 15 звёзд

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 Крутить колесо", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])

    await message.answer("Тебе доступно колесо удачи! Крути и получи приз:", reply_markup=keyboard)

# Обработка результата от WebApp
@dp.message(F.web_app_data)
async def webapp_result(message: types.Message):
    prize = message.web_app_data.data
    await message.answer(f"🎉 Ты выиграл: {prize}")

    # Например, отправка админу:
    if ADMIN_ID:
        await bot.send_message(ADMIN_ID, f"Пользователь @{message.from_user.username or message.from_user.id} выиграл: {prize}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())