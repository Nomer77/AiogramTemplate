from aiogram import types
from aiogram_dialog import DialogManager, ShowMode
from typing import Any



async def on_chosen_smth(callback_data: types.CallbackQuery, widget: Any, manager: DialogManager, chosen_id: str):
    manager.dialog_data.update(
        chosen_field={
            'id': int(chosen_id)
        }
    )
    await manager.switch_to(...)


async def on_entered_smth(message: types.Message, widget: Any, manager: DialogManager, input_text: str):
    manager.show_mode = ShowMode.DELETE_AND_SEND
    manager.dialog_data.setdefault("input_values", []).append(input_text)
