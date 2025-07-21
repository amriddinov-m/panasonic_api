from datetime import datetime

from aiogram import types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.MESSAGES import MESSAGES

from bot.keyboards.main import start_btns, phone_btns, main_menu_btn
from bot.loader import dp, bot, form_router
from user.models import User


@dp.message(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    print(message.from_user.full_name)
    user = User.objects.filter(tg_id=message.from_user.id)
    if user:
        await show_main_btns(message, state)
    else:
        keyboard = phone_btns()
        await message.answer(MESSAGES['user_start'].format(message.from_user.full_name), reply_markup=keyboard)


@dp.message(F.contact)
async def contact_search_step(message: types.Message):
    phone_number = message.contact.phone_number
    normalized_phone = phone_number.lstrip('+')
    updated = User.objects.filter(phone_number__in=[normalized_phone, f"+{normalized_phone}"]).update(tg_id=message.from_user.id)
    print(phone_number)
    if updated:
        keyboard = start_btns()
        user = User.objects.get(phone_number__in=[normalized_phone, f"+{normalized_phone}"])
        await bot.send_message(message.from_user.id,
                               MESSAGES['success_logged'].format(user.first_name, user.last_name, phone_number),
                               reply_markup=keyboard)
    else:
        await message.answer(MESSAGES['permission_denied'], reply_markup=None)


@form_router.message(F.text == '🔙 Главное меню')
async def show_main_btns(message: types.Message, state: FSMContext):
    keyboard = start_btns()
    await bot.send_message(message.from_user.id,
                           MESSAGES['main_step'],
                           reply_markup=keyboard)
    await state.clear()

