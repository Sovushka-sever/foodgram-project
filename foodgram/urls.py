# """YaMDb URL Configuration
#
# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/3.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.conf import settings
#
urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('redoc/', TemplateView.as_view(
#         template_name='redoc.html'
#     ), name='redoc'),
#     path('api/', include('users.urls')),
#     path('api/', include('reviews.urls')),
#     path('api/', include('artworks.urls')),
]


handler404 = "foodgram.views.page_not_found"  # noqa
handler500 = "foodgram.views.server_error"  # noqa

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
