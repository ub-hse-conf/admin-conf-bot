from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from structlog import get_logger

from src.constants.menu import ACTIVITY_BUTTON
from src.models import ActivityType, ActivityEventStatus
from src.services import ActivityService
from src.utils.keyboard_utils import get_cancel_button

router = Router()

class ActivityState(StatesGroup):
    copy_visits = State()

@router.message(Command("activity"))
@router.message(F.text == ACTIVITY_BUTTON)
async def activity_handler(message: Message, activity_service: ActivityService):
    get_logger().info("Handled activity command")

    activities = await activity_service.get_activities()
    buttons = []
    for activity in activities:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{get_event_emoji_or_nothing(activity.has_event)}{activity.name} {activity.start_time}-{activity.end_time}",
                    callback_data=f"activity:{activity.id}"
                )
            ]
        )

    buttons.append([get_cancel_button()])

    text = "Выбери активность для работы:"

    await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))


@router.callback_query(F.data == "activity_back")
async def back_handler(query: CallbackQuery, activity_service: ActivityService):
    get_logger().info("Handled activity back")
    await query.answer("")

    activities = await activity_service.get_activities()
    buttons = []
    for activity in activities:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{get_event_emoji_or_nothing(activity.has_event)}{activity.name} {activity.start_time}-{activity.end_time}",
                    callback_data=f"activity:{activity.id}"
                )
            ]
        )

    buttons.append([get_cancel_button()])

    text = "Выбери активность для работы:"

    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

def get_event_emoji_or_nothing(has_event: bool) -> str:
    if has_event:
        return "▶️ "
    else:
        return ""


@router.callback_query(F.data.startswith("activity:"))
async def select_activity_handler(callback_query: CallbackQuery, state: FSMContext, activity_service: ActivityService):
    await callback_query.answer("")
    activity_id = int(callback_query.data.split(":")[1])

    get_logger().info("Handled activity selection, activity id: %d", activity_id)

    activity = await activity_service.get_activity(activity_id)
    event = None if not activity.has_event else await activity_service.get_activity_event(activity_id)

    prefix = "" if activity.activity_type == ActivityType.CONTEST else activity.activity_type.value + " "
    text = (
        f"*{prefix}{activity.name}*\n"
        f"{activity.location}, {activity.start_time}-{activity.end_time}\n\n"
        f"{activity.description}"
    )

    buttons = [
        [InlineKeyboardButton(text="📝 Скопировать посещения", callback_data=f"activity_visits_copy:{activity_id}")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="activity_back")],
    ]

    if event:
        status = ""
        match event.status:
            case ActivityEventStatus.PREPARED:
                buttons.insert(0, [InlineKeyboardButton(text="▶️ Запустить ивент", callback_data=f"activity_start:{activity_id}")])
                status = "🔑 Готов к запуску"
            case ActivityEventStatus.CONTINUED:
                buttons.insert(0, [InlineKeyboardButton(text="⏹️ Завершить ивент", callback_data=f"activity_end:{activity_id}")],)
                status = "⏳ Запущен"
            case ActivityEventStatus.ENDED:
                status = "✅ Завершен"

        duration_text = "" if not event.duration else f"Продолжительность: {event.duration.seconds // 60} мин.\n"
        event_text = (
            f"Событие: {event.name}\n"
            f"{duration_text}"
            f"Статус: {status}"
        )

        text += "\n\n" + event_text

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback_query.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("activity_start:"))
async def start_confirmation_activity_handler(callback_query: CallbackQuery, activity_service: ActivityService):
    id = int(callback_query.data.split(":")[1])
    get_logger().info("Handled activity start confirmation for id: %d", id)

    event = await activity_service.get_activity_event(id)

    await callback_query.answer("Вы собираетесь запустить ивент. Подтвердите действие.", show_alert=True)

    text = (
        "*Подтверждение*\n"
        f"Вы собираетесь запустить ивент *{event.name}*"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"activity_start_confirm:{id}")],
            [get_cancel_button()],
        ]
    )

    await callback_query.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("activity_start_confirm:"))
async def start_activity_handler(callback_query: CallbackQuery, activity_service: ActivityService):
    id = int(callback_query.data.split(":")[1])
    get_logger().info("Handled activity start for id: %d", id)

    await activity_service.run_activity_event(id)
    await callback_query.message.delete()
    await callback_query.answer("Вы успешно запустили ивент")


@router.callback_query(F.data.startswith("activity_end:"))
async def end_confirmation_activity_handler(callback_query: CallbackQuery, activity_service: ActivityService):
    id = int(callback_query.data.split(":")[1])
    get_logger().info("Handled activity end confirmation for id: %d", id)

    event = await activity_service.get_activity_event(id)

    await callback_query.answer("Вы собираетесь завершить ивент. Подтвердите действие.", show_alert=True)

    text = (
        "*Подтверждение*\n"
        f"Вы собираетесь завершить ивент *{event.name}*"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"activity_end_confirm:{id}")],
            [get_cancel_button()],
        ]
    )

    await callback_query.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("activity_end_confirm:"))
async def end_activity_handler(callback_query: CallbackQuery, activity_service: ActivityService):
    id = int(callback_query.data.split(":")[1])
    get_logger().info("Handled activity end for id: %d", id)

    await activity_service.stop_activity_event(id)
    await callback_query.message.delete()
    await callback_query.answer("Вы успешно завершили ивент")


@router.callback_query(F.data.startswith("activity_visits_copy:"))
async def copy_visits_handler(query: CallbackQuery, state: FSMContext, activity_service: ActivityService):
    await query.answer("")
    await state.set_state(ActivityState.copy_visits)
    await state.update_data(activity_id=query.data.split(":")[1])

    get_logger().info("Handled start activity visits copy for id: %s", query.data.split(":")[1])

    activities = await activity_service.get_activities()
    buttons = []
    for activity in activities:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{get_event_emoji_or_nothing(activity.has_event)}{activity.name} {activity.start_time}-{activity.end_time}",
                    callback_data=f"activity_visits_copy_activity:{activity.id}"
                )
            ]
        )

    buttons.append([get_cancel_button()])

    text = "Выберите активность куда вы хотите скопировать посещения:"

    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))


@router.callback_query(F.data.startswith("activity_visits_copy_activity:"), ActivityState.copy_visits)
async def copy_visits_activity_confirmation_handler(query: CallbackQuery, state: FSMContext, activity_service: ActivityService):
    data = await state.get_data()
    from_activity_id = int(data["activity_id"])
    to_activity_id = int(query.data.split(":")[1])

    get_logger().info("Handled activity visits copy confirmation from %d to %d", from_activity_id, to_activity_id)

    from_activity = await activity_service.get_activity(from_activity_id)
    to_activity = await activity_service.get_activity(to_activity_id)

    text = (
        f"Вы собираетесь скопировать посещения из активности *{from_activity.name}* в активность *{to_activity.name}*.\n"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"activity_visits_copy_confirm:{from_activity_id}:{to_activity_id}")],
            [get_cancel_button()],
        ]
    )

    await query.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("activity_visits_copy_confirm"))
async def copy_visits_activity_handler(query: CallbackQuery, state: FSMContext, activity_service: ActivityService):
    from_activity_id, to_activity_id = query.data.split(":")[1:]
    get_logger().info("Handled activity visits copy from %d to %d", int(from_activity_id), int(to_activity_id))

    await activity_service.copy_activity_visits(int(from_activity_id), int(to_activity_id))
    await query.answer("Вы успешно скопировали посещения")
    await query.message.delete()
    await state.clear()

