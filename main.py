import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация
API_TOKEN = os.getenv('API_TOKEN')
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Состояния
class Form(StatesGroup):
    waiting_for_phone = State()
    waiting_for_code = State()

# Кнопка для номера
def get_phone_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton("Отправить номер телефона", request_contact=True)
    keyboard.add(button)
    return keyboard

# Команда старт
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Нажмите кнопку ниже, чтобы отправить номер:", reply_markup=get_phone_keyboard())
    await Form.waiting_for_phone.set()

# Обработка номера
@dp.message_handler(content_types=types.ContentType.CONTACT, state=Form.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    await message.answer("Номер получен. Теперь введите код:", reply_markup=ReplyKeyboardRemove())
    await Form.waiting_for_code.set()

# Обработка кода
@dp.message_handler(state=Form.waiting_for_code)
async def process_code(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    phone = user_data.get('phone')
    code = message.text
    
    # Финальный вывод
    await message.answer(f"Данные получены:\nНомер: {phone}\nКод: {code}")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
