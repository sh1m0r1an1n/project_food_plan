from django.db import models
from django.core.validators import MinValueValidator


class DietType(models.Model):
    name = models.CharField(verbose_name="Название", max_length=20, unique=True)
    slug = models.SlugField(verbose_name="Слаг", max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип диеты"
        verbose_name_plural = "Типы диет"


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name="Название", max_length=50, help_text="Пример: Помидор", unique=True
    )
    quantity = models.CharField(
        max_length=50,
        verbose_name="Количество",
        blank=True,
        null=True,
        help_text="Пример: 400 грамм, 6 зубчиков (необязательно)"
    )

    def __str__(self):
        return f"{self.name} ({self.quantity})" if self.quantity else self.name

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ["name"]


class Recipe(models.Model):
    title = models.CharField(
        verbose_name="Название",
        max_length=100,
        unique=True,
        help_text="Пример: Спагетти Карбонара",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Пример: Нежное куриное филе в сливочном соусе с травами.",
    )
    image = models.ImageField(verbose_name="Фото/гифка блюда", upload_to="media/", blank=True)
    diet_types = models.ManyToManyField(
        DietType,
        verbose_name="Типы питания",
        related_name="recipes",
        blank=True
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