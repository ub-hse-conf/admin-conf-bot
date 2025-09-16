from aiogram import Router, Bot
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from constants.texts import SCANNER_TEXT, FIO_ERROR_TEXT, PROGRAM_CHANGE_TEXT, COURSE_CHANGE_TEXT, EMAIL_CHANGE_TEXT, \
    EMAIL_ERROR_TEXT, RESULT_TEXT, COMMAND_TEXT
from constants.transcription import type_of_program_dict
from middlewares.utils import get_courses_keyboard, get_programs_keyboard, parse_name, send_error_message, \
    is_error_message, remove_error_message, get_registration_result_keyboard, parse_email, get_main_reply_keyboard, \
    get_mini_app_keyboard

router = Router()


@router.message(Command("scanner"))
async def cmd_scanner(message: Message, state: FSMContext) -> None:
    keyboard = get_mini_app_keyboard()
    bot_message = await message.answer(
        text=SCANNER_TEXT,
        reply_markup=keyboard
    )
    await state.update_data(info_message_id=bot_message.message_id)
