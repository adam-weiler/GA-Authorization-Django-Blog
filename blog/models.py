# from datetime import datetime
from django.conf import settings #Needed for foreignkey.
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.utils import timezone # Needed for timezone.localtime()

class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    draft = models.BooleanField()
    published_date = models.DateTimeField(default=timezone.localtime())
    author = models.CharField(max_length=255)
    # topic = models.ForeignKey(
    #     Topic, on_delete=models.CASCADE)

    def __str__(self):
        return f"'{self.title}' - by {self.author}'"

class Topic(models.Model):
    topic = models.CharField(max_length=255)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='topics')

    def __str__(self):
        return f"topic = {self.topic}"

class Comment(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.localtime())
    message = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'\'{self.message}\' - {self.name}'

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'draft', 'author']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'message']