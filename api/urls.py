# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from api import views
# from rest_framework.authtoken import views as token_views
#
# router_v1 = DefaultRouter()
# router_v1.register(r'posts', views.PostViewSet, basename='post')
# router_v1.register(r'posts/(?P<id>\d+)/comments',
#                    views.CommentViewSet,
#                    basename='comment')
#
#
# urlpatterns = [
#     path('api/v1/api-token-auth/', token_views.obtain_auth_token),
#     path('api/v1/', include(router_v1.urls))
# ]
#
