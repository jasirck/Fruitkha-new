from django.urls import path
from . import views


urlpatterns = [
    path("homepage", views.homepage, name="homepage"),
    path("", views.homepage, name="homepage"),
    path("about", views.about, name="about"),
    path("news", views.news, name="news"),
    path("contact", views.contact, name="contact"),
]
