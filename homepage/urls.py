from django.urls import path
from homepage import views

urlpatterns = [
    path('', views.home_page, name='home')
]