import django
from asgiref.sync import sync_to_async
django.setup()
from django.core.cache import cache
import random
from recipes.models import Recipe, DietType


async def get_daily_recipe():
    """Возвращает рецепт дня с кэшированием на 24 часа (асинхронно)."""
    seconds_in_day = 86400
    recipe = await sync_to_async(cache.get)('daily_recipe')

    if not recipe:
        active_recipes = await sync_to_async(Recipe.objects.filter)(is_active=True)
        exists = await sync_to_async(active_recipes.exists)()

        if exists:
            recipe_list = await sync_to_async(list)(active_recipes)
            recipe = random.choice(recipe_list)
            await sync_to_async(cache.set)('daily_recipe', recipe, seconds_in_day)
        else:
            recipe = None

    return recipe


async def get_recipe_ingredients(recipe_id):
    """Возвращает список ингредиентов рецепта (асинхронно)."""
    try:
        recipe = await sync_to_async(Recipe.objects.prefetch_related('ingredients').get)(id=recipe_id)
        return [ingredient.name for ingredient in recipe.ingredients.all()]
    except Recipe.DoesNotExist:
        return []


async def get_all_diets():
    """Возвращает список диет для кнопок (асинхронно)."""
    diets = await sync_to_async(lambda: list(DietType.objects.values_list('name', flat=True)))()
    return list(diets)
