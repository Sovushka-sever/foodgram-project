def get_ingredients(request):
    """
    Получение ингредиентов из формы создания/редактирования рецепта
    """

    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            value = key[15:]
            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + value
            ]
    return ingredients
