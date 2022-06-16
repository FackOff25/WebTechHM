"""AskKozlov URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from AskKozlovApp import views
from AskKozlov import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls, name="admin"),
                  path('', views.new_questions, name="new questions"),
                  path('new/', views.new_questions, name="new questions"),
                  path('hot/', views.hot_questions, name="hot questions"),
                  path('tag/<str:tg>', views.list_with_tags, name='tag'),
                  path('signup/', views.signup, name="sign up"),
                  path('login/', views.login, name="log in"),
                  path('logout/', views.logout, name="log out"),
                  path('settings/', views.settings, name="settings"),
                  path('ask/', views.ask, name="new question"),
                  path('question/<int:qid>/', views.question, name="question"),
                  path('vote_question/', views.vote_question, name="vote question"),
                  path('vote_answer/', views.vote_answer, name="vote answer"),
                  path('submit_correction/', views.submit_correction, name="vote answer")
              ]
