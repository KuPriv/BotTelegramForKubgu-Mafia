import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from idea.config import token


async def main():
    bot = Bot(token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())


if __name__ == "__main__":
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())