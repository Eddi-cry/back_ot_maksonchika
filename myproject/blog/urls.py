from django.urls import path
from . import views
from .views import generate_download_link

urlpatterns = [
    path('', views.home, name='home'),
    path('generate_download_link/', generate_download_link, name='generate_download_link'),
]