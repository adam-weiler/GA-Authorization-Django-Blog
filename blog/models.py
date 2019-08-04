# from datetime import datetime
from django.conf import settings #Needed for foreignkey.
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.utils import timezone # Needed for timezone.localtime()
from django.core.validators import (MinLengthValidator,)

from datetime import date, datetime
from django.core.exceptions import ValidationError

from django import forms

from django.forms import DateInput


# def not_future(value):
#     today = datetime.today()
#     breakpoint()
#     if value > today:
#         raise ValidationError('published_date cannot be in the future if it is a draft.')

class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(
        validators=[MinLengthValidator(1)]
    )
    draft = models.BooleanField()
    # published_date = models.DateTimeField(default=datetime.today(), validators=[not_future])
    published_date = models.DateField(default=datetime.today())
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
        fields = ['title', 'body', 'draft', 'published_date', 'author']
        widgets = {
        #     # 'published_date': forms.DateInput(attrs={'class':'datepicker', 'value': datetime.now().strftime("%d-%m-%Y")})
            # 'published_date': forms.DateInput(attrs={'class':'datepicker', 'value': datetime.now()})
            'published_date': forms.DateInput()
        }

    # def clean_date(self):
    #     date = self.cleaned_data.get['published_date']
    #     if date < datetime.date.today():
    #         raise forms.ValidationError('The date cannot be in the past!')
    #     return date

    # def clean_published_date(self):
    #     date = self.cleaned_data['published_date']
    #     breakpoint()
    #     if date < datetime.date.now():
    #         raise forms.ValidationError('No past Date')
    #     return date

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
            #published date must be in future.
        else: #Else is_draft is false.
            
            #published date must be in the past.
            if pub_date > today:
                self.add_error(
                    'published_date', 'Published articles cannot have a future date.'
                )
        
        


        



class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'message']
