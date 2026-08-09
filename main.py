import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from database import init_db, add_user, update_user_vote, get_user_data
from openbudget_api import send_openbudget_sms, verify_openbudget_code

PASTDAGI TOKEN O'RNIGA O'ZINGIZNING TOKENINGIZNI QO'YING

TOKEN = "8905603586:AAHsAFlidgu68xH5THVZWylYR-G4hOmzFIc"
INITIATIVE_ID = "123456"

bot = Bot(token=TOKEN)
dp = Dispatcher()

class VoteProcess(StatesGroup):
waiting_for_phone = State()
waiting_for_code = State()

def main_keyboard():
return ReplyKeyboardMarkup(
keyboard=[
[KeyboardButton(text="🗳 Ovoz berish"), KeyboardButton(text="💰 Balans")],
[KeyboardButton(text="📞 Yordam")]
],
resize_keyboard=True
)

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
add_user(message.from_user.id)
await message.answer("Open Budget botiga xush kelibsiz!", reply_markup=main_keyboard())

@dp.message(F.text == "🗳 Ovoz berish")
async def start_vote(message: types.Message, state: FSMContext):
kb = ReplyKeyboardMarkup(
keyboard=[[KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)]],
resize_keyboard=True
)
await message.answer("Telefon raqamingizni yuboring:", reply_markup=kb)
await state.set_state(VoteProcess.waiting_for_phone)

@dp.message(VoteProcess.waiting_for_phone, F.contact)
async def process_phone(message: types.Message, state: FSMContext):
phone = message.contact.phone_number
res = await send_openbudget_sms(phone, INITIATIVE_ID)
if res["success"]:
await state.update_data(phone=phone, session_id=res["session_id"])
await message.answer("SMS kodni kiriting:", reply_markup=ReplyKeyboardRemove())
await state.set_state(VoteProcess.waiting_for_code)
else:
