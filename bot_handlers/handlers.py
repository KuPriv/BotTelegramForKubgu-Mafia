import asyncio
import os
import random
import sqlite3
import pandas as pd
from dotenv import load_dotenv

from aiogram import Bot, types, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.filters.chat_member_updated import (
    ChatMemberUpdatedFilter,
    IS_NOT_MEMBER,
    MEMBER,
)
from aiogram.types import FSInputFile, URLInputFile

from long_strings_for_handlers import shuti_text, arabic_symbols, china_text

# загрузка секретов из .env
# Так же было бы славно перевести везде в капс.
load_dotenv()
token = os.getenv("TOKEN")
my_id = os.getenv("MY_ID")
chat_id = os.getenv("CHAT_ID")

bot = Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
router = Router()


@router.chat_join_request()
async def handle_join_request(message: types.Message):
    try:
        print("dp.chat_join_request()")
        print(f"comeback israil {message.from_user.username}")
        await bot.approve_chat_join_request(
            chat_id=message.chat.id, user_id=message.from_user.id
        )
        photo_hello = FSInputFile(
            "../photos_and_videos/png_for_functions_handlers/1.jpg",
            filename="danya nozh",
        )
        await asyncio.sleep(2)
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo_hello,
            caption="ДАНЯ НОЖ ПРИВЕТСТВУЕТ ВАС",
        )
    except Exception as e:
        print(f"Произошла ошибка: {e}")


@router.chat_member(ChatMemberUpdatedFilter(MEMBER >> IS_NOT_MEMBER))
async def handle_invite_request(message: types.Message):
    print("dp.chat_member()")
    user_status = await bot.get_chat_member(
        chat_id=message.chat.id, user_id=message.from_user.id
    )
    print(user_status)
    if user_status.status not in ("administrator", "creator"):
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
                    can_pin_messages=True,
                ),
            )
            print("Send.")
            await bot.send_message(
                message.from_user.id,
                f'<a href="https://t.me/mafiaKUBGU">В пизду я бы не заходил сюда</a> ',
                parse_mode="HTML",
            )
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")


@router.message(Command("accepted"))
async def misha_house(message: types.Message):
    with sqlite3.connect("../db/mafiadb.db") as con:
        with con.cursor() as cur:
            sql = """\
            SELECT * FROM perm_ids WHERE complete = 1
            """
            try:
                cur.execute(sql)
                mas = cur.fetchall()
                ids = []
                usernames = []
                for i in range(len(mas)):
                    ids.append(mas[i][0])
                for i in range(len(mas)):
                    usernames.append(mas[i][1])
                s = """"""
                for i in range(len(ids)):
                    if ids[i] != 1239883887:
                        s += f'<a href="tg://user?id={ids[i]}"> {usernames[i]}</a>\n'
                print(s)
                await message.answer(
                    text=f"Список людей допущенных до квартирника у марки:\n {s}"
                    f" В черном списке: Никого",
                    parse_mode="HTML",
                )
            except sqlite3.DatabaseError as err:
                print("Ошибка:", err)
            else:
                print("Успешно.")


@router.message(Command("tag"))
async def who_did_test(message: types.Message):
    with sqlite3.connect("../db/mafiadb.db") as con:
        with con.cursor() as cur:
            sql = """\
                SELECT * FROM perm_ids
                """
            try:
                print(1)
                cur.execute(sql)
                mas = cur.fetchall()
                ids = []
                usernames = []
                for i in range(len(mas)):
                    ids.append(mas[i][0])
                for i in range(len(mas)):
                    usernames.append(mas[i][1])
                print(ids)
                print(usernames)
                index = 0
                for i in range(int((len(ids) / 5)) + 1):
                    s = """"""
                    if len(ids) - (i * 5) >= 5:
                        for j in range(5):
                            s += f'<a href="tg://user?id={ids[(i * 5) + j]}"> {usernames[(i * 5) + j]}</a> '
                            print(ids[(i * 5) + j], usernames[(i * 5) + j])
                    else:
                        for j in range(len(ids) - (i * 5)):
                            s += f'<a href="tg://user?id={ids[(i * 5) + j]}"> {usernames[(i * 5) + j]}</a> '
                            print(ids[(i * 5) + j], usernames[(i * 5) + j])
                    await message.answer(text=s, parse_mode="HTML")

            except sqlite3.DatabaseError as err:
                print("Ошибка:", err)
            else:
                print("Успешно.")


@router.message(Command("bye22"))
async def ban_me(message: types.Message):
    await bot.ban_chat_member(chat_id=message.chat.id, user_id=my_id)
    print("Handled command 'bye'")


@router.message(Command("silly"))
async def us(message: types.Message):
    directory = "png_for_bot/"
    files = os.listdir(directory)
    file: str = directory + random.choice(files)
    agenda = FSInputFile(path=file, filename="попка дурак")
    await message.answer("/silly dlya ne silly")
    await bot.send_photo(chat_id=message.chat.id, photo=agenda)


@router.message(Command("maf"))
async def us(message: types.Message):
    await bot.send_message(
        chat_id="6643633703", text="ти педик бугагаг (я твое сообщени не вижу)"
    )


@router.message(Command("send_danya"))
async def us(message: types.Message):
    agenda = FSInputFile(
        path="../photos_and_videos/png_for_functions_handlers/1.jpg", filename="1.jpg"
    )
    await bot.send_photo(chat_id=message.chat.id, photo=agenda)


