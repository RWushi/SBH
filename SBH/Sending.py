from Config import app
from DBFunctions import status_change, get_last_time, time_change, get_users, increment_message_count, user_reset
from datetime import datetime, timezone


async def check_triggers(user_id):
    try:
        async for message in app.get_chat_history(user_id):
            if message.text and message.outgoing:
                text = message.text.lower()
                if any(trigger in text for trigger in ["прекрасно", "ожидать"]):
                    await status_change(user_id, 'finished')
                    return True
    except Exception:
        await status_change(user_id, 'dead')
        return True

    return False


async def send_scheduled_message(user_id, text, interval):
    last_time = await get_last_time(user_id)
    if last_time:
        current_time = datetime.now(timezone.utc).replace(microsecond=0)
        if (current_time - last_time).total_seconds() >= interval:
            if not await check_triggers(user_id):
                await app.send_message(user_id, text)
                await time_change(user_id)
                await increment_message_count(user_id)


async def check_scheduled_messages():
    users = await get_users()
    for user in users:
        user_id = user['id']
        messages_sent = user['messages_sent']
        if messages_sent == 0:
            await send_scheduled_message(user_id, 'Текст1', 6 * 60)
        if messages_sent == 1:
            await send_scheduled_message(user_id, 'Текст2', 45 * 60)
        if messages_sent == 2:
            await send_scheduled_message(user_id, 'Текст3', (24 * 60 * 60) + (2 * 60 * 60))
