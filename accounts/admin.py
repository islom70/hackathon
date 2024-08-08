from django.contrib import admin

from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('username', 'email')
