"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.root, name='index'),  # Redirect to all articles.
    
    # path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', views.login_view, name="login"),
    path('accounts/logout/', views.logout_view, name="logout"),
    path('accounts/signup', views.signup, name='signup'),  # Form to signup for new account.
    # path('accounts/signup_create', views.signup_create, name='signup_create'),  # Saving a new account.

    path('articles/', views.show_all, name='show_all'),  # Show all articles.

    path('articles/new', views.new_article, name='new_article'),  # Form to create a new article.
    path('articles/create', views.create_article, name='create_article'),  # Saving new article.
    # path('home/', views.home_page, name='home_page'),
    
    path('articles/<int:article_id>', views.show_article, name='show_article'),  # Show 1 article.
    path('articles/<int:article_id>/edit', views.article_edit, name='article_edit'),  # Edits current article, if owner.
    path('articles/<int:article_id>/comments/new', views.create_comment, name='create_comment'),  # Saving a new comment.
]
