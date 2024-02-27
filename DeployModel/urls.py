from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", views.home, name='home'),
    path("result/", views.result, name='result'),
    path("", views.index, name="index"),
]