import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8156313241:AAHUKtlzKZ219V2yqlFJhXbsHNQku9Eh1PM"
# ID владельца, которому будут приходить уведомления
ADMIN_ID = 8345948344 

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_contact_keyboard():
    button = KeyboardButton(text="Отправить номер телефона", request_contact=True)
    return ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True, one_time_keyboard=True)

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Нажми на кнопку ниже, чтобы поделиться своим номером:", reply_markup=get_contact_keyboard())

@dp.message(F.contact)
async def contact_handler(message: types.Message):
    phone = message.contact.phone_number
    user_id = message.from_user.id
    username = message.from_user.username
    
    # Отправка номера владельцу бота
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Получен новый номер:\nНомер: {phone}\nЮзер: @{username}\nID: {user_id}"
    )
    
    await message.answer("Спасибо! Ваш номер отправлен администратору.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
