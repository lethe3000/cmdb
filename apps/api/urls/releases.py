from django.urls import path

from apps.api.views.releases import ReleaseDetail, ReleaseList

urls = [
    path('', ReleaseList.as_view(), name='release_list'),
    path('<str:uid>/', ReleaseDetail.as_view(), 'release_detail'),

]

__all__ = ['urls']
