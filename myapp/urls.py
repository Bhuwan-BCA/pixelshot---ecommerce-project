from django.urls import path
from .views.main_view import home_view
from .views.auth_view import register_view, login_view

urlpatterns = [
    path('', home_view, name='homepage'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
]