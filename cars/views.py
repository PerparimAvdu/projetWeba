import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import *
from login_settings.decorators import allowed_user
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.forms import inlineformset_factory
from django.urls import reverse


def all_cars(request):
    brand = request.GET.get('brand')
    if brand == None:
        cars = Car.objects.all()
    else:
        cars = Car.objects.filter(brand__name=brand)

    brands = Brand.objects.all()
    context = {'brands': brands, 'cars': cars}

    return render(request, "cars/all_cars.html", context)


def car_detail(request, pk):
    car = Car.objects.get(id=pk)
    car_price = Price.objects.all().filter(car=pk)
    context = {'car': car, 'car_price': car_price}

    return render(request, "cars/car_detail.html", context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def add_car(request):
    brands = Brand.objects.all()

    if request.method == 'POST':
        data = request.POST
        car_image = request.FILES.get('car_image1')

        if data['brand'] != 'none':
            brand = Brand.objects.get(id=data['brand'])
        elif data['brand_new'] != '':
            brand, created = Brand.objects.get_or_create(name=data['brand_new'], brand_image=car_image)
        else:
            brand = None

        car = Car.objects.create(brand=brand,
                                description=data['description'],
                                car_image1=car_image,
                                buy_date=data['buy_date'],
                                carburant=data['carburant'],
                                transmission=data['transmission'],
                                consumption=data['consumption'],
                                max_speed=data['max_speed'],
                                model=data['model'],
                                )
        messages.success(request, f'A car has been added !')
        return redirect('cars:all_cars')

    context = {'brands': brands}

    return render(request, "cars/add_car.html", context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def update_car(request, pk):
    car = Car.objects.get(pk=pk)
    form = CarForm(instance=car)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            car = form.save(commit=False)
            car.car_image2 = form.cleaned_data.get('car_image2')
            car.save()
            messages.success(request, f'{car} has been updated !')
            return redirect('cars:all_cars')

    context = {'form': form}
    return render(request, 'cars/update_car.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def delete_car(request, pk):
    car = Car.objects.get(pk=pk)
    if request.method == 'POST':
        car.delete()
        messages.warning(request, f'{car} has been deleted')
        return redirect('cars:all_cars')

    context = {'car': car}
    return render(request, 'cars/delete_car.html', context)


def article(request):
    art = Article.objects.all()
    context = {'article': art}

    return render(request, 'cars/article.html', context)

