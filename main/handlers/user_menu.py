import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from main.data.config import chat_id
from main.data.loader import bot

logging.basicConfig(filename="log.txt", level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

router = Router()


def regular_check(email: str) -> bool:
    return email and "@" in email and "." in email


class Form(StatesGroup):
    credentials = State()
    phone_number = State()
    work_expierience = State()
    location = State()


@router.message(Command("start_form"))
async def start(message: Message, state: FSMContext):
    await message.answer("Введите ваши полные данные (имя и фамилия)")
    await state.set_state(Form.credentials)


@router.message(Form.credentials)
async def credentials(message: Message, state: FSMContext):
    await state.update_data(credentials=message.text)
    await message.answer("Введите актуальные контактные данные (@ и тел.)")
    await state.set_state(Form.phone_number)


@router.message(Form.phone_number)
async def phone_number(message: Message, state: FSMContext):
    if not regular_check(email=message.text):
        await message.answer("Укажите верный имейл!")
        return
    await state.update_data(phone_number=message.text)
    await message.answer("Укажите свой опыт работы (годы, должность)")
    await state.set_state(Form.work_expierience)


@router.message(Form.work_expierience)
async def work_expierience(message: Message, state: FSMContext):
    await state.update_data(work_expierience=message.text)
    await message.answer("Укажите вашу адресную информацию")
    await state.set_state(Form.location)


@router.message(Form.location)
async def location(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    data = await state.get_data()
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Accept", callback_data="Accept")],
                                               [InlineKeyboardButton(text="Decline", callback_data="Decline")]])
    await bot.send_message(chat_id=chat_id,
                           text=(f"Полученные данны от пользователя:\n"
                                 f"Имя: {data['credentials']}\n"
                                 f"Телефон: {data['phone_number']}\n"
                                 f"Опыт работы: {data['work_expierience']}"
                                 f"\nАдрес: {data['location']}"),
                           reply_markup=kb)
    await state.clear()


@router.callback_query()
async def accept_decline(call: CallbackQuery):
    await call.answer()
    if call.data == "Accept":
        await bot.send_message(chat_id=call.from_user.id, text="Ваша заявка принята!")
    elif call.data == "Decline":
        await bot.send_message(chat_id=call.from_user.id, text="Ваша заявка отклонена!")
