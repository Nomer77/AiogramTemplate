from aiogram_dialog import Dialog

from .windows import *


dialog = Dialog(
    hello_window(),
    name='welcome everybody dialog'
)
