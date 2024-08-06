#В своих проектах я всегда оставляю файл с тестами, для того чтобы тестировать проблемные места кода
from Config import DB
from datetime import datetime, timezone
import asyncio


async def user_reset():
    async with DB() as conn:
        await conn.execute('''
                    INSERT INTO users (id, status_updated_at, created_at)
                    VALUES ($1, $2, $2)
                    ''', 1, datetime.now(timezone.utc))

asyncio.run(user_reset())