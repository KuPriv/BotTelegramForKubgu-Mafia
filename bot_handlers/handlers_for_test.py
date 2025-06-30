import asyncio
import os
import random
import sqlite3
from dotenv import load_dotenv

from aiogram import Bot, types, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command

from aiogram.types import FSInputFile
from config import chat_id
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# выгрузка токена из .env
load_dotenv()
token = os.getenv("TOKEN")

bot = Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
router = Router()

directory = "mafia_photos/"
solutions = {
    "efim.jpg": "Биг Босс в игре",
    "danya.jpg": "Пьешь - не трожь нож",
    "ilya.jpg": "Вуз хуйня, отчисляйся",
    "zayac.jpg": "В игре 7 долбаебов и 3 пиздабола",
    "vlada.jpg": "Играю со вторым игроком",
    "narek.jpg": "Илья ,ты придирок!Я тебе говорю блять ,НбС там был.Я ебу как ?Я свечку рядом с ним не держал.",
    "ivan.jpg": "Главное Алика проиграла",
    "alika.jpg": "Я такая пикми",
    "misha.jpg": "Салютик",
    "bezv.jpg": "ЭТО ПОЛОМАННАЯ ИГРА",
    "sist.jpg": "Я не пью не курю матом не ругаюсь, целка-патриот",
    "egor.jpg": "Я красный, пасс",
    "amal.jpg": "Ах ты ж козлина!",
    "maykl.jpg": "Дооооброе утро город, красный игрок мирный житель",
    "nver.jpg": "Хватит меня параноить, я не дон",
    "akbar.jpg": "У нас угадайка, давайте проголосуем по балансу",
    "nafan.jpg": "ОН КРАСНЫЙ ПО ЛИЦУ",
    "lubimka.jpg": "Хорошо, твоя сопля длиннее",
    "miru.jpg": "Теперь я царица за столом",
    "nastya.jpg": "Давайте свергнем Нарека",
    "anarx.jpg": "Вы сегодня на токсик вайбе",
    "sonya.jpg": "Ам-ням ебался",
    "oleg.jpg": "Я крышую нарека",
    "kulik.jpg": "Любовник мидка",
    "midok.jpg": "Разбил у марки всю посуду и зашел в туалет в шкаф",
    "ail.jpg": "ДА Я РЕАЛЬНО ШЕРИФ",
    "wookie.jpg": "Мы имеем право тупить!",
    "nbc.jpg": "Программист пошутил",
}


async def temp_use(message):
    if message.chat.type == "private":
        print("handled temp_use()")
        with sqlite3.connect("../db/mafiadb.db") as con:
            with con.cursor() as cur:
                sql = f"""\
                SELECT * from mafia WHERE id_user = {message.from_user.id}
                """
                try:
                    cur.execute(sql)
                    arr = cur.fetchall()
                    gen = arr[0][2]
                    files = gen.split(" ")
                    ans = arr[0][3]
                    arr_temps: list = ans.split(" ")
                    if arr_temps[0] == "":
                        arr_temps.remove("")
                    if len(arr_temps) != len(files):
                        print(arr_temps)
                        print(files)
                        temp = random.choice(files)
                        while temp in arr_temps:
                            temp = random.choice(files)
                        file = directory + temp
                        arr_temps.append(temp)
                        ans = " ".join(arr_temps)
                        photo = FSInputFile(path=file, filename=temp)
                        await bot.send_photo(chat_id=message.chat.id, photo=photo)
                        if temp != "efim.jpg":
                            await message.answer("Ваши догадки, кто этот покемон???")
                        else:
                            await message.answer("Надеюсь, ты знаешь эту легенду...")
                        builder = ReplyKeyboardBuilder()
                        maybe_solutions = [temp]
                        while len(maybe_solutions) != 4:
                            var = random.choice(files)
                            if var not in maybe_solutions:
                                maybe_solutions.append(var)
                        random.shuffle(maybe_solutions)
                        await message.answer("ВАРИАНТЫ ОТВЕТОВ:")
                        for i in range(1, 5):
                            await message.answer(
                                f"{i} - {solutions[maybe_solutions[i - 1]]}"
                            )
                            builder.add(types.KeyboardButton(text=str(i)))
                        builder.adjust(2)
                        temp_sol = " ".join(maybe_solutions)
                        sql = f"""\
                            UPDATE mafia SET answered = '{ans}', temp = '{temp_sol}' WHERE id_user = {message.from_user.id}
                        """
                        cur.execute(sql)
                        await message.answer(
                            "Ну и че думаешь?",
                            reply_markup=builder.as_markup(
                                resize_keyboard=True, one_time_keyboard=True
                            ),
                        )
                    else:
                        await message.answer(
                            "Поздравляем! вы истинный чебурек! я бы тебя в землю втоптал милаш."
                        )
                        sql = f"""\
                        UPDATE perm_ids SET complete = 1 WHERE id_user = {message.from_user.id}
                        """
                        await bot.send_message(
                            chat_id=chat_id,
                            text=f'Поздравляем <a href="tg://user?id={message.from_user.id}"> {message.from_user.first_name}</a> с прохождением теста!',
                            parse_mode="HTML",
                        )
                        cur.execute(sql)
                except sqlite3.DatabaseError as err:
                    print("Ошибки: ", err)
                else:
                    print("Успешно.")
                    con.commit()


