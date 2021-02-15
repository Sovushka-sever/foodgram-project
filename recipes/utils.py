from django.http import HttpResponse

from .models import Ingredient, IngredientValue
import csv
from django.http import HttpResponse


# def get_ingredients(request):
#     ingredients = []
#     for ingredient in request.ingredients.all():
#         value = ingredient.ingredient_values.get(recipe=request)
#         ingredients.append((ingredient.title, value, ingredient.dimension))
#     return ingredients

# def get_ingredients(request):
#     ingredients = {}
#     for key, ingredient_name in request.POST.items():
#         if 'nameIngredient' in key:
#             _ = key.split('_')
#             ingredients[ingredient_name] = int(request.POST[
#                 f'valueIngredient_{_[1]}']
#             )
#     return ingredients
#
#
# def create_ingridients(request, recipe):
#
#     for key, amount in request.items():
#         arg = key.split('_')
#         if arg[0] == 'nameIngredient':
#             title = amount
#         if arg[0] == 'amountIngredient':
#             ingredient, _ = Ingredient.objects.get_or_404(
#                 title=title,
#                 defaults={'dimension': 'шт'}
#             )
#             IngredientValue.objects.update_or_create(
#                 ingredient=ingredient, recipe=recipe, defaults={'amount': amount}
#             )
def get_ingredients(request):
    ing_dict = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            value = key[15:]
            ing_dict[request.POST[key]] = request.POST['valueIngredient_' + value]
    return ing_dict


def create_ingridients(ing_dict, recipe):
    for key, value in ing_dict.items():
        # IngredientValue.objects.create(
        #     amount=ing_dict[key],
        #     ingredient=Ingredient.objects.get(title=value),
        #     recipe=recipe,
        # )
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


