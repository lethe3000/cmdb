from django.urls import path

from apps.api.views.categories import CategoryList, CategoryDetail, CategoryChildren

urls = [
    path('', CategoryList.as_view()),
    path('<str:uid>/', CategoryDetail.as_view()),
    path('children/child', CategoryChildren.as_view())
]

__all__ = ['urls']
