import asyncio
import os
import random
import sqlite3

from aiogram import Bot, types, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER
from aiogram.types import FSInputFile, ChatMemberBanned, ChatMemberRestricted, URLInputFile
from config_for_test import token
from config import my_id, chat_id
import pandas as pd

bot = Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
router = Router()


"""@router.message()
async def ttt(message: types.Message):
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
    )"""


@router.chat_join_request()
async def handle_join_request(message: types.Message):
    try:
        print("dp.chat_join_request()")
        print(f"comeback israil {message.from_user.username}")
        await bot.approve_chat_join_request(chat_id=message.chat.id, user_id=message.from_user.id)
        #gif = FSInputFile("greeting.gif", filename="greeting.gif")
        photo_hello = FSInputFile('png_for_functions_handlers/photo_2024-08-02_13-45-19.jpg', filename='danya nozh')
        await asyncio.sleep(2)
        #await bot.send_message(chat_id=message.chat.id, text='ЛИВАЙ ПОКА НЕ ПОЗДНО ДОЛБАЕБ ЗРЯ ТЫ СЮДА ЗАШЕЛ БЛЯЯЯЯЯТЬ')
        #await bot.send_message(chat_id=message.chat.id, text=f'Приветствуем сектанта: <a href="tg://user?{message.from_user.id}">{message.from_user.username}</a>')
        #await bot.send_animation(chat_id=message.chat.id, animation=gif)
        await bot.send_photo(chat_id=message.chat.id, photo=photo_hello, caption='ДАНЯ НОЖ ПРИВЕТСТВУЕТ ВАС')
    except Exception as e:
        print(f"Произошла ошибка: {e}")


@router.chat_member(ChatMemberUpdatedFilter(MEMBER >> IS_NOT_MEMBER))
async def handle_invite_request(message: types.Message):
    print("dp.chat_member()")
    user_status = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    print(user_status)
    if isinstance(user_status, ChatMemberBanned) or isinstance(user_status, ChatMemberRestricted):
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


@router.message(Command("accepted"))
async def misha_house(message: types.Message):
    con = sqlite3.connect('mafiadb.db')
    cur = con.cursor()
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
            s += f'<a href="tg://user?id={ids[i]}"> {usernames[i]}</a>\n'
        print(s)
        await message.answer(text=f'Список людей допущенных до квартирника у марки: {s}', parse_mode='HTML')
    except sqlite3.DatabaseError as err:
        print('Ошибка:', err)
    else:
        print('Успешно.')
    cur.close()
    con.close()


@router.message(Command("tag"))
async def who_did_test(message: types.Message):
    con = sqlite3.connect('mafiadb.db')
    cur = con.cursor()
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
        for i in range(int((len(ids) / 5))):
            s = """"""
            for j in range(5):
                s += f'<a href="tg://user?id={ids[i + j]}"> {usernames[i + j]}</a> '
                index = i + j
            await message.answer(text=s, parse_mode='HTML')
        s = """"""
        for i in range(index, len(ids)):
            s += f'<a href="tg://user?id={ids[i]}"> {usernames[i]}</a> '
        await message.answer(text=s, parse_mode='HTML')
    except sqlite3.DatabaseError as err:
        print('Ошибка:', err)
    else:
        print('Успешно.')
    cur.close()
    con.close()


@router.message(Command("bye22"))
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


@router.message(Command("silly"))
async def us(message: types.Message):
    directory = 'png_for_bot/'
    files = os.listdir(directory)
    file: str = directory + random.choice(files)
    agenda = FSInputFile(path=file, filename='попка дурак')
    await message.answer("/silly dlya ne silly")
    await bot.send_photo(chat_id=message.chat.id, photo=agenda)


@router.message(Command("maf"))
async def us(message: types.Message):
    ref = '<a href=https://t.me/MafiososBot>/start@MafiososBot</a>'
    await message.answer('/start')

@router.message(Command("send_one_pic"))
async def us(message: types.Message):
    agenda = FSInputFile(path='png_for_functions_handlers/Screenshot from 2024-08-05 16-53-52.png', filename='1.png')
    await bot.send_photo(chat_id=message.chat.id, photo=agenda)
    await message.answer('так лучше?')


@router.message(Command("wookie"))
async def tronula(message: types.Message):
    video_url = 'https://youtu.be/aMGa4993ohc?si=916kDHHCoLb1F1Lk'
    await message.answer(f"мозг вуки при поиске мафов чееек: {video_url}")

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


@router.message(Command("song"))
async def send_songs(message: types.Message):
    #audio = FSInputFile('nervy-kofe-mojj-drug.mp3')
    #await bot.send_audio(message.chat.id, audio)
    audio_file = URLInputFile('https://muzwild.net/upload_file/66a2c65973e986.43660759.mp3', filename='sirop.mp3')
    await message.answer_audio(audio=audio_file)
    await asyncio.sleep(1)
    await message.answer('Мои Supreme трусы испачканы в сиропе\n'
                         'А всё из-за того, что штаны спущены до жопы')
    #await message.answer("Нервы ура!")


