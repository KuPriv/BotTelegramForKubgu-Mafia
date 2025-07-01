import aiohttp
import asyncio
import aioconsole
import os
from dotenv import load_dotenv
import logging
from time import asctime


class OwnException(Exception):
    def __str__(self):
        return "Меня убил ctrl + C :("


def setup():
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")
    template_request = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s"

    return TOKEN, CHAT_ID, template_request


async def wait_message(TOKEN, CHAT_ID, template_request):
    logging.info("Зашли в wait_message, %s", asctime())
    logging.info("Ожидание ввода...")
    message = await aioconsole.ainput(
        "Для выхода введите: 'q'\nВведите ваше сообщение: "
    )
    if message == "q":
        raise OwnException()

    logging.info(
        "Сообщение получено: %s в %s"
        % (
            message,
            asctime(),
        )
    )
    return await send_message(TOKEN, CHAT_ID, template_request, message)


async def send_message(TOKEN, CHAT_ID, template_request, message):
    logging.info("Зашли в send_message, %s", asctime())
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            template_request
            % (
                TOKEN,
                CHAT_ID,
                message,
            )
        )
        logging.info("Отправили запрос. Ждем подтверждения.")
        return await response.json()


async def main():
    TOKEN, CHAT_ID, template_request = setup()
    while True:
        try:
            result_of_response = await wait_message(TOKEN, CHAT_ID, template_request)
            if result_of_response.get("ok"):
                logging.info(
                    "Сообщение %s успешно отправлено в chat id: %s в %s"
                    % (
                        result_of_response["result"]["text"],
                        CHAT_ID,
                        asctime(),
                    )
                )
        except OwnException as e:
            logging.exception(e)
            break
        except Exception as e:
            logging.exception("Ошибка: ", exc_info=e)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())

    except Exception as e:
        logging.exception("ФАТАЛИТИ:", exc_info=e)
