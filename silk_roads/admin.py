
from django.contrib import admin
from .models import custom_user

@admin.register(custom_user)
class custom_userAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_joined', 'is_active', 'is_staff')
    search_fields = ('username',)
    list_filter = ('is_active', 'is_staff')
    ordering = ('date_joined',)
