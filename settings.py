from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import Executor
from aiogram.utils.exceptions import ValidationError
from DataBase import ORM
from dotenv import load_dotenv
from typing import Final
import logging
import os
import sys


def load_envFile(env_file: str) -> None:
    if os.path.isfile(env_file):
        load_dotenv(dotenv_path=env_file)
        logging.info("Environment file connected.")
    else:
        logging.critical("Didn't found Environment file")
        sys.exit(1)

logging.basicConfig(level=logging.INFO)
load_envFile(".env")
try:
    bot: Final = Bot(token=os.getenv("BOT_TOKEN"), parse_mode='html')
except ValidationError:
    logging.critical("The token is undefined or invalid. Check .env file")
    sys.exit(1)
storage: Final = MemoryStorage()
dp: Final = Dispatcher(bot, storage=storage)
executor: Final = Executor(dp, skip_updates=True)

async def service_startup(dp: Dispatcher):
    await ORM.orm_init()

async def service_shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()
    await ORM.orm_shutdown()

