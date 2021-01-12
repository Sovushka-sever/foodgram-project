from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


User = get_user_model()


@admin.register(User)
class UsersAdmin(UserAdmin):
    list_filter = (
        'username',
        'email',
        'is_staff',
        'is_superuser',
        'is_active',
        'groups',
    )

# list_filter позволяет фильтровать по указаным полям
# @admin.register выполняет ту же функцию, что и замененная admin.site.register()
