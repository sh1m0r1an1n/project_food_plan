import random
from pathlib import Path
from asgiref.sync import sync_to_async
from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, CallbackQuery
import django
django.setup()
from decimal import Decimal

from Keyboards.keyboards import get_restrictions_keyboard, choose_diet_button
from Common.tools import get_recipe_ingredients, get_daily_recipe, get_all_diets
from recipes.models import Recipe
from Common.states import RestrictionStates


user_private_router = Router()
user_selections = {}


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    daily_recipe = await get_daily_recipe()
    diet_type = await sync_to_async(list)(
        daily_recipe.diet_types.all().values_list('name', flat=True))
    ingredients = await get_recipe_ingredients(daily_recipe.id)
    photo_path = FSInputFile(f'{daily_recipe.image}')
    message_with_daily_recipe = (f'Приветствую {message.from_user.first_name}!\n'
                                 f'Рецепт дня: {daily_recipe.title}.\n'
                                 '\n'
                                 f'Описание: {daily_recipe.description}\n'
                                 '\n'
                                 f'Ограничения: {', '.join(diet_type)}\n'
                                 f'Cтоимость: {daily_recipe.total_cost}\n'
                                 '\n'
                                 f'Ингредиенты: {', '.join(ingredients)}\n'
                                 f'Если вы хотите выбрать другие ограничения по составу блюда или вас не устроила стоимость, нажмите на кнопку⏬')

    if f'{daily_recipe.image}'.endswith('.gif'):
        await message.answer_animation(animation=photo_path,
                                       caption=message_with_daily_recipe,
                                       reply_markup=choose_diet_button)
    else:
        await message.reply_photo(photo=photo_path,
                                  caption=message_with_daily_recipe,
                                  reply_markup=choose_diet_button)


@user_private_router.message(Command('diets'))
@user_private_router.message(F.text.contains('Выбрать ограничения'))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(RestrictionStates.choosing_restrictions)
    user_selections[message.from_user.id] = set()
    options = await get_all_diets()
    keyboard = get_restrictions_keyboard(user_selections[message.from_user.id], options)
    await message.answer("Выберите особые ограничения (можно ничего не выбирать):", reply_markup=keyboard)


@user_private_router.callback_query(RestrictionStates.choosing_restrictions)
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    data = callback_query.data
    options = await get_all_diets()

    if user_id not in user_selections:
        user_selections[user_id] = set()

    if data.startswith("toggle_"):
        option = data.replace("toggle_", "")
        if option in user_selections[user_id]:
            user_selections[user_id].remove(option)
        else:
            user_selections[user_id].add(option)

        keyboard = get_restrictions_keyboard(user_selections[user_id], options)
        await callback_query.message.edit_reply_markup(reply_markup=keyboard)
        await callback_query.answer()

    elif data == "save":
        selected = user_selections.get(user_id, set())
        if selected:
            await callback_query.message.answer(f"Сохранено: {', '.join(selected)}")
        else:
            await callback_query.message.answer("Вы не выбрали ограничения. Все ингредиенты разрешены!")
        await state.update_data(choosing_restrictions=selected)

        await callback_query.message.answer("Введите ограничение по стоимости (например, 1000):")
        await state.set_state(RestrictionStates.budget_condition)
        await callback_query.answer()

    elif data == "clear":
        user_selections[user_id].clear()
        keyboard = get_restrictions_keyboard(user_selections[user_id], options)
        await callback_query.message.edit_reply_markup(reply_markup=keyboard)
        await callback_query.answer(text="Выбор очищен!")


@user_private_router.message(RestrictionStates.budget_condition, (F.text.regexp(r"^(\d+)$").as_("digits")))
async def get_budget_of_user(message: types.Message, state: FSMContext):
    await state.update_data(budget_condition=message.text)
    data = await state.get_data()
    active_recipes =  await sync_to_async(list)(Recipe.objects.filter(is_active=True))

    matching_recipes = []
    for recipe in active_recipes:
        diet = await sync_to_async(list)(recipe.diet_types.values_list('name', flat=True))
        if set(data['choosing_restrictions']) == set(diet) and recipe.total_cost < Decimal(data['budget_condition']):
            matching_recipes.append(recipe)

    try:
        suitable_recipe = random.choice(matching_recipes)
        ingredients = await get_recipe_ingredients(suitable_recipe.id)
        photo_path = FSInputFile(f'{suitable_recipe.image}')
        message_with_daily_recipe = (f'Рецепт дня: {suitable_recipe.title}.\n'
                                     '\n'
                                     f'Описание: {suitable_recipe.description}\n'
                                     '\n'
                                     f'стоимость: {suitable_recipe.total_cost}\n'
                                     '\n'
                                     f'Ингредиенты: {', '.join(ingredients)}\n')

        if f'{suitable_recipe.image}'.endswith('.gif'):
            await message.answer_animation(animation=photo_path,
                                           caption=message_with_daily_recipe)
        else:
            await message.reply_photo(photo=photo_path,
                                      caption=message_with_daily_recipe)
    except IndexError:
        await message.answer(f"Подходящих рецептов не нашлось.")

    await state.clear()
