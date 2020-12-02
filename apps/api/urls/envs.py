from django.urls import path

from apps.api.views.categories import EnvDetail, EnvList

urls = [
    path('', EnvList.as_view()),
    path('<str:uid>/', EnvDetail.as_view()),
]

__all__ = ['urls']
