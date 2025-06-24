from django.db import models
from experts.models import Expert


class Document(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name='documents')
    user_file = models.FileField(upload_to='documents/')
    name = models.CharField(max_length=200)
    file_type = models.CharField(max_length=20)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.file_type})"


class Chunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    text = models.TextField()
    embedding = models.BinaryField()  # serialized numpy array or pointer to vector DB
    position = models.IntegerField()

    def __str__(self):
        return f"Chunk {self.position} from {self.document.name}"
