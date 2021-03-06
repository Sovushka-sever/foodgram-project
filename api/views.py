from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from rest_framework.generics import (
    ListAPIView,
    get_object_or_404,
)
from django.views import View
from rest_framework.utils import json
from recipes.models import (
    Ingredient,
    Subscription,
    Favorite,
    Recipe,
    ShoppingList
)
from .serializers import IngredientSerializer

User = get_user_model()


class IngredientListAPIView(ListAPIView):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        query = self.request.query_params.get('query')

        if query:
            return queryset.filter(title__icontains=query)

        return queryset


class Favorites(LoginRequiredMixin, View):

    def post(self, request):
        req_ = json.loads(request.body)
        recipe_id = req_.get('id')

        if recipe_id is None:
            return JsonResponse({'success': False}, status=400)

        recipe = get_object_or_404(Recipe, id=recipe_id)
        obj, created = Favorite.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )
        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(
            Favorite,
            recipe=recipe_id,
            user=request.user
        )
        recipe.delete()
        return JsonResponse({'success': True})


class Subscribe(LoginRequiredMixin, View):

    def post(self, request):
        req_ = json.loads(request.body)
        author_id = req_.get('id')

        if author_id is None:
            return JsonResponse({'success': False}, status=400)

        author = get_object_or_404(User, id=author_id)
        obj, created = Subscription.objects.get_or_create(
            user=request.user,
            author=author
        )
        return JsonResponse({'success': True})

    def delete(self, request, author_id):
        subscription = get_object_or_404(
            Subscription,
            author=author_id,
            user=request.user
        )
        subscription.delete()
        return JsonResponse(data={'success': True})


class Purchase(LoginRequiredMixin, View):

    def post(self, request):
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ShoppingList.objects.get_or_create(user=request.user, recipe=recipe)
        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        ShoppingList.objects.filter(
            user=request.user,
            recipe=recipe_id
        ).delete()
        return JsonResponse({'success': True})
