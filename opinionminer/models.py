from django.db import models
from django.utils import timezone

class Opinion(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    sentiment = models.CharField(max_length=20)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.sentiment})"

    def __str__(self):
        return f"{self.title} ({self.sentiment})"