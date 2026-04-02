from django.urls import path
from .views.main_view import homepage

urlpatterns = [
    path('', homepage, name='homepage'),
]