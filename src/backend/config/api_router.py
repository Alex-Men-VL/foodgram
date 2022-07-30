from apps.users.api.views import UserViewSet
from rest_framework.routers import SimpleRouter

from django.urls import include
from django.urls import path

app_name = 'api'

router = SimpleRouter()

router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