@router.message(Command("shuti_lock"))
async def send_songs(message: types.Message):
    #audio = FSInputFile('nervy-kofe-mojj-drug.mp3')
    #await bot.send_audio(message.chat.id, audio)
    href = 'https://dl3s2.muzofond.fm/aHR0cDovL2YubXAzcG9pc2submV0L21wMy8wMDAvNjQ2LzMwMS82NDYzMDEubXAz'
    audio_file = URLInputFile(url=href, filename='shuti.mp3')
    await message.answer_audio(audio=audio_file)
    await asyncio.sleep(1)
    s = """Два вора, лихо скрывшись от погони
Делить украденное золото решили
На старом кладбище, вечернею порою
Уселись рядом на заброшенной могиле
И вроде поровну досталось им богатство
Но вот беда — последняя монета
Один кричит: «Она моя — я лучше дрался!»
«Да что б ты делал, друг, без моего совета?»

[Куплет 1]
— Отдай монету, а не то я рассержусь
— Мне наплевать, я твоей злости не боюсь
— Но ведь я похитил деньги и всё дело провернул
— Без моих идей, невежа, ты бы и шагу не шагнул

[Припев]
Что же делать нам с монетой, как же нам её делить?
— Отдадим покойнику
— Отлично! Так тому и быть

[Куплет 2]
— Я был проворней, значит, денежка моя
— Не допущу, чтоб ты богаче был, чем я
— Сейчас вцеплюсь тебе я в горло и на части разорву
— Я прибью тебя дубиной и все деньги заберу!
See upcoming rock shows
Get tickets for your favorite artists
You might also like
МИР ГОРИТ (WORLD IS BURNING)
Oxxxymiron
ГЛАМУР (GLAMOUR)
​uniqe, nkeeei, ARTEM SHILOVETS & Wipo
Два друга и разбойники (Two Friends and Robbers)
Король и Шут (Korol I Shut)
[Припев]
Что же делать нам с монетой, как же нам её делить
— Отдадим покойнику
— Отлично! Так тому и быть

[Куплет 3]
И мертвец, гремя костями, вдруг поднялся из земли:
«Довели меня, проклятые, ей-богу, довели!»
Воры вмиг переглянулись, и помчались наутёк
А мертвец всё золото с собой в могилу уволок"""
    await message.answer(s)
    #await message.answer('Мои Supreme трусы испачканы в сиропе\n'
                         #'А всё из-за того, что штаны спущены до жопы')
    #await message.answer("Нервы ура!")



@router.message(Command("qwe"))
async def same(message: types.Message):
    #s = """В Краснодарском крае жара усилится, и 4 августа днем температура может достигнуть +37 градусов!"""
    s2 = 'ПИЗДАНУТАЯ ТЫ ОДНА КАПСОМ ПИШЕШЬ ХАРЭ'
    #await message.answer(s)
    await message.answer(s2)

@router.message(Command("wawookie"))
async def what_about_wookie(message: types.Message):
    s1 = '太阳, [4 авг. 2024 в 16:55]\n' + \
'скажите честно вуки это чей-то проект по истреблению населения'
    s2 =  '太阳, [4 авг. 2024 в 16:56]\n' + \
'это пиздец кто создал вуки для убийства людей'
    s3 = 'Бля мне кароче кажется иногда, что у вуки свой мир, где у нее нет этих сообщений, которые пишут здесь, и она поэтому о них не знает и не видит'
    s4 = 'мне иногда кажется что вуки не умеет читать'
    s5 = 'фраза вуки: Мы имеем право тупить!'
    s6 = 'фраза вуки: Мы не используем фразы по типу клянусь если что'
    s7 = """Ребят хватит пожалуйста уже творить эту хрень и подъебывать хотя бы сегодня, я сказала что у меня нет настроения и это очень сильно раздражает, неужели нельзя это понять, у меня не стальные нервы и все это терпеть невозможно на постоянке, я не концентрируюсь на этом постоянно но сейчас это очень раздражает, хватит пожалуйста"""
    li = [s1, s2, s3, s4, s5, s6, s7]
    ans = random.choice(li)
    await message.answer(ans)


@router.message(Command("clean"))
async def clean_bot_messages(message: types.Message):
    lis = []
    await bot.delete_messages(chat_id=message.chat.id, message_ids=lis)


@router.message(Command("test_info"))
async def clean_bot_messages(message: types.Message):
    await message.answer('КРУТОЙ ТЕСТ УЖЕ ПРЯМО У МЕНЯ В ЛИЧКЕ!!! ПИШИ МНЕ КОММАНДУ /start В ЛС')


@router.message(Command('china'))
async def talk_about_china(message: types.Message):
    s = """Кита́й или Маша Макима (кит. трад. 中國, упр. 中国, пиньинь Zhōngguó, палл. Чжунго), официальное название — Кита́йская Наро́дная
     Респу́блика (сокр. КНР), (кит. трад. 中華人民共和國, упр. 中华人民共和国, пиньинь Zhōnghuá Rénmín Gònghéguó, палл. Чжунхуа
      Жэньминь Гунхэго) — государство в Восточной Азии. Занимает 4-е место в мире по территории среди государств (9 598 962 км2),
       уступая России, Канаде и США, а по численности населения — 1 411 750 000 жителей (без Тайваня, Гонконга и Макао) — второе 
       после Индии. Уровень урбанизации равен 65 %. """
    await message.answer(s)


@router.message(Command('musor'))
async def qw(message: types.Message):
    await message.answer('алика ты такая пикми')


@router.message(Command('weather'))
async def krasniyday(message: types.Message):
    df = pd.read_html('https://rp5.ru/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B4%D0%B0%D1%80%D0%B5,_%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B4%D0%B0%D1%80%D1%81%D0%BA%D0%B8%D0%B9_%D0%BA%D1%80%D0%B0%D0%B9')
    print(df[8][0:10])