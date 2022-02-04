from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

app_name = 'cars'

urlpatterns = [
    path('all_cars/', views.all_cars, name='all_cars'),
    path('car_detail/<str:pk>/', views.car_detail, name='car_detail'),
    path('add_car/', views.add_car, name='add_car'),
    path('update_car/<str:pk>/', views.update_car, name='update_car'),
    path('delete_car/<str:pk>/', views.delete_car, name='delete_car'),
    path('article/', views.article, name='article')
]