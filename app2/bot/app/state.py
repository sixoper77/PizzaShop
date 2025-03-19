from aiogram.fsm.state import State, StatesGroup
class OrderForm(StatesGroup):
    last_name = State()
    email = State()
    city = State()
    address = State()
    postal_code = State()