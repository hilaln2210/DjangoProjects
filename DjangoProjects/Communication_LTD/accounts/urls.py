from django.urls import path
from .views import (
    home_view, register_view, login_view,
    change_password_view, forgot_password_view, reset_password_view,
    add_customer_view
)
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('change_password/', change_password_view, name='change_password'),
    path('forgot_password/', forgot_password_view, name='forgot_password'),
    path('reset_password/', reset_password_view, name='reset_password'),
    path('add_customer/', add_customer_view, name='add_customer'),
    path('password_reset_success/', TemplateView.as_view(template_name='password_reset_success.html'), name='password_reset_success'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
