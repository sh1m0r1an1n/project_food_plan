from django.contrib import admin
from .models import Recipe, Ingredient
from django.contrib.auth.models import Group, User


admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "diet_type", "total_cost", "is_active")
    list_editable = ("diet_type", "is_active")
    list_filter = ("diet_type", "is_active", "total_cost")
    search_fields = ("title",)
    raw_id_fields = ("ingredients",)
    fields = (
        "title",
        "description",
        "cooking_steps",
        "image",
        "cooking_time",
        "diet_type",
        "total_cost",
        "is_active",
        "ingredients",
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
