from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:  # pragma: no cover
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
