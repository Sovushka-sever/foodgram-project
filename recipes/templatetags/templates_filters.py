from django import template

from recipes.models import Favorite, Subscription, ShoppingList

register = template.Library()


@register.filter(name='is_follow')
def is_follow(author, user):
    return Subscription.objects.filter(
        user=user, author=author
    ).exists()


@register.filter(name='is_favorite')
def is_favorite(recipe_id, user_id):
    return Favorite.objects.filter(
        user_id=user_id, recipe_id=recipe_id
    ).exists()


@register.filter(name='is_shop')
def is_shop(recipe, user):
    return ShoppingList.objects.filter(
        user=user, recipe=recipe
    ).exists()


@register.filter(name='get_filter_values')
def get_filter_values(value):
    return value.getlist('filters')


@register.filter(name='get_filter_link')
def get_filter_link(request, tag):
    new_request = request.GET.copy()

    if tag.slug in request.GET.getlist('filters'):
        filters = new_request.getlist('filters')
        filters.remove(tag.slug)
        new_request.setlist('filters', filters)
    else:
        new_request.appendlist('filters', tag.slug)

    return new_request.urlencode()


@register.filter(name='plural_recipe')
def plural_recipe(number):
    """
    Фильтр для корректного отображения рецепта во множественном числе
    """

    if number % 10 == 1 and number not in (11, 111):
        ending = ''
    elif 1 < number % 10 < 5 and number not in (12, 13, 14, 112, 113, 114):
        ending = 'а'
    else:
        ending = 'ов'
    return ending
