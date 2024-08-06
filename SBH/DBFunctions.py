from Config import DB
from datetime import datetime, timezone


async def add_new_user(user_id):
    async with DB() as conn:
        await conn.execute('''
                INSERT INTO users (id, created_at, status, status_updated_at)
                VALUES ($1, $2, 'alive', $2)
                ON CONFLICT (id) DO NOTHING
            ''', user_id, datetime.now(timezone.utc).replace(microsecond=0))


async def status_change(user_id, status):
    async with DB() as conn:
        await conn.execute('''
            UPDATE users SET status = $2,
            status_updated_at = $3
            WHERE id = $1
        ''', user_id, status, datetime.now(timezone.utc).replace(microsecond=0))


async def get_last_time(user_id):
    async with DB() as conn:
        last_time = await conn.fetchval('SELECT last_message_sent_at FROM users WHERE id = $1', user_id)
        if not last_time:
            last_time = await conn.fetchval('SELECT created_at FROM users WHERE id = $1', user_id)
    return last_time


async def time_change(user_id):
    async with DB() as conn:
        await conn.execute('''
            UPDATE users SET last_message_sent_at = $2
            WHERE id = $1
        ''', user_id, datetime.now(timezone.utc).replace(microsecond=0))


async def get_users():
    async with DB() as conn:
        users_info = await conn.fetch('SELECT id, messages_sent FROM users WHERE status = $1', 'alive')
    return users_info


async def increment_message_count(user_id):
    async with DB() as conn:
        await conn.execute('UPDATE users SET messages_sent = messages_sent + 1 WHERE id = $1', user_id)


async def user_reset(user_id):
    async with DB() as conn:
        await conn.execute('''
                    UPDATE users SET status = 'alive', messages_sent = 0,
                    status_updated_at = $2, last_message_sent_at = NULL,
                    created_at = $2 WHERE id = $1
                ''', user_id, datetime.now(timezone.utc).replace(microsecond=0))
