from aiogram.dispatcher import Dispatcher
from settings import dp, executor, service_startup, service_shutdown
from handlers import register_all_handlers

def main(dp: Dispatcher) -> None:
    register_all_handlers(dp)
    executor.on_startup(service_startup)
    executor.on_shutdown(service_shutdown)
    executor.start_polling()

if __name__ == '__main__':
    main(dp)