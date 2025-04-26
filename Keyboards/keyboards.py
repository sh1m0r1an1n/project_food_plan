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


choose_diet_button = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Выбрать ограничения')]],
        resize_keyboard=True)