@router.message(Command("send_sobak"))
async def us2(message: types.Message):
    agenda = FSInputFile(
        path="../photos_and_videos/png_for_functions_handlers/sobak.png",
        filename="sobak.png",
    )
    await bot.send_photo(chat_id=chat_id, photo=agenda)


@router.message(Command("yupi"))
async def tronula(message: types.Message):
    video_url = "https://youtu.be/aMGa4993ohc?si=916kDHHCoLb1F1Lk"
    await message.answer(f"мозг юпи при поиске мафов чееек: {video_url}")


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
            can_pin_messages=True,
        ),
    )


@router.message(Command("song"))
async def send_songs(message: types.Message):
    # audio = FSInputFile('nervy-kofe-mojj-drug.mp3')
    # await bot.send_audio(message.chat.id, audio)
    audio_file = URLInputFile(
        "https://muzwild.net/upload_file/66a2c65973e986.43660759.mp3",
        filename="sirop.mp3",
    )
    await message.answer_audio(audio=audio_file)
    await asyncio.sleep(1)
    await message.answer(
        "Мои Supreme трусы испачканы в сиропе\n"
        "А всё из-за того, что штаны спущены до жопы"
    )
    # await message.answer("Нервы ура!")


@router.message(Command("shuti_lock"))
async def send_songs(message: types.Message):
    href = "https://dl3s2.muzofond.fm/aHR0cDovL2YubXAzcG9pc2submV0L21wMy8wMDAvNjQ2LzMwMS82NDYzMDEubXAz"
    audio_file = URLInputFile(url=href, filename="shuti.mp3")
    await message.answer_audio(audio=audio_file)
    await asyncio.sleep(1)
    await message.answer(shuti_text)


@router.message(Command("clean"))
async def clean_bot_messages(message: types.Message):
    lis = []
    await bot.delete_messages(chat_id=message.chat.id, message_ids=lis)


@router.message(Command("test_info"))
async def clean_bot_messages(message: types.Message):
    await message.answer(
        "КРУТОЙ ТЕСТ УЖЕ ПРЯМО У МЕНЯ В ЛИЧКЕ!!! ПИШИ МНЕ КОМАНДУ /start В ЛС"
    )


@router.message(Command("makima"))
async def best_func(message: types.Message):
    await bot.send_message(
        chat_id=813252640,
        text=f"Я тебя люблю!!! вызвал: {message.from_user.first_name}",
    )


@router.message(lambda message: "развод" in message.text.lower())
async def same(message: types.Message):
    users_id = ("1798427554", "1049132960")
    if str(message.from_user.id) in users_id:
        print("Ya tut")
        await asyncio.sleep(3)
        s1 = f'<a href="tg://user?id=1798427554"> @Shiro0ri </a>'
        s2 = f'<a href="tg://user?id=1049132960">@bezvreda1</a>'
        s = "поженить пару" + s1 + s2
        await message.answer(s, parse_mode="HTML")


@router.message(Command("nasrek"))
async def best_func(message: types.Message):
    video = FSInputFile(
        "../photos_and_videos/videos_and_memes/narek.MOV", filename="NASREK"
    )
    await bot.send_video(message.chat.id, video)


@router.message(Command("fermer"))
async def best_func(message: types.Message):
    await message.answer("Фарма")


@router.message(lambda message: "с др" in message.text.lower())
async def same(message: types.Message):
    await message.answer("От души )")


@router.message(Command("iris"))
async def best_func(message: types.Message):
    await message.answer("Ирис пидорас.")


@router.message(Command("pigeon"))
async def same3(message: types.Message):
    with sqlite3.connect("../db/mafiadb.db") as con:
        with con.cursor() as cur:
            try:
                sql = """\
                SELECT * from perm_ids
                """
                cur.execute(sql)
                mas = cur.fetchall()
                ids = []
                usernames = []
                for i in range(len(mas)):
                    ids.append(mas[i][0])
                for i in range(len(mas)):
                    usernames.append(mas[i][1])
                index = random.randint(0, len(ids) - 1)
            except sqlite3.DatabaseError as err:
                print("Ошибка:", err)
            else:
                print("Успешно.")
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=f'<a href="tg://user?id={ids[index]}">{usernames[index]}</a> ВАДИМ У ТЕБЯ БУДИЛЬНИК ХУЯРИТ АЛО ВАДИМ ПОСМОТРИ ЛС АЛО ЕБЛАААААААААН',
                    parse_mode="HTML",
                )
                await bot.send_message(chat_id=ids[index], text=arabic_symbols)


@router.message(Command("china"))
async def talk_about_china(message: types.Message):
    await message.answer(china_text)


@router.message(Command("musor"))
async def qw(message: types.Message):
    await message.answer(chat_id="-1002019000148", text="ХИХИХИ ТЫ ТАКОЙ МИЛИИИ ИРИС")


@router.message(Command("weather"))
async def krasniyday(message: types.Message):
    df = pd.read_html(
        "https://rp5.ru/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B4%D0%B0%D1%80%D0%B5,_%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B4%D0%B0%D1%80%D1%81%D0%BA%D0%B8%D0%B9_%D0%BA%D1%80%D0%B0%D0%B9"
    )
    print(df[8][0:10])
