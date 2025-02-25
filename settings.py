from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from aiogram.utils.token import TokenValidationError
from dotenv import load_dotenv
from typing import Final
import logging
import os
import sys

from orm import ORM


def load_envFile(env_file: str) -> None:
    if os.path.isfile(env_file):
        load_dotenv(dotenv_path=env_file)
        logging.info("Environment file connected.")
    else:
        logging.critical("Didn't found Environment file")
        sys.exit(1)

logging.basicConfig(level=logging.INFO)

ENV_FILE = ".env.template"
load_envFile(ENV_FILE)

try:
    bot: Final = Bot(token=os.getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
except TokenValidationError:
    logging.critical("The token is undefined or invalid. Check .env file")
    sys.exit(1)

dp: Dispatcher = Dispatcher(storage=MemoryStorage(), events_isolation=SimpleEventIsolation())


async def on_startup():
    await ORM.orm_init()

async def on_shutdown():
    await ORM.orm_shutdown()
    await dp.storage.close()
