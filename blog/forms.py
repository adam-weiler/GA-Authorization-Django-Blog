from datetime import date
from django.forms import DateInput, ModelForm
from blog.models import Article, Comment


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        # fields = ['title', 'body', 'draft', 'published_date', 'author']
        fields = ['title', 'body', 'draft', 'published_date']
        widgets = {
            'published_date': DateInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        new_title = cleaned_data.get('title')
        new_body = cleaned_data.get('body')
        is_draft = cleaned_data.get('draft')
        pub_date = cleaned_data.get('published_date')
        today = date.today()

        if len(new_title) < 10:
            self.add_error(
                'title', 'Article title must be longer than 10 characters.'
            )

        if len(new_body) < 10:
            self.add_error(
                'body', 'Article body must be longer than 10 characters.'
            )
        
        if pub_date == None: #If user didn't enter a date, it defaults to today.
            pub_date = today

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

