from django.urls import path
from accounts import views
from accounts.views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', views.login, name='login')
]