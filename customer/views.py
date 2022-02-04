import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib import messages
from reservations_management.filters import ReservationFilter
from login_settings.decorators import allowed_user
from cars.models import Car, Price
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, BadHeaderError


# from utils import date     dont work the thing with the date mock


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer', 'admin'])
def user_settings(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Update saved !')

    context = {'form': form, 'customer': customer}
    return render(request, 'customer/user_settings.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer', 'admin'])
def delete_account_from_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        logout(request)
        messages.warning(request, f"Account has been deleted !")
        return redirect("home:homepage")

    context = {'customer': customer}
    return render(request, 'customer/delete_account.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def customer_dashboard(request, customer_pk):
    customer = Customer.objects.get(id=customer_pk)

    reservations = customer.reservation_set.all().order_by('-date_created')
    reservation_count = reservations.count()

    myFilter = ReservationFilter(request.GET, queryset=reservations)
    reservations = myFilter.qs

    context = {'customer': customer, 'reservations': reservations, 'reservation_count': reservation_count,
               'myFilter': myFilter}
    return render(request, 'customer/customer_dashboard.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def create_reservation_from_customer(request, car_pk):
    car = Car.objects.get(pk=car_pk)
    car_price = Price.objects.all().filter(car=car_pk)
    customer = request.user.customer
    available_date_check = datetime.now().replace(microsecond=0).replace(second=0).isoformat()

    if request.method == 'POST':
        form = request.POST
        Reservation.objects.create(
            customer=customer,
            car=car,
            status='Pending',
            hours_kms_price=form['hours_kms_price'],
            note=form['note'],
            date_location_start=form['date_location_start'],
        )

        date_location = form['date_location_start']
        note = form['note']
        hours_kms_price = form['hours_kms_price']

        contextformail = {'date_location': date_location, 'note': note, 'hours_kms_price': hours_kms_price, 'customer': customer, 'car': car}

        subject = f'New reservation demand for {customer}'
        html_message = render_to_string('customer/reservation_created_mail.html', contextformail)
        plain_message = strip_tags(html_message)
        from_email = customer.email
        to_email = settings.EMAIL_HOST_USER

        try:
            send_mail(
                subject,
                plain_message,
                from_email,  # from email
                # [form['email']], another way to pick up the mail from a form
                [to_email],  # destination email
                html_message=html_message,
                fail_silently=False
            )
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

        messages.success(request, f'Your reservation for the {car} is done, you will receive a confirmation per mail in the next 24h !')
        return redirect('customer:customer_dashboard', customer_pk=customer.pk)

    else:
        context = {'car_price': car_price, 'car': car, 'customer': customer, 'available_date_check': available_date_check}
        return render(request, 'customer/reservation_from_customer.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def update_reservation_from_customer_1(request, reservation_pk):
    reservation = Reservation.objects.get(id=reservation_pk)
    form = ReservationFormByCustomer1(instance=reservation)
    if request.method == 'POST':
        form = ReservationFormByCustomer1(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect("customer:update_reservation_from_customer_2", reservation_pk=reservation.pk)

    else:
        context = {'form': form}
        return render(request, 'customer/update_reservation_from_customer_1.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def update_reservation_from_customer_2(request, reservation_pk):
    reservation = Reservation.objects.get(pk=reservation_pk)
    customer = request.user.customer
    car = reservation.car
    form = ReservationFormByCustomer2(instance=reservation)
    car_price = Price.objects.all().filter(car=car.pk) # car in red must be the name in the Price field
    available_date_check = datetime.now().replace(microsecond=0).replace(second=0).isoformat()
    if request.method == 'POST':
        form = ReservationFormByCustomer2(request.POST, instance=reservation)
        normalform = request.POST
        if form.is_valid():
            form.save()

        date_location = normalform['date_location_start']
        note = normalform['note']
        hours_kms_price = normalform['hours_kms_price']

        contextformail = {'date_location': date_location, 'note': note, 'hours_kms_price': hours_kms_price,
                          'customer': customer, 'car': car}

        subject = f'Reservation update for {customer}'
        html_message = render_to_string('customer/reservation_update_mail.html', contextformail)
        plain_message = strip_tags(html_message)
        from_email = customer.email
        to_email = settings.EMAIL_HOST_USER

        try:
            send_mail(
                subject,
                plain_message,
                from_email,  # from email
                # [form['email']], another way to pick up the mail from a form
                [to_email],  # destination email
                html_message=html_message,
                fail_silently=False
            )
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

        messages.success(request,
                         f'Your update for the {car} is done, you will receive a confirmation per mail in the next 24h !')
        return redirect('customer:customer_dashboard', customer_pk=customer.pk)

    else:
        context = {'form': form, 'car_price': car_price, 'car': car, 'reservation_pk': reservation_pk, 'customer': customer, 'available_date_check': available_date_check}
        return render(request, 'customer/update_reservation_from_customer_2.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def delete_reservation_from_customer(request, reservation_pk):
    reservation = get_object_or_404(Reservation, pk=reservation_pk)
    customer = reservation.customer
    if request.method == 'POST':
        reservation.delete()
        return redirect("customer:customer_dashboard", customer_pk=customer.pk)

    context = {'reservation': reservation, 'customer': customer}
    return render(request, 'customer/delete_reservation_from_customer.html', context)



 # # date_location_start = form['date_location_start']
        # # if date_location_start <= date.today():
        # #     raise ValidationError(_('Date should be in the future.'))
        #     # messages.warning(request, f'Select a futur date from now please')
        #     # redirect('customer:create_reservation_from_customer')
        # elif date_location_start > date.today():