import asyncio
import os
import random

from aiogram import Bot, types, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command

from aiogram.types import FSInputFile, ChatMemberBanned, ChatMemberRestricted, URLInputFile
from config_for_test import token
from config import my_id, chat_id
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder

bot = Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
router = Router()


@router.message(Command('start'))
async def start_test(message: types.Message):
    kb = [
        [types.KeyboardButton(text='НАЧАТЬ ТЕСТ BOSS OF THE GYM')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='ТОЛЬКО ПОПРОБУЙ ОТСТУПИТЬ ПЕТУХ')
    await message.answer("ОТВЕТЬ НА ВОПРОС ТЕСТ ХОЧЕШЬ НАЧАТЬ ИЛИ НЕТ ЧЕПУШНЯ??\n" + \
                         "ЭТОТ ТЕСТ ПРОВЕРИТ ДОСТОИН ЛИ ТЫ КВАРТИРНИКА У МИШИ МАРКИ", reply_markup=keyboard)


@router.message(F.text.lower() == "начать тест boss of the gym")
async def start_test(message: types.Message):
    if message.chat.type == 'private':
        directory = 'mafia_photos/'
        files = os.listdir(directory)
        random.shuffle(files)
        solutions = {
            'efim.jpg': "большой босс",
            'danya.jpg': "даня нож режж",
            'ilya.jpg': "главный алкаш илья",
            'zayac.jpg': 'заяц не кролик',
            'vlada.jpg': 'влада крутой волк'
        }
        await message.answer('Тест на адекватность начат.')
        await asyncio.sleep(1)
        await message.answer('3')
        await asyncio.sleep(1)
        await message.answer('2')
        await asyncio.sleep(1)
        await message.answer('1')
        await asyncio.sleep(1)
        guested = []
        while len(guested) != len(files):
            file: str = directory + random.choice(files)
            temp = file.replace('mafia_photos/', '')
            if temp not in guested:
                photo = FSInputFile(path=file, filename=temp)
                await bot.send_photo(chat_id=message.chat.id, photo=photo)
                if temp != 'efim.jpg':
                    await message.answer('Ваши догадки, кто этот покемон???')
                else:
                    await message.answer("Надеюсь, ты знаешь эту легенду...")
                builder = ReplyKeyboardBuilder()
                for i in range(1, 5):
                    builder.add(types.KeyboardButton(text=str(i)))
                builder.adjust(2)
                await message.answer(
                    'Ну и че думаешь?',
                    reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True),
                )
                guested.append(temp)


@router.message(F.text == '1' or F.text == '2' or F.text == '3' or F.text == '4')
async def check_answers(message: types.Message):
    ...