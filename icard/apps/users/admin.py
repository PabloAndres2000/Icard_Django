
# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from icard.apps.users.models import User


class UserAdmin(UserAdmin):
    """
    User model admin.
    """

    list_display = ('email', 'username', 'first_name',
                    'last_name', 'is_staff')


admin.site.register(User)
