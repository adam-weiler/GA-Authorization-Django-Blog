# from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from blog.models import Article, Topic, Comment
from blog.forms import ArticleForm, CommentForm, LoginForm


def root(request): # Redirects to http://localhost:8000/articles
    return redirect(reverse("show_all"))


def show_all(request):  # Renders a list of all articles.
    return render(request, "articles.html", { 
        'blog_articles': Article.objects.all().order_by('-published_date'),
        'blog_topics': Topic.objects.all() 
    })  #The - in published_date means order from newest to oldest.


def show_article(request, article_id):  # Renders a single article.
    return render(request, 'article.html', {
        'article': Article.objects.get(pk=article_id), 
        'form': CommentForm()
    })


@login_required
def new_article(request):  # Renders a form to create a new article.
    return render(request, 'article_form.html', {
        'form': ArticleForm()
    })


@login_required
def create_article(request):  # User creating a new article.
    form = ArticleForm(request.POST)

    if form.is_valid():
        new_article = form.save(commit=False)
        new_article.user = request.user
        new_article.save()

        return redirect(reverse('show_all'))
    else:  # Else sends user back to article_form page.
        return render(request, 'article_form.html', {
            'form': form
        })
        # return redirect(reverse('new_article')) #How do you reverse and attach a form..?


def create_comment(request, article_id):  # Renders a form to create a new comment.
    article = Article.objects.get(pk=article_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.article = article
        new_comment.save()
        return redirect(reverse('show_article', args=[article_id]))
    else:  # Else sends user back to article page.
        return render(request, 'article.html', {
            'article': article, 
            'form': form
        })


def signup(request):  # Renders a form for a new user to signup.
    if request.user.is_authenticated:
        return redirect(reverse("show_all"))

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.clenaed_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('show_all'))
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {
        'form': form
    })


def login_view(request):  # Logins in user if request is valid.
    if request.user.is_authenticated:
        return redirect(reverse('show_all'))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('show_all'))
                else:
                    form.add_error('username', 'This account has been disabled.')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {
        'form': form
    })
    

def logout_view(request):
    logout(request)
    return redirect(reverse("show_all"))


@login_required
def article_edit(request, article_id):
    article = get_object_or_404(Article, pk=article_id, user=request.user.pk)  # Returns 404 if article does not exist or if user is not owner.

    if request.user.is_authenticated:  # Checks if user is logged in.
        if request.method == 'POST':  # Checks if request is POST.
            form = ArticleForm(request.POST)

            if form.is_valid():
                edit_article = form.save(commit=False)
                edit_article.user = request.user
                edit_article.id = article_id
                edit_article.save()
                return redirect(reverse('show_article', kwargs={'article_id':article_id}))
            else:
                return render(request, 'article_edit.html', {  # This repeats.
                    'article': article,
                    'article_id': article_id,
                    'form': ArticleForm(instance=article)
                })

        return render(request, 'article_edit.html', {  # This repeats.
            'article': article,
            'article_id': article_id,
            'form': ArticleForm(instance=article)
        })
    else:
        return redirect(reverse('image_details', kwargs={'article_id':article_id}))