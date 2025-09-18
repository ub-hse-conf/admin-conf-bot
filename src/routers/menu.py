from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from src.constants.menu import SCANNER_BUTTON, ACTIVITY_BUTTON, BE_REAL_BUTTON, CONFERENCE_MANAGEMENT_BUTTON


def generate_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=SCANNER_BUTTON)],
            [KeyboardButton(text=ACTIVITY_BUTTON), KeyboardButton(text=BE_REAL_BUTTON)],
            [KeyboardButton(text=CONFERENCE_MANAGEMENT_BUTTON)],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберете пункт из меню ниже"
    )



