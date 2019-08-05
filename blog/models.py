from datetime import date, datetime

from django.db import models
from django.forms import DateInput, ModelForm
from django.utils import timezone # Needed for timezone.localtime()
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
    created_at = models.DateTimeField(default=timezone.localtime())
    message = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'\'{self.message}\' - {self.name}'


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'draft', 'published_date', 'author']
        widgets = {
            'published_date': DateInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        is_draft = cleaned_data.get('draft')
        pub_date = cleaned_data.get('published_date')
        today = date.today()

        if is_draft is True:
            if pub_date < today:
                self.add_error(
                    'published_date', 'Draft articles cannot have a past date.'
                )
        else: #Else is_draft is false.
            if pub_date > today:
                self.add_error(
                    'published_date', 'Published articles cannot have a future date.'
                )
        

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'message']

