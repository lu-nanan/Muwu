"""
URL configuration for MarkFlow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from MarkFlowImpl.views import auth_views, word_add_views, image_extract, word_filter_views, basic_massage
from MarkFlowImpl.views.word_learn_views import GetWordsView, LearningFeedbackView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/",auth_views.login),
    path('verification/',auth_views.verification),
    path('register/',auth_views.register),
    path('words/search/',word_add_views.word_search),
    path('image/',image_extract.recognize_covered_words ),
    path('image_test/',image_extract.test_recognize_covered_words),
    path('word_add/',word_add_views.word_add),
    path('word_get/',GetWordsView.as_view()),
    path(
        "word_book/",
        word_filter_views.SimpleUserWordFilterAPIView.as_view(),
        name="user-word-filter"
    ),
    path('word_feedback/',LearningFeedbackView.as_view()),
    path('basic_message/',basic_massage.UserWordStatsAPIView.as_view())
]
