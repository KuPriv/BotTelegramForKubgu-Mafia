import asyncio
import logging
from aiogram.types import InputFile
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config import token


async def main():
    bot = Bot(token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())


if __name__ == "__main__":
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())