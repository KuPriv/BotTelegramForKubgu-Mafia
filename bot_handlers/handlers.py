import asyncio
import os
import random
import logging
import sqlite3
from dotenv import load_dotenv

from aiogram import Bot, types, Router, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.filters.chat_member_updated import (
    ChatMemberUpdatedFilter,
    IS_NOT_MEMBER,
    MEMBER,
)
from aiogram.types import FSInputFile, URLInputFile

from bot_handlers.long_strings_for_handlers import (
    shuti_text,
    arabic_symbols,
    china_text,
)

from faster_whisper import WhisperModel
from pydub import AudioSegment

# загрузка секретов из .env
# Так же было бы славно перевести везде в капс.
load_dotenv()
token = os.getenv("TOKEN")
my_id = os.getenv("MY_ID")
my_id = int(my_id)
chat_id = os.getenv("CHAT_ID")
shiro_id, bezvreda_id, makima_id = (
    os.getenv("shiro_id"),
    os.getenv("bezvreda_id"),
    os.getenv("makima_id"),
)

# Устанавливаю путь до mafiadb.db
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "db", "mafiadb.db")

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


async def get_usernames_list(cur: sqlite3.Cursor) -> tuple:
    logging.warning("Зашли в get_usernames_list")
    mas = cur.fetchall()
    logging.warning("mas: %s", mas)
    ids = []
    usernames = []
    for i in range(len(mas)):
        ids.append(mas[i][0])
    for i in range(len(mas)):
        usernames.append(mas[i][1])
    logging.warning("ids: %s", ids)
    logging.warning("usernames: %s", usernames)
    return ids, usernames, cur


@router.message(Command("accepted"))
async def misha_house(message: types.Message):
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        sql = """\
        SELECT * FROM perm_ids WHERE complete = 1
        """
        try:
            cur.execute(sql)
            ids, usernames, cur = await get_usernames_list(cur)
            s = """"""
            for i in range(len(ids)):
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
        finally:
            cur.close()


@router.message(Command("tag"))
async def who_did_test(message: types.Message):
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        sql = """\
            SELECT * FROM perm_ids
            """
        try:
            cur.execute(sql)
            ids, usernames, cur = await get_usernames_list(cur)
            print(ids)
            print(usernames)
            for i in range(int((len(ids) / 5)) + 1):
                s = """"""
                if len(ids) - (i * 5) >= 5:
                    for j in range(5):
                        s += f'<a href="tg://user?id={ids[(i * 5) + j]}"> {usernames[(i * 5) + j]}</a> '
                else:
                    for j in range(len(ids) - (i * 5)):
                        s += f'<a href="tg://user?id={ids[(i * 5) + j]}"> {usernames[(i * 5) + j]}</a> '
                await message.answer(text=s, parse_mode="HTML")

        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("Успешно.")
        finally:
            cur.close()


@router.message(Command("send_danya"))
async def us(message: types.Message):
    agenda = FSInputFile(
        path="../photos_and_videos/png_for_functions_handlers/1.jpg", filename="1.jpg"
    )
    await bot.send_photo(chat_id=message.chat.id, photo=agenda)


@router.message(Command("send_sobak"))
async def us2():
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
async def unban_user():
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
        chat_id=makima_id,
        text=f"Я тебя люблю!!! вызвал: {message.from_user.first_name}",
    )


@router.message(Command("nasrek"))
async def best_func(message: types.Message):
    video = FSInputFile(
        "../photos_and_videos/videos_and_memes/narek.MOV", filename="NASREK"
    )
    await bot.send_video(message.chat.id, video)


@router.message(Command("fermer"))
async def best_func(message: types.Message):
    await message.answer("Фарма")


@router.message(Command("iris"))
async def best_func(message: types.Message):
    await message.answer("Ирис пидорас.")


@router.message(Command("pigeon"))
async def same3(message: types.Message):
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        try:
            sql = """\
            SELECT * from perm_ids
            """
            cur.execute(sql)
            ids, usernames, cur = await get_usernames_list(cur)
            index = random.randint(0, len(ids) - 1)
        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("Успешно.")
            await bot.send_message(
                chat_id=message.chat.id,
                text=f'<a href="tg://user?id={ids[index]}">{usernames[index]}</a> ВАДИМ У ТЕБЯ БУДИЛЬНИК ХУЯРИТ АЛО '
                f"ВАДИМ ПОСМОТРИ ЛС АЛО ЕБЛАААААААААН",
                parse_mode="HTML",
            )
            await bot.send_message(chat_id=ids[index], text=arabic_symbols)
        finally:
            cur.close()


@router.message(Command("china"))
async def talk_about_china(message: types.Message):
    await message.answer(china_text)


# Установка модели для работы с аудио
model = WhisperModel("base", device="cpu", compute_type="float32", num_workers=1)


@router.message(F.voice)
async def handle_voice(message: types.Message):
    file_info = await message.bot.get_file(message.voice.file_id)
    downloaded = await message.bot.download_file(file_info.file_path)

    ogg_path = f"voice_{message.message_id}.ogg"
    wav_path = ogg_path.replace(".ogg", ".wav")

    with open(ogg_path, "wb") as f:
        f.write(downloaded.getvalue())

    audio = AudioSegment.from_file(ogg_path)

    audio = audio.set_frame_rate(16000)
    audio = audio.set_channels(1)
    audio = audio.normalize()

    audio.export(wav_path, format="wav")

    segments, info = model.transcribe(
        str(wav_path),
        beam_size=5,
        language="ru",
        temperature=0.0,
        compression_ratio_threshold=2.4,
        log_prob_threshold=-1.0,
        no_speech_threshold=0.6,
        initial_prompt="Это голосовое сообщение на русском языке.",
    )

    text_segments = []
    for segment in segments:
        text_segments.append(segment.text.strip())

    final_text = " ".join(text_segments).strip()

    await message.reply(final_text or "Я дебил мдя.")

    os.remove(ogg_path)
    os.remove(wav_path)
