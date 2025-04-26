from aiogram.fsm.state import StatesGroup, State


class RestrictionStates(StatesGroup):
    choosing_restrictions = State()
    budget_condition = State()