import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Вставьте сюда токен, полученный от BotFather
TOKEN = "8156313241:AAHUKtlzKZ219V2yqlFJhXbsHNQku9Eh1PM"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаем клавиатуру с кнопкой запроса номера
def get_contact_keyboard():
    button = KeyboardButton(
        text="Отправить номер телефона", 
        request_contact=True
    )
    return ReplyKeyboardMarkup(
        keyboard=[[button]], 
        resize_keyboard=True, 
        one_time_keyboard=True
    )

# Команда /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Привет! Нажми на кнопку ниже, чтобы поделиться своим номером:",
        reply_markup=get_contact_keyboard()
    )

# Обработка полученного контакта
@dp.message(F.contact)
async def contact_handler(message: types.Message):
    phone = message.contact.phone_number
    name = message.contact.first_name
    await message.answer(f"Спасибо, {name}! Я получил ваш номер: {phone}")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
