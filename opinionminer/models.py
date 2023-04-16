from django.db import models

class Opinion(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    sentiment = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.title} ({self.sentiment})"