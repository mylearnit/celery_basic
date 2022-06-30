from django.db import models

# Create your models here.
class Notification(models.Model):
    title=models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)