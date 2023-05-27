from aiogram.dispatcher.filters.state import StatesGroup, State


class RubsSom(StatesGroup):
    rub = State()
class SomsRub(StatesGroup):
    som = State()


class KztsSom(StatesGroup):
    kzt = State()
class SomsKzt(StatesGroup):
    som= State()