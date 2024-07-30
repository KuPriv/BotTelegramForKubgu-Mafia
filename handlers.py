import asyncio

from aiogram import Bot, types, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER
from aiogram.types import FSInputFile, ChatMemberBanned, ChatMemberRestricted
from config_for_test import token
from config import my_id, chat_id


bot = Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
router = Router()


@router.chat_join_request()
async def handle_join_request(message: types.Message):
    try:
        print("dp.chat_join_request()")
        user_status = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        print(user_status)
        if isinstance(user_status, ChatMemberBanned) or isinstance(user_status, ChatMemberRestricted):
            print('i am called here (unban) in join request')
            try:
                await bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id,
                    permissions=types.ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_polls=True,
                        can_send_other_messages=True,
                        can_add_web_page_previews=True,
                        can_invite_users=True,
                        can_pin_messages=True
                    )
                )
            except Exception as e:
                await message.reply(f"Произошла ошибка: {e}")
        print(f"comeback israil {message.from_user.username}")
        await bot.approve_chat_join_request(chat_id=message.chat.id, user_id=message.from_user.id)
        #gif = FSInputFile("greeting.gif", filename="greeting.gif")
        await asyncio.sleep(2)
        await bot.send_message(chat_id=message.chat.id, text=f'Приветствуем сектанта: <a href="tg://user?{message.from_user.id}">{message.from_user.username}</a>')
        #await bot.send_animation(chat_id=message.chat.id, animation=gif)
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")


@router.chat_member()
async def handle_invite_request(message: types.Message):
    print("dp.chat_member()")
    user_status = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    print(user_status)
    if isinstance(user_status, ChatMemberBanned):
        print('i am called here (unban)')
        try:
            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=message.from_user.id,
                permissions=types.ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_polls=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_invite_users=True,
                    can_pin_messages=True
                )
            )
        except Exception as e:
            await message.reply(f"Произошла ошибка: {e}")
        try:
            await bot.send_message(message.from_user.id, f'<a href="https://t.me/mafiaKUBGU">В пизду я бы не заходил сюда</a> ', parse_mode='HTML')
        except Exception as e:
            await message.reply(f"Произошла ошибка: {e}")


@router.message(Command("bye"))
async def ban_me(message: types.Message):
    await bot.ban_chat_member(chat_id=message.chat.id, user_id=my_id)
    print("Handled command 'bye'")
    """await bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=my_id,
        permissions=types.ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_invite_users=True,
            can_pin_messages=True
        )
    )"""


@router.message(Command("hi"))
async def unban_user(message: types.Message):
    print("Handled command 'hi'")
    await bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=my_id,
        permissions=types.ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_invite_users=True,
            can_pin_messages=True
        )
    )