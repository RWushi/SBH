import asyncio
import threading
from Config import app
from DBFunctions import add_new_user, user_reset
from Sending import check_scheduled_messages
from pyrogram import filters, types


async def delete_stop_messages(user_id, keywords):
    async for message in app.get_chat_history(user_id):
        if message.text and any(keyword in message.text.lower() for keyword in keywords):
            await message.delete()


@app.on_message(filters.private)
async def first_message(client, message: types.Message):
    user_id = message.from_user.id
    text = message.text.lower()

    if user_id != client.me.id:
        await add_new_user(user_id)
    elif user_id == client.me.id and text == "рестарт":
        chat_partner_id = message.chat.id
        await user_reset(chat_partner_id)
        await message.delete()
        await delete_stop_messages(chat_partner_id, ["прекрасно", "ожидать"])


async def periodic_check():
    await asyncio.sleep(15)
    while True:
        await check_scheduled_messages()
        await asyncio.sleep(15)


def run_periodic_check():
    asyncio.run(periodic_check())


def start():
    periodic_thread = threading.Thread(target=run_periodic_check)
    periodic_thread.start()

    app.run()


if __name__ == '__main__':
    start()
