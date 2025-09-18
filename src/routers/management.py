from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from structlog import get_logger

from src.constants.menu import CONFERENCE_MANAGEMENT_BUTTON
from src.constants.messages import MANAGE_COMMAND_TEXT, MANAGE_GENERATE_AUTH_CODE_TEXT
from src.services import AuthService
from src.utils.keyboard_utils import get_cancel_button, get_cancel_keyboard

router = Router()

class ManagementState(StatesGroup):
    input_code_count = State()
    confirm_end_conference = State()


@router.message(Command("manage"))
@router.message(F.text == CONFERENCE_MANAGEMENT_BUTTON)
async def conference_management(message: Message, auth_service: AuthService):
    get_logger().info("Handled conference_management command")
    if not await auth_service.is_admin(message.from_user.id):
        await message.answer(
            "У вас нет прав на управление конференцией",
        )
        return

    keyboard = [
        [InlineKeyboardButton(text="📱 Сгенерировать коды для волонтеров", callback_data="generate_auth_codes")],
        [InlineKeyboardButton(text="⚠️ Завершить конференцию", callback_data="finish_conference")],
        [get_cancel_button()]
    ]

    await message.answer(MANAGE_COMMAND_TEXT, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))

@router.callback_query(F.data == "finish_conference")
async def finish_conference(callback_query: CallbackQuery):
    get_logger().info("Handled finish_conference callback query")
    pass

@router.callback_query(F.data == "generate_auth_codes")
async def generate_auth_codes(callback_query: CallbackQuery, state: FSMContext):
    get_logger().info("Handled generate_auth_codes callback query")
    await callback_query.answer("")

    await callback_query.message.edit_text(MANAGE_GENERATE_AUTH_CODE_TEXT, reply_markup=get_cancel_keyboard())
    await state.set_state(ManagementState.input_code_count)

@router.message(ManagementState.input_code_count)
async def input_code_count(message: Message, state: FSMContext, auth_service: AuthService):
    get_logger().info("Handled input_code_count message")
    if message.text.isdigit():
        count = int(message.text)
        if count > 0:
            get_logger().info(f"Generating {count} auth codes")
            codes = await auth_service.generate_codes(count)
            codes_str = "\n".join(list(map(lambda x: f"`{x}`", codes)))

            await message.answer(
                f"Сгенерированные коды:\n\n{codes_str}",
            )
            await state.clear()

        else:
            get_logger().info("Handle invalid count")
            await message.answer(
                "Количество должно быть больше 0",
                reply_markup=get_cancel_keyboard()
            )
    else:
        get_logger().info("Handle invalid format of count")
        await message.answer(
            "Количество должно быть числом",
            reply_markup=get_cancel_keyboard()
        )



