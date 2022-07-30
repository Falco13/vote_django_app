from django.contrib import admin
from contact.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name_user', 'first_name', 'email', 'text', 'created_at', 'is_done']
    readonly_fields = ['created_at']
