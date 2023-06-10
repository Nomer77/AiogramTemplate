from aiogram.dispatcher import Dispatcher
from settings import dp, executor, service_startup, service_shutdown

def main(dp: Dispatcher) -> None:
    executor.on_startup(service_startup)
    executor.on_shutdown(service_shutdown)
    executor.start_polling()

if __name__ == '__main__':
    main(dp)