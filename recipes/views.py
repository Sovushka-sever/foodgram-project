from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RecipeForm
from .models import (
    Recipe,
    Ingredient,
    Subscription,
    ShoppingList,
    IngredientValue,
)
from django.core.paginator import Paginator
from .utils import get_ingredients


def index(request):
    """Главная страница '/index' """

    tags_slug = request.GET.getlist('filters')
    recipe_list = Recipe.objects.all()

    if tags_slug:
        recipe_list = recipe_list.filter(
            tags__slug__in=tags_slug).distinct().all()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'index.html',
        {'page': page,
         'paginator': paginator, }
    )


def new_recipe(request):
    """Создание рецепта '/new' """

    user = User.objects.get(username=request.user)
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    ingredients = get_ingredients(request)

    if not form.is_valid():
        return render(
            request,
            'new_recipe.html',
            {'is_edit': False,
             'form': form, }
        )

    recipe = form.save(commit=False)
    recipe.author = user
    recipe.save()

    for title, amount in ingredients.items():
        ingredient = Ingredient.objects.get(title=title)
        units = IngredientValue(
            amount=amount,
            ingredient=ingredient,
            recipe=recipe)
        units.save()
    form.save_m2m()

    return redirect('index')


def recipe_edit(request, username, recipe_id):
    """Редактирование рецепта """

    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
        author__username=username
    )

    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    ingredients = get_ingredients(request)

    if not form.is_valid():
        return render(
            request,
            'new_recipe.html',
            {'is_edit': True,
             'form': form,
             'recipe': recipe, }
        )

    IngredientValue.objects.filter(recipe=recipe).delete()
    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()

    for title, amount in ingredients.items():
        ingredient = Ingredient.objects.get(title=title)
        units = IngredientValue(
            amount=amount,
            ingredient=ingredient,
            recipe=recipe)
        units.save()
    form.save_m2m()

    return redirect(
        'recipe',
        username=username,
        recipe_id=recipe_id,
    )


def recipe_delete(request, recipe_id, username):
    """Удаление рецепта"""

    recipe = get_object_or_404(Recipe, id=recipe_id)
    author = get_object_or_404(User, username=username)

    if request.user == author:
        recipe.delete()
    return redirect('index')


def recipe_view(request, recipe_id, username):
    """Отображение рецепта"""

    recipe = get_object_or_404(Recipe, id=recipe_id)
    profile = get_object_or_404(User, username=username)

    return render(
        request,
        'singlePage.html',
        {'profile': profile,
         'recipe_id': recipe_id,
         'recipe': recipe, }
    )


def profile(request, username):
    """Профиль пользователя"""

    username = get_object_or_404(User, username=username)
    tag = request.GET.getlist('filters')
    recipes = Recipe.objects.filter(
        author=username
    ).select_related('author').all()

    if tag:
        recipes = recipes.filter(tags__slug__in=tag)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if request.user.is_authenticated:
        following = Subscription.objects.filter(
            user=request.user
        ).filter(
            author=username
        ).select_related('author')

        if not following:
            following = None

        return render(
            request,
            'authorRecipe.html',
            {'username': username,
             'page': page,
             'paginator': paginator,
             'following': following, }
        )

    return render(
        request,
        'authorRecipe.html',
        {'username': username,
         'page': page,
         'paginator': paginator, }
    )


def favorite(request):
    """Просмотр избранных рецептов"""

    tag = request.GET.getlist('filters')
    recipe_list = Recipe.objects.filter(
        favorites__user__id=request.user.id).all()

    if tag:
        recipe_list = recipe_list.filter(
            tags__slug__in=tag).distinct()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'favorite.html',
        {'page': page,
         'paginator': paginator, }
    )


def subscription(request):
    """Просмотр избранных авторов"""

    author_list = Subscription.objects.filter(
         user__id=request.user.id).all()

    paginator = Paginator(author_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'myFollow.html',
        {'page': page,
         'paginator': paginator,
         'author': author_list, }
    )


def shopping_list(request):
    """Просмотр списка покупок"""

    shopping_list_user = ShoppingList.objects.filter(user=request.user).all()
    return render(
        request,
        'shopping_list.html',
        {'shopping_list': shopping_list_user, }
    )


def download_list(request):
    """Скачивание списка покупок"""

    shopping_list = ShoppingList.objects.filter(user=request.user).all()
    ingredients_dict = {}

    for item in shopping_list:

        for unit in item.recipe.recipe_ingredients.all():

            title = f'{unit.ingredient.title} {unit.ingredient.dimension}'

            if title in ingredients_dict.keys():
                ingredients_dict[title] += unit.amount
            else:
                ingredients_dict[title] = unit.amount

    ingredients_list = []

    for key, value in ingredients_dict.items():
        ingredients_list.append(f'{key} - {value}, ' + '\n')

    response = HttpResponse(
        ingredients_list,
        content_type='application/text charset=utf-8'
    )
    response['Content-Disposition'] = 'attachment; filename="ShoppingList.txt"'
    return response
