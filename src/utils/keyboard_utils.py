from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_cancel_button():
    return InlineKeyboardButton(text="❌ Отмена", callback_data="CANCEL")

def get_cancel_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [get_cancel_button()]
        ]
    )