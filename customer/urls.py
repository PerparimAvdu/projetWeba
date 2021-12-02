from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'customer'

urlpatterns = [
    path('settings/<str:pk>/', views.user_settings, name='user_settings'),

    path('delete_account/<str:pk>/', views.delete_account_from_customer, name='delete_account_from_customer'),

    path('customer_dashboard/<str:customer_pk>/', views.customer_dashboard, name='customer_dashboard'),

    path('create_reservation_from_customer/<str:car_pk>/', views.create_reservation_from_customer, name='create_reservation_from_customer'),

    path('update_reservation_from_customer_1/<str:reservation_pk>/', views.update_reservation_from_customer_1, name='update_reservation_from_customer_1'),

    path('update_reservation_from_customer_2/<str:reservation_pk>/', views.update_reservation_from_customer_2, name='update_reservation_from_customer_2'),

    path('delete_reservation_customer/<str:reservation_pk>/', views.delete_reservation_from_customer, name='delete_reservation_from_customer'),

]