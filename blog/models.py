from django.conf import settings #Needed for foreignkey.
from django.contrib.auth.models import User
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    draft = models.BooleanField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=255)
    # topic = models.ForeignKey(
    #     Topic, on_delete=models.CASCADE)

    def __str__(self):
        return f"title = {self.title}"

class Topic(models.Model):
    topic = models.CharField(max_length=255)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='topics')

    def __str__(self):
        return f"topic = {self.topic}"