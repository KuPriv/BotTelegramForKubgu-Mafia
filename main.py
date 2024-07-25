import asyncio
import logging
import re

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from pyrogram import Client

from config_for_test import token, api_hash, api_id
bot = Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

#game@MafiososBot
"""доделать вызов гея который начал игру
и еще сделать таймер на 5 минут чтоб тегать раз в 5 минут людей"""
@dp.message(Command("nasrek"))
async def get_user_ids(message: types.Message):
    chat = await bot.get_chat(message.chat.id)
    if chat.type in ["supergroup", "group"]:
        s = []
        async with Client("my_account", api_id, api_hash, bot_token=token) as app:
            async for m in app.get_chat_members(message.chat.id):
                s.append(m)
        id_list = re.findall(r'id=\d{9}', str(s))
        #usernames_list = re.findall(r'username=[^\s) ]*', str(s))
        id_list = set(id_list)
        id_list = list(id_list)
        counter = 0
        counter_for_users = 0
        s = ""
        for i in id_list:
            if counter == 5:
                await bot.send_message(message.chat.id, s, parse_mode='HTML')
                s = ''
                counter = 0
            mention = f'<a href="tg://user?{str(i)}">{counter_for_users}</a> '
            s += mention
            print(s)
            counter += 1
            counter_for_users += 1
    if chat.type not in ["supergroup", "group"]:
        result = await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    result = await bot.get_chat_member_count(chat_id=message.chat.id)


"""@dp.message(Command("bb"))
async def get_user_ids(message: types.Message):
    await message.answer('я спать всем пока')
"""

async def main():
    #dp.message.register(cmd_end, Command("end"))
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())