from django.urls import path, include
from . import views

user_patterns = [
    path('', views.profile, name='profile'),
    path('<int:recipe_id>/', views.recipe_view,
         name='recipe'),
    path('<int:recipe_id>/edit/', views.recipe_edit,
         name='recipe_edit'),
    path('<int:recipe_id>/delete/', views.recipe_delete,
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
    path('<str:username>/', include(user_patterns)),
]

