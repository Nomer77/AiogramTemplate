from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Row

from tools.keyboards import BaseKeyboard

from .states import WelcomeFSM
from . import getters

kbd = BaseKeyboard(module_name='welcome')


def hello_window():
    return Window(
        Const('Hello, world!'),
        Row(
            kbd.cancel_btn()
        ),
        getter=getters.get_welcome,
        state=WelcomeFSM.world
    )
