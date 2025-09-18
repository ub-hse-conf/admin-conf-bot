from multiprocessing.util import get_logger

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from src.constants.menu import BE_REAL_BUTTON
from src.models import BeRealStatus
from src.services import TaskService
from src.utils.keyboard_utils import get_cancel_button

router = Router()

@router.message(F.text == BE_REAL_BUTTON)
@router.message(Command("be_real"))
async def be_real_handler(message: Message, task_service: TaskService):
    get_logger().info("Handled be real handler")
    be_reals = await task_service.get_be_reals()

    text = (
        "Выберите BeReal для запуска:"
    )

    buttons = []

    for be_real in be_reals:
        buttons.append(
            [
                InlineKeyboardButton(text=f"{convert_status_to_emoji(be_real.status)} {be_real.name}", callback_data=f"be_real:{be_real.id}")
            ]
        )

    buttons.append([get_cancel_button()])

    await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))


def convert_status_to_emoji(status: BeRealStatus) -> str:
    return {
        status.READY: "✏️",
        status.IN_PROCESS: "🚀",
        status.FINISHED: "✅",
    }[status]

@router.callback_query(F.data.startswith("be_real:"))
async def be_real_callback_handler(callback_query: Message, task_service: TaskService):
    be_real_id = int(callback_query.data.split(":")[1])
    get_logger().info("Handled be real callback handler for be real id: %d", be_real_id)

    be_real = await task_service.get_be_real(be_real_id)

    if be_real.status != BeRealStatus.READY:
        await callback_query.answer(
            "🚫 BeReal уже завершен или запущен!",
        )
        return

    text = (
        "Вы собираетесь запустить BeReal:\n\n"
        f"📝 Название: {be_real.name}\n"
        f"📅 Время: {be_real.duration.seconds // 60} мин.\n"
        f"Описание: {be_real.description}\n\n"
    )

    buttons = [
        [InlineKeyboardButton(text="🚀 Запустить", callback_data=f"be_real_start:{be_real.id}")],
        [get_cancel_button()]
    ]

    await callback_query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

@router.callback_query(F.data.startswith("be_real_start:"))
async def be_real_start_callback_handler(callback_query: Message, task_service: TaskService):
    id = int(callback_query.data.split(":")[1])
    get_logger().info("Launched be real with id: %d", id)
    await task_service.run_be_real(id)
    await callback_query.answer("🚀 BeReal запущен!")
    await callback_query.message.delete()