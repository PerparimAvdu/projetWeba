from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'reservations_management'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),

    path('all_customers_from_admin/', views.all_customers_from_admin, name='all_customers_from_admin'),

    path('create_customer_from_admin/', views.create_customer_from_admin, name='create_customer_from_admin'),

    path('customer_profile_from_admin/<str:pk>/',
         views.customer_profile_from_admin,  name='customer_profile_from_admin'),

    path('delete_customer_admin/<str:pk>/', views.delete_customer_from_admin,  name='delete_customer_from_admin'),

    path('create_reservation_from_admin_1/', views.create_reservation_from_admin_1, name='create_reservation_from_admin_1'),

    path('create_reservation_from_admin_2/<str:customer_pk>/<str:car_pk>/', views.create_reservation_from_admin_2, name='create_reservation_from_admin_2'),

    path('update_reservation_from_admin_1/<str:reservation_pk>/', views.update_reservation_from_admin_1, name='update_reservation_from_admin_1'),

    path('update_reservation_from_admin_2/<str:reservation_pk>/', views.update_reservation_from_admin_2, name='update_reservation_from_admin_2'),

    path('delete_reservation_from_admin/<str:pk>/', views.delete_reservation_from_admin, name='delete_reservation_from_admin'),

]