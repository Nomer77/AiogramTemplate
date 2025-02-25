from aiogram.fsm.state import State, StatesGroup


class WelcomeFSM(StatesGroup):
    world = State()
