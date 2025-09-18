from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from structlog import get_logger

from src.constants.menu import ACTIVITY_BUTTON
from src.services import ActivityService

router = Router()

class ActivityState(StatesGroup):
    selecting_activity = State()
    manage_activity = State()
    confirming_action = State()

@router.message(Command("activity"))
@router.message(F.text == ACTIVITY_BUTTON)
async def activity_handler(message: Message, state: FSMContext, activity_service: ActivityService):
    get_logger().info("Handled activity command")

    activities = await activity_service.get_activities()
    buttons = []
    for activity in activities:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=activity.name,
                    callback_data=f"activity:{activity.id}"
                )
            ]
        )

    text = "Выбери активность для работы:"

    await state.set_state(ActivityState.selecting_activity)
    await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))


@router.callback_query(F.data.startswith("activity:"), ActivityState.selecting_activity)
async def select_activity_handler(callback_query: CallbackQuery, state: FSMContext, activity_service: ActivityService):
    await callback_query.answer("")
    activity_id = callback_query.data.split(":")[1]

    get_logger().info("Handled activity selection, activity id: %s", activity_id)

    await callback_query.message.edit_text("Выбрана активность: " + activity_id, reply_markup=None)
    await state.set_state(ActivityState.manage_activity)
