import aiosqlite
from config import DB_PATH

async def add_application(user_id, full_name, email, phone, skills, portfolio=None, resume_file_id=None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            INSERT INTO applications (user_id, full_name, email, phone, skills, portfolio, resume_file_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, full_name, email, phone, skills, portfolio, resume_file_id))
        await db.commit()

async def get_applications(status=None):
    async with aiosqlite.connect(DB_PATH) as db:
        if status:
            cursor = await db.execute('SELECT * FROM applications WHERE status = ? ORDER BY created_at DESC', (status,))
        else:
            cursor = await db.execute('SELECT * FROM applications ORDER BY created_at DESC')
        return await cursor.fetchall()

async def get_application(app_id):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute('SELECT * FROM applications WHERE id = ?', (app_id,))
        return await cursor.fetchone()

async def update_application_status(app_id, status):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('UPDATE applications SET status = ? WHERE id = ?', (status, app_id))
        await db.commit()

async def delete_application(app_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('DELETE FROM applications WHERE id = ?', (app_id,))
        await db.commit() 