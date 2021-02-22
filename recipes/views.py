from django.contrib.auth.models import User
from django.db.models import Sum
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
import csv
from .utils import get_ingredients


def index(request):
    """Главная страница"""
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
    """Создание рецепта"""
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    ingredients = get_ingredients(request)

    if form.is_valid():
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
        return redirect('index')

    return render(
        request,
        'new_recipe.html',
        {'is_edit': False,
         'form': form, }
    )


def recipe_edit(request, username, recipe_id):
    """Редактирование рецепта"""
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

    if form.is_valid():
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
        return redirect('recipe', username=username, recipe_id=recipe_id, )

    return render(
        request,
        'new_recipe.html',
        {'is_edit': True,
         'form': form,
         'recipe': recipe, }
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
    recipes = Recipe.objects.filter(author=username). \
        select_related('author').all()

    if tag:
        recipes = recipes.filter(tags__slug__in=tag)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if request.user.is_authenticated:
        following = Subscription.objects.filter(user=request.user). \
            filter(author=username).select_related('author')

        if not following:
            following = None
        else:
            following = True

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
    recipes = Recipe.objects.filter(recipe_shopping_list__user=request.user)
    ingredients_list = recipes.values(
        'ingredients__title',
        'ingredients__dimension'
    ).annotate(
        total_amount=Sum('recipe_ingredients__amount')
    )
    file_data = ''

    for item in ingredients_list:
        line = ' '.join(str(value) for value in item.values())
        file_data += line + '\n'

    response = HttpResponse(
        file_data,
        content_type='application/text charset=utf-8'
    )
    response['Content-Disposition'] = 'attachment; filename="ShoppingList.txt"'
    return response


def add_recipe(request):
    with open('ingredients.csv', encoding='utf-8') as file:
        r_file = csv.reader(file, delimiter=',')

        for i in r_file:
            Ingredient.objects.create(title=i[0], dimension=i[1])
        return redirect('index')
