from django.contrib.auth import get_user_model
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    get_object_or_404,
)
from rest_framework.response import Response
from recipes.models import Ingredient, Subscription, Favorite, Recipe, ShoppingList
from .serializers import (
    IngredientSerializer,
    SubscriptionSerializer,
    FavoriteSerializer,
    ShoppingListSerializer,
)

User = get_user_model()


class IngredientListAPIView(ListAPIView):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        query = self.request.query_params.get('query', None)

        if query is not None:
            queryset = queryset.filter(title__icontains=query)

        return queryset


class SubscriptionCreateAPIView(CreateAPIView):
    serializer_class = SubscriptionSerializer


class SubscriptionDeleteAPIView(DestroyAPIView):
    serializer_class = SubscriptionSerializer
    queryset = User.objects.all()

    def destroy(self, request, *args, **kwargs):
        Subscription.objects.filter(
            user=self.request.user, author=self.get_object()
        ).delete()
        return Response(data={'success': True})


class FavoriteCreateAPIView(CreateAPIView):
    serializer_class = FavoriteSerializer


class FavoriteDeleteAPIView(DestroyAPIView):
    serializer_class = FavoriteSerializer
    queryset = Recipe.objects.all()

    def destroy(self, request, *args, **kwargs):
        Favorite.objects.filter(
            user=self.request.user, recipe=self.get_object()
        ).delete()
        return Response(data={'success': True})


class ShoppingListCreateAPIView(CreateAPIView):
    serializer_class = ShoppingListSerializer
    queryset = Recipe.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request=request)
        return Response(data={'success': True})


class ShoppingListDestroyAPIView(DestroyAPIView):
    serializer_class = ShoppingListSerializer
    queryset = Recipe.objects.all()

    def destroy(self, request, *args, **kwargs):
        recipe = self.get_object()
        user = get_object_or_404(User, username=request.user.username)
        shoppinglist = ShoppingList(request)
        shoppinglist.delete(recipe.id)
        return Response(data={'success': True})


# class Favorites(LoginRequiredMixin, View):
#     def post(self, request):
#         req_ = json.loads(request.body)
#         recipe_id = req_.get('id', None)
#         if recipe_id:
#             recipe = get_object_or_404(Recipe, id=recipe_id)
#             obj, created = Favorite.objects.get_or_create(
#                 user=request.user, recipe=recipe
#             )
#             if created:
#                 return JsonResponse({'success': True})
#             return JsonResponse({'success': False})
#         return JsonResponse({'success': False}, status=400)
#
#     def delete(self, request, recipe_id):
#         recipe = get_object_or_404(
#             Favorite, recipe=recipe_id, user=request.user
#         )
#         recipe.delete()
#         return JsonResponse({'success': True})
#
#
# class Purchases(LoginRequiredMixin, View):
#
#     def post(self, request):
#         recipe_id = json.loads(request.body)['id']
#         recipe = get_object_or_404(Recipe, id=recipe_id)
#         ShoppingList.objects.get_or_create(
#             user=request.user, recipe=recipe)
#         return JsonResponse({'success': True})
#
#     def delete(self, request, recipe_id):
#         recipe = get_object_or_404(Recipe, id=recipe_id)
#         user = get_object_or_404(User, username=request.user.username)
#         obj = get_object_or_404(ShoppingList, user=user, recipe=recipe)
#         obj.delete()
#         return JsonResponse({'success': True})
#
#
# class Subscribe(LoginRequiredMixin, View):
#     def post(self, request):
#         req_ = json.loads(request.body)
#         author_id = req_.get('id', None)
#         if author_id is not None:
#             author = get_object_or_404(User, id=author_id)
#             obj, created = Subscription.objects.get_or_create(
#                 user=request.user, author=author
#             )
#             if created:
#                 return JsonResponse({'success': True})
#             return JsonResponse({'success': False})
#         return JsonResponse({'success': False}, status=400)
#
#     def delete(self, request, author_id):
#         user = get_object_or_404(
#             User, username=request.user.username
#         )
#         author = get_object_or_404(User, id=author_id)
#         obj = get_object_or_404(Subscription, user=user, author=author)
#         obj.delete()
#         return JsonResponse({'success': True})
#
#
# class Purchase(LoginRequiredMixin, View):
#     def post(self, request):
#         recipe_id = json.loads(request.body)['id']
#         recipe = get_object_or_404(Recipe, id=recipe_id)
#         ShoppingList.objects.get_or_create(user=request.user, recipe=recipe)
#         return JsonResponse({'success': True})
#
#     def delete(self, request, recipe_id):
#         recipe = get_object_or_404(Recipe, id=recipe_id)
#         user = get_object_or_404(User, username=request.user.username)
#         obj = get_object_or_404(ShoppingList, user=user, recipe=recipe)
#         obj.delete()
#         return JsonResponse({'success': True})
#
#
# # class Ingredient(LoginRequiredMixin, View):
# #     def get(self, request):
# #         text = request.GET['query']
# #         ingredients = Ingredient.objects.filter(
# #             title__icontains=text).values('title', 'dimension')
# #         return JsonResponse(ingredients, safe=False)
#
#
# def get_ing(request):
#     text = request.GET['query']
#     ingredients = Ingredient.objects.filter(
#         title__icontains=text).values_list('title', 'dimension')
#     unit = []
#     for i in ingredients:
#         unit.append(
#             {
#                 'title': i[0],
#                 'dimension': i[1],
#             }
#         )
#     return JsonResponse(unit, safe=False)
