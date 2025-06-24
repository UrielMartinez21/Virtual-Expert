from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    max_experts = models.IntegerField(default=1)
    max_documents_per_expert = models.IntegerField(default=10)
    max_file_size_mb = models.IntegerField(default=10)
    plan_type = models.CharField(max_length=50, default='free')  # free, pro, enterprise

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f"Profile of {self.user.username}"