@router.message(Command("start"))
async def start_test(message: types.Message):
    if message.chat.type == "private":
        print(f"handled start_test(), {message.from_user.first_name}")
        id_user = message.from_user.id
        username = message.from_user.first_name
        with sqlite3.connect("../db/mafiadb.db") as con:
            with con.cursor() as cur:
                sql = """\
                INSERT or IGNORE INTO perm_ids (id_user, username) VALUES (?,?)
                """
                sql_maf = """\
                INSERT or IGNORE INTO mafia (id_user, username) VALUES (?,?)
                """
                sql_test = f"""\
                UPDATE mafia SET generated = '' and answered = '', accept = 1 where id_user = {id_user}
                """
                try:
                    cort = (id_user, username)
                    cur.execute(sql, cort)
                    cur.execute(sql_maf, cort)
                    cur.execute(sql_test)
                except sqlite3.DatabaseError as err:
                    print("Ошибка:", err)
                else:
                    print("Успешно.")
                    con.commit()
                kb = [[types.KeyboardButton(text="НАЧАТЬ ТЕСТ BOSS OF THE GYM")]]
                keyboard = types.ReplyKeyboardMarkup(
                    keyboard=kb,
                    resize_keyboard=True,
                    one_time_keyboard=True,
                    input_field_placeholder="ТОЛЬКО ПОПРОБУЙ ОТСТУПИТЬ ПЕТУХ",
                )
                await message.answer(
                    "ОТВЕТЬ НА ВОПРОС ТЕСТ ХОЧЕШЬ НАЧАТЬ ИЛИ НЕТ ЧЕПУШНЯ??\n"
                    + "ЭТОТ ТЕСТ ПРОВЕРИТ ДОСТОИН ЛИ ТЫ КВАРТИРНИКА У МИШИ МАРКИ",
                    reply_markup=keyboard,
                )


@router.message(F.text.lower() == "начать тест boss of the gym")
async def start_test(message: types.Message):
    if message.chat.type == "private":
        files = os.listdir(directory)
        random.shuffle(files)
        await message.answer("Тест на адекватность начат.")
        for i in range(3):
            await asyncio.sleep(1)
            await message.answer(str(3 - i))
        s = " ".join(files)
        with sqlite3.connect("../db/mafiadb.db") as con:
            with con.cursor() as cur:
                sql = f"""\
                UPDATE mafia SET generated = '{s}', answered = '' WHERE id_user = {message.from_user.id}
                """
                try:
                    cur.execute(sql)
                except sqlite3.DatabaseError as err:
                    print("Ошибка: ", err)
                else:
                    print("Успешно.")
                    con.commit()
                await temp_use(message)


@router.message(F.text.regexp(r"[1-4]"))
async def check_answers(message: types.Message):
    if message.chat.type == "private":
        print(f"handled check_answers(), {message.from_user.first_name}")
        t = True
        with sqlite3.connect("../db/mafiadb.db") as con:
            with con.cursor() as cur:
                sql = f"""\
                SELECT * from mafia WHERE id_user = {message.from_user.id}
                """
                try:
                    cur.execute(sql)
                    arr = cur.fetchall()
                    if arr[0][5] == 1:
                        ans = arr[0][3]
                        temp_ans = arr[0][4]
                        ans = ans.split(" ")
                        temp_ans = temp_ans.split(" ")
                        index = temp_ans.index(ans[-1])
                        s = [
                            "Повезло, давай дальше...",
                            "Хитро выебанный жук...",
                            "мда дед зашел тест проходить",
                            "хватит правильно отвечать...",
                            "тебе бы в русскую рулетку играть...",
                            "да ты бы мишу марки перепил....",
                        ]
                        if (
                            index + 1 == int(message.text)
                            and len(ans) != len(temp_ans) - 1
                        ):
                            await message.answer(random.choice(s))
                        elif index + 1 != int(message.text):
                            await message.answer(
                                "Я ждал, когда ты провалишься))) СКАЖИ ВСЕМ ПОКА А ОЙ НЕ УСПЕЕШЬ АХАХАХХА"
                            )
                            await message.answer(
                                f"Правильный ответ: {solutions[temp_ans[index]]}"
                            )
                            sql = f"""\
                            UPDATE mafia SET accept = 0 WHERE id_user = {message.from_user.id}
                            """
                            cur.execute(sql)
                            if message.from_user.id == 2096676129:
                                await bot.send_message(
                                    chat_id=chat_id,
                                    text=f'Ты свою квартиру проебал, ключи от хаты давай. --> <a href="tg://user?id={message.from_user.id}"> {message.from_user.first_name}</a>',
                                    parse_mode="HTML",
                                )
                            else:
                                await bot.send_message(
                                    chat_id=chat_id,
                                    text=f'ЭТОТ ЛОХ НЕ СДАЛ ТЕСТ --> <a href="tg://user?id={message.from_user.id}"> {message.from_user.first_name}</a>',
                                    parse_mode="HTML",
                                )
                            t = False
                except sqlite3.DatabaseError as err:
                    print("Ошибка: ", err)
                else:
                    print("Успешно.")
                    con.commit()
                if t:
                    await temp_use(message)
