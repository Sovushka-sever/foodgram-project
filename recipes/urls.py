from django.urls import path, include
from . import views

user_patterns = [
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/<int:recipe_id>/', views.recipe_view,
         name='recipe'),
    path('<str:username>/<int:recipe_id>/edit/', views.recipe_edit,
         name='recipe_edit'),
    path('<str:username>/<int:recipe_id>/delete/', views.recipe_delete,
         name='recipe_delete'),
]

urlpatterns = [
    path('new/', views.new_recipe, name='new_recipe'),
    path('addrecipe/', views.add_recipe),
    path('favorite/', views.favorite, name='favorite'),
    path('subscription/', views.subscription, name='subscription'),
    path('shopping_list/', views.shopping_list, name='shopping_list'),
    path('download_list', views.download_list, name='download_list'),
    path('', views.index, name='index'),
    path('', include(user_patterns)),
    # path('', views.index, name='index'),
]

