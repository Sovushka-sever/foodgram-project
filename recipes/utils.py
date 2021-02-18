from django.http import HttpResponse

from .models import Ingredient, IngredientValue
import csv
from django.http import HttpResponse


def get_ingredients(request):
    # ingredients = []
    # for ingredient in recipe.ingredients.all():
    #     amount = ingredient.ingredient_values.get(recipe=recipe)
    #     ingredients.append((ingredient.title, amount, ingredient.dimension))
    # return ingredients

    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            value = key[15:]
            ingredients[request.POST[key]] = request.POST['valueIngredient_' + value]
    return ingredients


def create_ingridients(ingredients, recipe):
    for key, value in ingredients.items():
        arg = key.split("_")
        if arg[0] == 'nameIngredient':
            title = value
        if arg[0] == 'valueIngredient':
            ingredient, _ = Ingredient.objects.get_or_create(
                title=title, defaults={'dimension': 'шт'}
            )
            IngredientValue.objects.update_or_create(
                ingredient=ingredient, recipe=recipe, defaults={'amount': value}
            )


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="tags.csv"'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


