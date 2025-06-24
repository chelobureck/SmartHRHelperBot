from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboards.user import main_menu_kb, cancel_kb
from utils.validators import is_valid_email, is_valid_phone
from database.models import add_application
from config import ADMIN_IDS, SUPPORT_EMAIL
from aiogram import Bot
import logging

router = Router()

WELCOME_TEXT = (
    "👋 Привет! Я бот-рекрутер SmartHRHelperBot.\n"
    "Я помогу тебе откликнуться на вакансию.\n"
    "Нажми кнопку ниже, чтобы начать!"
)
HELP_TEXT = "ℹ️ Для отклика на вакансию нажмите кнопку 'Откликнуться на вакансию'.\nЕсли возникли вопросы — пишите /support."
CANCEL_TEXT = "Опрос отменён."

def user_info_str(user):
    return (
        f"\n========== Новый пользователь нажал /start =========="
        f"\nID:           {user.id}"
        f"\nUsername:     @{user.username}"
        f"\nИмя:          {user.first_name}"
        f"\nФамилия:      {user.last_name}"
        f"\nЯзык:         {user.language_code}"
        f"\nБот?:         {user.is_bot}"
        f"\nСсылка:       tg://user?id={user.id}"
        f"\nПолный объект: {user}"
        f"\n====================================================\n"
    )

class ApplicationFSM(StatesGroup):
    full_name = State()
    email = State()
    phone = State()
    skills = State()
    portfolio = State()
    resume = State()

@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Обработка команды /start"""
    user = message.from_user
    logging.info(user_info_str(user))
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_kb())

@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Обработка команды /help"""
    await message.answer(HELP_TEXT)

@router.message(Command("support"))
async def cmd_support(message: Message) -> None:
    await message.answer(f"Связь с HR: {SUPPORT_EMAIL}")

@router.message(F.text == "Откликнуться на вакансию")
async def start_application(message: Message, state: FSMContext):
    await state.set_state(ApplicationFSM.full_name)
    await message.answer("Введите ваше ФИО:", reply_markup=cancel_kb())

@router.message(ApplicationFSM.full_name)
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(ApplicationFSM.email)
    await message.answer("Введите ваш email:")

@router.message(ApplicationFSM.email)
async def process_email(message: Message, state: FSMContext):
    if not is_valid_email(message.text):
        await message.answer("❌ Некорректный email. Попробуйте снова:")
        return
    await state.update_data(email=message.text)
    await state.set_state(ApplicationFSM.phone)
    await message.answer("Введите ваш телефон (например, +79991234567):")

@router.message(ApplicationFSM.phone)
async def process_phone(message: Message, state: FSMContext):
    if not is_valid_phone(message.text):
        await message.answer("❌ Некорректный номер. Попробуйте снова:")
        return
    await state.update_data(phone=message.text)
    await state.set_state(ApplicationFSM.skills)
    await message.answer("Опишите ваши ключевые навыки (через запятую):")

@router.message(ApplicationFSM.skills)
async def process_skills(message: Message, state: FSMContext):
    await state.update_data(skills=message.text)
    await state.set_state(ApplicationFSM.portfolio)
    await message.answer("Ссылка на портфолио/резюме (опционально, или напишите -):")

@router.message(ApplicationFSM.portfolio)
async def process_portfolio(message: Message, state: FSMContext):
    portfolio = message.text if message.text != '-' else None
    await state.update_data(portfolio=portfolio)
    await state.set_state(ApplicationFSM.resume)
    await message.answer("Загрузите PDF с резюме (опционально, или напишите -):")

@router.message(ApplicationFSM.resume)
async def process_resume(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    resume_file_id = None
    if message.document and message.document.mime_type == 'application/pdf':
        resume_file_id = message.document.file_id
    elif message.text and message.text != '-':
        await message.answer("Пожалуйста, загрузите PDF-файл или напишите - если не хотите прикладывать резюме.")
        return
    await add_application(
        user_id=message.from_user.id,
        full_name=data['full_name'],
        email=data['email'],
        phone=data['phone'],
        skills=data['skills'],
        portfolio=data.get('portfolio'),
        resume_file_id=resume_file_id
    )
    await state.clear()
    await message.answer("✅ Ваша заявка отправлена! Мы свяжемся с вами.", reply_markup=main_menu_kb())
    # Уведомление админу
    text = f"Новая заявка!\nФИО: {data['full_name']}\nEmail: {data['email']}\nТелефон: {data['phone']}\nНавыки: {data['skills']}"
    for admin_id in ADMIN_IDS:
        await bot.send_message(admin_id, text)

@router.message(F.text == "Отмена")
async def cancel(message: Message, state: FSMContext) -> None:
    """Обработка отмены опроса"""
    await state.clear()
    await message.answer(CANCEL_TEXT, reply_markup=main_menu_kb()) 