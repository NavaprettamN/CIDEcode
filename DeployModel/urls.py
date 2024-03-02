from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("mixer/", views.mixer_page, name='mixer'),
    path("illicit/", views.illicit_page, name='illicit'),
    path("transaction/", views.transaction_page, name='transaction'),
    path("overall/", views.overall_analaysis_page, name='overall'),
]
