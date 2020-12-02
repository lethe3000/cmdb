from django.urls import path, include

from apps.api.generics import LoginView
from apps.api.swagger import SwaggerSchemaView
from apps.api.views import ApiRootView, DjangoMigrationView
from .credentials import urls as credentials_url
from .categories import urls as categories_url
from .apps import urls as apps_url
from .envs import urls as envs_url

app_name = 'api'
urlpatterns = [
    path('', ApiRootView.as_view(), name='api_root_view'),
    path('login/', LoginView.as_view(), name='login_view'),
    path('credential/', include(credentials_url)),
    path('category/', include(categories_url)),
    path('app/', include(apps_url)),
    path('env/', include(envs_url)),
]

# swagger views
urlpatterns += [
    path('swagger/', SwaggerSchemaView.as_view(), name='swagger_view'),
    path('migrations/', DjangoMigrationView.as_view(), name='migrations_view'),
]
