from .models import Ingredient, IngredientValue


def get_ingredients(recipe):
    ingredients = []
    for ingredient in recipe.ingredients.all():
        amount = ingredient.ingredient_values.get(recipe=recipe)
        ingredients.append((ingredient.title, amount, ingredient.dimension))
    return ingredients


def create_ingridients(recipe, data):
    for key, amount in data.items():
        arg = key.split("_")
        if arg[0] == "nameIngredient":
            title = amount
        if arg[0] == "valueIngredient":
            ingredient, _ = Ingredient.objects.get_or_create(
                title=title, defaults={"dimension": "шт"}
            )
            IngredientValue.objects.update_or_create(
                ingredient=ingredient, recipe=recipe, defaults={"amount": amount}
            )
