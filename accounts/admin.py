from django.contrib import admin
from accounts.models import User


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'username',
                    'first_name',
                    'last_name',
                    'email',
                    'is_active',
                    'email_confirmed',
                    'is_staff',
                    'is_superuser',
                    'date_joined',
                    'last_login',
                    ]
