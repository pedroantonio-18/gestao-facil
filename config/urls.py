from django.contrib import admin
from django.urls import include, path

from pages.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path("__reload__/", include("django_browser_reload.urls")),
]
