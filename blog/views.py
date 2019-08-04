from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from blog.models import * #Importing the classes from models.py file.


def root(request): # Redirects to http://localhost:8000/home/
    return HttpResponseRedirect('/home')

# def home_page(request): # http://localhost:8000/home/
#     context = { 'blog_articles': Article.objects.all().order_by('-published_date'), 'blog_topics': Topic.objects.all() } #The - in published_date means order from newest to oldest.

#     response = render(request, 'index.html', context)
#     return HttpResponse(response)

def show_all(request):
    context = { 'blog_articles': Article.objects.all().order_by('-published_date'), 'blog_topics': Topic.objects.all() } #The - in published_date means order from newest to oldest.

    response = render(request, 'articles.html', context)
    return HttpResponse(response)

def show_article(request, id): #Load a single article page based on id.
    article = Article.objects.get(pk=id)
    form = CommentForm()
    # form.article = article # assoicate the comment to the article somehow
    return render(request, 'article.html', {
        'article': article, 
        'form': form
    })

def create_comment(request, article_id):
    article = Article.objects.get(pk=article_id)
    form = CommentForm(request.POST)

    comment = form.save(commit=False)
    comment.article = article
    comment.save()
    return redirect(reverse("show_article", args=[article_id]))

    # # pass
    # article_id = request.POST['article']
    # article = Article.objects.get(pk=article_id)

    # form = CommentForm(request.POST)
    # context = {'article': article, 'form':form}

    # if form.is_valid():
    #     new_comment = form.save(commit=False)
    #     # new_comment.article = 


    # article_id = request.POST['article']
    # # 
    # article = Article.objects.get(pk=article_id)
    # # breakpoint()
    # # form.fields.append({'article_id':'article'}) #Sets the foreign key as the article object.

    # # if form.is_valid():
    #     # comment = form.save(commit=False)
    #     # comment.message = message
    
    # # form.article = article_id
    # form.save()

    # response = render(request, 'article.html', context)
    # return HttpResponse(response)

    # # form = CommentForm(request.POST)
    # # form.save()

    # # context = {'article': article}
    # # response = render(request, 'article.html', context)
    # # return HttpResponse(response)