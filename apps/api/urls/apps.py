from django.urls import path

from apps.api.views.categories import AppList, AppDetail

urls = [
    path('', AppList.as_view()),
    path('<str:uid>/', AppDetail.as_view()),
]

__all__ = ['urls']
