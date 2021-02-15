from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.conf import settings


handler404 = 'foodgram.views.page_not_found'  # noqa
handler500 = 'foodgram.views.server_error'  # noqa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', include('django.contrib.flatpages.urls')),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),
    # path('about-author/', views.flatpage,
    #      {'url': '/about-author/'}, name='about-author'),
    # path('about-spec/', views.flatpage,
    #      {'url': '/about-spec/'}, name='about-spec'),
    path('', include('recipes.urls')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
