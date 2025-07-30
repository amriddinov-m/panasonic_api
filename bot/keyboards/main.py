from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_btn():
    kb = [
        [
            KeyboardButton(text='🔙 Главное меню'),
        ],

    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def start_btns():
    kb = [
        [
            KeyboardButton(text='📃 Шаблон отчёта'),
            KeyboardButton(text='📤 Выгрузить склад'),
        ],
        [
            KeyboardButton(text='🗂 Прайс каталог'),
        ]

    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                   input_field_placeholder="Выберите что вас именно интересует 👇🏼")
    return keyboard


def task_btns():
    kb = [
        [
            KeyboardButton(text='📌 Создать поручение'),
        ],
        [
            KeyboardButton(text='🗓 Просроченные поручения'),
            KeyboardButton(text='📌 Мои поручения'),
        ],
        [
            KeyboardButton(text='🔙 Главное меню'),
        ],

    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                   input_field_placeholder="Выберите что вас именно интересует 👇🏼")
    return keyboard


def director_lot_btns():
    kb = [
        [
            KeyboardButton(text='📃 Создать лот'),
        ],
        [
            KeyboardButton(text='📃 Поиск по лоту'),
        ],
        [
            KeyboardButton(text='🔙 Главное меню'),
        ],

    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                   input_field_placeholder="Выберите что вас именно интересует 👇🏼")
    return keyboard


def lot_btns():
    kb = [
        [
            KeyboardButton(text='📃 Мои лоты'),
        ],
        [
            KeyboardButton(text='📃 Поиск по лоту'),
        ],
        [
            KeyboardButton(text='🔙 Главное меню'),
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                   input_field_placeholder="Выберите что вас именно интересует 👇🏼")
    return keyboard


def lot_detail_btn(lot_id, is_show_report_btn):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="📃 Отправить отчет", callback_data=f"lot-send-report_{lot_id}"),
    )
    if is_show_report_btn:
        builder.row(
            types.InlineKeyboardButton(text="📃 Выгрузка отчета", callback_data=f"lot-export-data_{lot_id}"),
        )
    builder.row(
        types.InlineKeyboardButton(text=f'🔄 Отправить дальше', callback_data=f"lot-change-status_{lot_id}"),
    )


    return builder.as_markup()


def phone_btns():
    kb = [
        [
            KeyboardButton(text="📱 Поделиться номером телефона", request_contact=True),
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                   input_field_placeholder="Поделитесь своим контактом для авторизации 👇🏼")
    return keyboard


def inline_btns(qs, callback_data):
    builder = InlineKeyboardBuilder()
    for obj in qs:
        builder.row(
            types.InlineKeyboardButton(
                text=f'{obj}',
                callback_data=f'{callback_data}{obj.pk}')
        )
    return builder.as_markup()

