import logging
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

# Конфигурация
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST")
WEB_SERVER_PORT = os.getenv("WEB_SERVER_PORT")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Обработчики команд
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("👋 Я эхобот на вебхуках!")


@dp.message(F.text)
async def echo_text(message: Message):
    await message.answer(f"🔁 Вы сказали: <i>{message.text}</i>", parse_mode=ParseMode.HTML)


# Запуск сервера
async def on_startup(bot: Bot):
    await bot.set_webhook(f"{WEBHOOK_URL}")


async def main():
    dp.startup.register(on_startup)

    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path="/webhook")

    setup_application(app, dp, bot=bot)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
    await site.start()

    logging.info(f"Сервер запущен на {WEB_SERVER_HOST}:{WEB_SERVER_PORT}")
    await asyncio.Event().wait()  # Бесконечное ожидание


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())