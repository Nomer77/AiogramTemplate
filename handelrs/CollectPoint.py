from aiogram.dispatcher import Dispatcher
from .commands import regitster_command_handlers


#File for collect all register handlers from other modules

def register_all_handlers(dp: Dispatcher):
    regitster_command_handlers(dp)