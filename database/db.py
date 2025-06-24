import aiosqlite
from config import DB_PATH

CREATE_APPLICATIONS_TABLE = '''
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    skills TEXT NOT NULL,
    portfolio TEXT,
    resume_file_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'new'
);
'''

async def create_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(CREATE_APPLICATIONS_TABLE)
        await db.commit() 