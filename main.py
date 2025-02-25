from asyncio import run
from settings import bot, dp, on_startup, on_shutdown
from aiogram_dialog import setup_dialogs

from handlers import router as handlers_router
from dialogs import router as dialogs_router


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    setup_dialogs(dp)
    dp.include_router(handlers_router)
    dp.include_router(dialogs_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())