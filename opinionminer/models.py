from django.db import models
from django.utils import timezone

class Opinion(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    sentiment = models.CharField(max_length=20)
    date = models.DateField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    likes = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.sentiment})"

    def __str__(self):
        return f"{self.title} ({self.sentiment})"