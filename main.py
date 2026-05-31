# Импорт библиотеки aiogram для работы с Telegram API
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

# Инициализация бота и диспетчера
API_TOKEN = '8156313241:AAHUKtlzKZ219V2yqlFJhXbsHNQku9Eh1PM'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Определение состояний FSM
class Form(StatesGroup):
    waiting_for_phone = State()
    waiting_for_code = State()

# Команда старт
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Введите номер телефона:")
    await Form.waiting_for_phone.set()

# Получение номера
@dp.message_handler(state=Form.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.reply("Введите код:")
    await Form.waiting_for_code.set()

# Получение кода и вывод данных
@dp.message_handler(state=Form.waiting_for_code)
async def process_code(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    phone = user_data.get('phone')
    code = message.text
    
    # Вывод полученных данных
    await message.answer(f"Номер: {phone}\nКод: {code}")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
