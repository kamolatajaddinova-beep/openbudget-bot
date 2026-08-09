
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from database import init_db, add_user, update_user_vote
from openbudget_api import send_openbudget_sms, verify_openbudget_code

TOKEN = "8905603586:AAHsAFlidgu68xH5THVZWylYR-G4hOmzFIc"
ADMIN_ID = "123456"

bot = Bot(token=TOKEN)
dp = Dispatcher()

class VoteProcess(StatesGroup):
    waiting_for_phone = State()
    waiting_for_code = State()

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗳 Ovoz berish"), KeyboardButton(text="📞 Yordam")]
        ],
        resize_keyboard=True
    )

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await add_user(message.from_user.id, message.from_user.username)
    await message.answer(
        "Assalomu alaykum! OpenBudget botiga xush kelibsiz.\nOvoz berish uchun quyidagi tugmani bosing:",
        reply_markup=get_main_keyboard()
    )

async def main():
    init_db()
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
