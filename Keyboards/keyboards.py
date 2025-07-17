from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


def get_restrictions_keyboard(selected: set, options):
    keyboard = []
    for option in options:
        if option in selected:
            text = f"🟢{option}"
        else:
            text = f'🔴{option}'
        keyboard.append([InlineKeyboardButton(text=text, callback_data=f"toggle_{option}")])
    keyboard.append([
        InlineKeyboardButton(text="Сохранить", callback_data="save"),
        InlineKeyboardButton(text="Очистить выбор", callback_data="clear")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


choose_diet_button = KeyboardButton(text='Индивидуальные предпочтения')
choose_budget_button = KeyboardButton(text='Выбрать блюдо по дешевле')

combined_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [choose_diet_button, choose_budget_button]
    ],
    resize_keyboard=True
)
