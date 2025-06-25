from django.contrib import admin
from .models import Expert

# Register your models here.
@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile', 'created_at', 'updated_at')
    search_fields = ('name', 'profile__user__username')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('created_at', 'updated_at')