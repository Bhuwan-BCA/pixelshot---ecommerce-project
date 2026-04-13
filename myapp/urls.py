from django.urls import path
from .views.main_view import home_view, password_reset_view, password_reset_confirm_view,profile_view
from .views.auth_view import register_view, login_view, logout_view

urlpatterns = [
    path('', home_view, name='homepage'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password-reset/', password_reset_view, name='password_reset'),
    path('password-reset/<str:token>/', password_reset_confirm_view, name='password_reset_confirm'),
    path('profile/', profile_view, name='profile'),

]