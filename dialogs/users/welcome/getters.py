from aiogram_dialog import DialogManager

async def get_welcome(dialog_manager: DialogManager, **middleware_data):
    return {
        'getter_welcome': 'Hello, getter!'
    }
