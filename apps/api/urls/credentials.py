from django.urls import path

from apps.api.views import ApiRootView

urls = [
    path('', ApiRootView.as_view())
]

__all__ = ['urls']
