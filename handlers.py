import asyncio
import os
import random

from aiogram import Bot, types, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER
from aiogram.types import FSInputFile, ChatMemberBanned, ChatMemberRestricted, URLInputFile
from config_for_test import token
from config import my_id, chat_id


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
    agenda = FSInputFile(path='png_for_functions_handlers/Screenshot from 2024-08-04 18-26-03.png', filename='1.png')
    await bot.send_photo(chat_id=message.chat.id, photo=agenda)
    await message.answer('куда память на ubuntu нахуй уходит я не понимаю')


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


@router.message(Command("shutilock"))
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
    li = [s1, s2, s3, s4, s5]
    ans = random.choice(li)
    await message.answer(ans)

@router.message(Command("clean"))
async def clean_bot_messages(message: types.Message):
    lis = []
    await bot.delete_messages(chat_id=message.chat.id, message_ids=lis)
