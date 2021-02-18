from .models import ShoppingList, Tag


def counter(request):
    if request.user.is_authenticated:
        count = ShoppingList.objects.filter(user=request.user).count()
    else:
        count = None
    return {'count': count}


def all_tags(request):
    """
    Вывод всех тегов
    """

    tags = Tag.objects.all()
    return {'all_tags': tags}


def filter_in_url(request):
    """
    Установка фильтров в урл страницы
    """

    result_str = ''
    for item in request.GET.getlist('filters'):
        result_str += f'&filters={item}'
    return {'filters': result_str}