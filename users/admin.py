from django.contrib import admin
from . import models

@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'max_experts', 'max_documents_per_expert', 'plan_type']
    search_fields = ['user__username', 'user__email']
    list_filter = ['plan_type','max_experts', 'max_documents_per_expert']
    ordering = ['-updated_at']


