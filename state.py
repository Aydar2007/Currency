from aiogram.dispatcher.filters.state import State,StatesGroup

class DollarSom(StatesGroup):
    dollar = State()
class SomDollar(StatesGroup):
    som = State()


class EuroSom(StatesGroup):
    euro = State()
class SomEuro(StatesGroup):
    som = State()
