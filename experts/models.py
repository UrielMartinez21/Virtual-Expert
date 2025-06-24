from django.db import models
from users.models import Profile


class Expert(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experts')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.profile.user.username})"


class ChatMessage(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q: {self.question[:30]} - {self.user.username}"
