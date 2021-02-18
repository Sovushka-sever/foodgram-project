from django.urls import path
from . import views


# urlpatterns = [
#     path('ingredients/', views.get_ing),
#     path('favorites/', views.Favorites.as_view()),
#     path('favorites/<int:recipe_id>', views.Favorites.as_view()),
#     path('subscriptions/', views.Subscribe.as_view()),
#     path('subscriptions/<int:author_id>', views.Subscribe.as_view()),
#     path('purchases/', views.Purchase.as_view()),
#     path('purchases/<int:recipe_id>', views.Purchase.as_view()),
# ]

urlpatterns = [
    path(
        'v1/subscriptions/<int:pk>/',
        views.SubscriptionDeleteAPIView.as_view(),
        name='delete_subscriptions',
    ),
    path(
        'v1/subscriptions/',
        views.SubscriptionCreateAPIView.as_view(),
        name='create_subscriptions',
    ),
    path(
        'v1/favorites/<int:pk>/',
        views.FavoriteDeleteAPIView.as_view(),
        name='delete_favorites',
    ),
    path(
        'v1/favorites/',
        views.FavoriteCreateAPIView.as_view(),
        name='create_favorites',
    ),
    path(
        'v1/purchases/',
        views.ShoppingListCreateAPIView.as_view(),
        name='create_purchases',
    ),
    path(
        'v1/purchases/<int:pk>/',
        views.ShoppingListDestroyAPIView.as_view(),
        name='delete_purchases',
    ),
    path(
        'v1/ingredients/',
        views.IngredientListAPIView.as_view(),
        name='ingredients_list',
    ),
]