from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from blog.models import Article, Topic, Comment #Importing the classes from models.py file.

def root(request): # Redirects to http://localhost:8000/home/
    return HttpResponseRedirect('/home')

# def home_page(request): # http://localhost:8000/home/
#     context = { 'blog_articles': Article.objects.all().order_by('-published_date'), 'blog_topics': Topic.objects.all() } #The - in published_date means order from newest to oldest.

#     response = render(request, 'index.html', context)
#     return HttpResponse(response)

def articles_page(request):
    context = { 'blog_articles': Article.objects.all().order_by('-published_date'), 'blog_topics': Topic.objects.all() } #The - in published_date means order from newest to oldest.

    response = render(request, 'articles.html', context)
    return HttpResponse(response)

def article_show(request, id):
    article = Article.objects.get(pk=id)
    context = {'article': article}

    response = render(request, 'article.html', context)
    return HttpResponse(response)

def create_comment(request):
    new_comment = Comment()
    article_id = request.POST['article']
    article = Article.objects.get(pk=article_id)

    new_comment.name = request.POST['name']
    new_comment.message = request.POST['message']
    new_comment.article = article #Sets the foreign key as the article object.

    new_comment.save()

    context = {'article': article}
    response = render(request, 'article.html', context)
    return HttpResponse(response)