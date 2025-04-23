from django.db import models
from django.core.validators import MinValueValidator


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name="Название", max_length=50, help_text="Пример: Помидор"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ["name"]


class Recipe(models.Model):
    DIET_TYPES = [
        ("default", "Без ограничений"),
        ("vegan", "Веганское"),
        ("gluten_free", "Без глютена"),
    ]
    title = models.CharField(
        verbose_name="Название",
        max_length=100,
        help_text="Пример: Спагетти Карбонара",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Пример: Нежное куриное филе в сливочном соусе с травами.",
    )
    image = models.ImageField(verbose_name="Фото блюда", upload_to="media/", blank=True)
    diet_type = models.CharField(
        verbose_name="Тип питания",
        max_length=20,
        choices=DIET_TYPES,
        default="default",
        db_index=True,
    )
    total_cost = models.DecimalField(
        verbose_name="Общая стоимость",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Стоимость в рублях с копейками",
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name="Время приготовления (минут)", validators=[MinValueValidator(1)]
    )
    ingredients = models.ManyToManyField(Ingredient, verbose_name="Ингредиенты")
    cooking_steps = models.TextField(
        verbose_name="Шаги приготовления",
        help_text="Пример: 1. Нарежьте овощи... 2. Обжарьте мясо...",
    )
    is_active = models.BooleanField(
        verbose_name="Доступно для выбора",
        default=True,
        db_index=True,
        help_text="Снимите галочку, чтобы временно скрыть рецепт из выдачи.",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["-id"]
