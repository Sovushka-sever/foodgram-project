from django.urls import path
from . import views


urlpatterns = [
    path(
        'v1/subscriptions/<int:author_id>/',
        views.Subscribe.as_view(),
        name='delete_subscriptions',
    ),
    path(
        'v1/subscriptions/',
        views.Subscribe.as_view(),
        name='create_subscriptions',
    ),
    path(
        'v1/favorites/<int:recipe_id>/',
        views.Favorites.as_view(),
        name='delete_favorites',
    ),
    path(
        'v1/favorites/',
        views.Favorites.as_view(),
        name='create_favorites',
    ),
    path(
        'v1/purchases/',
        views.Purchase.as_view(),
        name='create_purchases',
    ),
    path(
        'v1/purchases/<int:recipe_id>/',
        views.Purchase.as_view(),
        name='delete_purchases',
    ),
    path(
        'v1/ingredients/',
        views.IngredientListAPIView.as_view(),
        name='ingredients_list',
    ),
]
