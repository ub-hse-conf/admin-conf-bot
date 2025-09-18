from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.config import MINI_APP_URL, SCANNER_LOGIN_API, SCANNER_PASSWORD_API
from src.constants.menu import SCANNER_BUTTON
from src.constants.messages import SCANNER_TEXT

router = Router()


@router.message(Command("scanner"))
@router.message(F.text == SCANNER_BUTTON)
async def cmd_scanner(message: Message, state: FSMContext) -> None:
    keyboard = get_mini_app_keyboard()
    bot_message = await message.answer(
        text=SCANNER_TEXT,
        reply_markup=keyboard
    )
    await state.update_data(info_message_id=bot_message.message_id)


def get_mini_app_keyboard():
    builder = InlineKeyboardBuilder()
    url = MINI_APP_URL + f"?login={SCANNER_LOGIN_API}&password={SCANNER_PASSWORD_API}"
    builder.add(
        InlineKeyboardButton(
            web_app=WebAppInfo(
                url=f"{url}"
            ),
            text="Сканнер"
        ),
    )
    builder.adjust(2)
    return builder.as_markup()
