from django.core.cache import cache
from django.db.models import QuerySet
import random
from .models import Recipe, DietType


def get_daily_recipe():
    """Возвращает рецепт дня с кэшированием на 24 часа."""
    seconds_in_day = 86400
    recipe = cache.get('daily_recipe')
    if not recipe:
        active_recipes = Recipe.objects.filter(is_active=True)
        if active_recipes.exists():
            recipe = random.choice(active_recipes)
            cache.set('daily_recipe', recipe, seconds_in_day)
        else:
            recipe = None
    return recipe


def get_recipe_ingredients(recipe_id): # recipe_id = recipe.id
    """Возвращает список ингредиентов рецепта."""
    try:
        recipe = Recipe.objects.prefetch_related('ingredients').get(id=recipe_id)
        return [ingredient.name for ingredient in recipe.ingredients.all()]
    except Recipe.DoesNotExist:
        return []


def get_all_diets():
    """Возвращает список диет для кнопок."""
    return list(DietType.objects.values_list('slug', flat=True))


def filter_by_diet(diet_slugs: list) -> QuerySet:
    """Фильтрует рецепты по списку диет."""
    return Recipe.objects.filter(
        is_active=True,
        diet_types__slug__in=diet_slugs
    ).distinct() # Убирает дубликаты


def filter_by_price(queryset, max_price=None) -> QuerySet:
    """Фильтрует рецепты по цене (<=) и сортирует по убыванию."""
    if max_price:
        queryset = queryset.filter(total_cost__lte=max_price)
    return queryset.order_by('-total_cost')