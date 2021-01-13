from django.contrib import admin
from .models import (
    Recipe,
    Ingredient,
    IngredientValue,
    Subscription,
    ShoppingList,
    Favorite,
)


class IngredientValueInline(admin.StackedInline):
    model = IngredientValue


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    def favorites_count(self, obj):
        favorite = Favorite.objects.filter(recipe=obj).count()
        return favorite

    favorites_count.short_description = 'Количество добавлений в избранное'

    list_display = ('pk', 'name', 'pub_date', 'author', 'display_favorites')
    search_fields = ('description',)
    list_filter = ('author', 'name', 'tags', 'pub_date')
    inlines = (IngredientValueInline,)
    readonly_fields = ('favorites_count',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit_of_measure')
    search_fields = ('title',)
    list_filter = ('title',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    fields = ('user', 'author')


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    fields = ('user', 'recipe')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    fields = ('user', 'recipe')
