from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# le appname empêche d'utiliser les views de django il faudrait pouvoir les redefinir


urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', views.logout_request, name='logout'),
    path('login/', views.login_request, name='login'),

    path('password_reset/', views.password_reset_request, name="password_reset"),

    path('password_reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name="login_settings/password_reset_sent.html"), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="login_settings/new_password.html"), name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="login_settings/password_reset_complete.html"), name="password_reset_complete"),





]