# from datetime import date, datetime

from django.db import models
# from django.forms import DateInput, ModelForm
# from django.utils import timezone # Needed for timezone.localtime()
from django.core.validators import (MinLengthValidator,)

# from django import forms


class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(
        validators=[MinLengthValidator(1)]
    )
    draft = models.BooleanField(default=False)    
    published_date = models.DateField(null=True) #This works
    author = models.CharField(max_length=255)

    def __str__(self):
        return f"'{self.title}' - by {self.author}'"


class Topic(models.Model):
    topic = models.CharField(max_length=255)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='topics')

    def __str__(self):
        return f"topic = {self.topic}"


class Comment(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    message = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'\'{self.message}\' - {self.name}'




