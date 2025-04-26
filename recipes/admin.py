from django.contrib import admin
from .models import Recipe, Ingredient, DietType
from django.contrib.auth.models import Group, User


admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "get_diet_types", "total_cost", "is_active")
    filter_horizontal = ("diet_types", "ingredients")
    list_editable = ("is_active", "total_cost")
    list_filter = ("diet_types", "is_active", "total_cost")
    search_fields = ("title",)
    fields = (
        "title",
        "description",
        "cooking_steps",
        "image",
        "cooking_time",
        "diet_types",
        "total_cost",
        "is_active",
        "ingredients",
    )

    def get_diet_types(self, obj):
        """Преобразует ID и объекты DietType в строку с названиями диет."""
        return ", ".join([diet.name for diet in obj.diet_types.all()])

    get_diet_types.short_description = "Типы питания"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    fields = ("name",)
    ordering = ["name"]


@admin.register(DietType)
class DietTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    list_editable = ("slug",)