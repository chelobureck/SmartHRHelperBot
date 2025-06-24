"""
Конфигурация проекта: все переменные берутся из .env
"""
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

BOT_TOKEN: str = os.getenv('BOT_TOKEN')
ADMIN_IDS: List[int] = [int(x) for x in os.getenv('ADMIN_IDS', str(os.getenv('ADMIN_ID', ''))).split(',') if x.strip()]
DB_PATH: str = os.getenv('DB_PATH', 'database/bot_db.sqlite3')
EXTERNAL_API_KEY: str = os.getenv('EXTERNAL_API_KEY')
SUPPORT_EMAIL: str = os.getenv('SUPPORT_EMAIL', 'example@company.com') 