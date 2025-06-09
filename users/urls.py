from django.urls import path
from .views import RegisterUserView, PingView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='user-register'),
    path('ping/', PingView.as_view(), name='ping'),
]
