from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ForceReply
from config import ADMIN_ID, ADMIN_IDS
from database.models import get_applications, get_application, update_application_status, delete_application
from keyboards.admin import admin_menu_kb

router = Router()

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

@router.message(Command("menu"))
async def admin_menu(message: Message):
    """Показать админ-меню"""
    if not is_admin(message.from_user.id):
        return
    await message.answer("Админ-панель:", reply_markup=admin_menu_kb())

@router.message(Command("list"))
async def list_applications(message: Message):
    if not is_admin(message.from_user.id):
        return
    apps = await get_applications()
    if not apps:
        await message.answer("Заявок нет.")
        return
    text = "Список заявок:\n"
    for app in apps:
        text += f"ID: {app[0]}, ФИО: {app[2]}, Статус: {app[8]}\n"
    await message.answer(text)

@router.message(F.text == "Просмотр заявки")
async def ask_view_id(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("Введите ID заявки для просмотра:", reply_markup=ForceReply())

@router.message(F.text == "Отметить просмотренной")
async def ask_mark_id(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("Введите ID заявки для отметки как просмотренной:", reply_markup=ForceReply())

@router.message(F.text == "Удалить заявку")
async def ask_delete_id(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("Введите ID заявки для удаления:", reply_markup=ForceReply())

@router.message(F.reply_to_message, F.reply_to_message.text == "Введите ID заявки для просмотра:")
async def view_application_reply(message: Message):
    if not is_admin(message.from_user.id):
        return
    try:
        app_id = int(message.text)
        app = await get_application(app_id)
        if not app:
            await message.answer("Заявка не найдена.")
            return
        text = (
            f"ID: {app[0]}\nФИО: {app[2]}\nEmail: {app[3]}\nТелефон: {app[4]}\n"
            f"Навыки: {app[5]}\nПортфолио: {app[6]}\nДата: {app[8]}\nСтатус: {app[9]}"
        )
        await message.answer(text)
    except Exception:
        await message.answer("Ошибка при просмотре заявки.")

@router.message(F.reply_to_message, F.reply_to_message.text == "Введите ID заявки для отметки как просмотренной:")
async def mark_viewed_reply(message: Message):
    if not is_admin(message.from_user.id):
        return
    try:
        app_id = int(message.text)
        await update_application_status(app_id, 'viewed')
        await message.answer("Заявка отмечена как просмотренная.")
    except Exception:
        await message.answer("Ошибка при обновлении статуса.")

@router.message(F.reply_to_message, F.reply_to_message.text == "Введите ID заявки для удаления:")
async def delete_app_reply(message: Message):
    if not is_admin(message.from_user.id):
        return
    try:
        app_id = int(message.text)
        await delete_application(app_id)
        await message.answer("Заявка удалена.")
    except Exception:
        await message.answer("Ошибка при удалении заявки.") 