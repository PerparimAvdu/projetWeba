from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from cars.models import Price
from login_settings.decorators import admin_only, allowed_user
from customer.forms import NewUserForm
from .forms import *
from .filters import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@login_required(login_url='login')
@admin_only
def dashboard(request):
    reservations = Reservation.objects.all().order_by('-date_created')
    customers = Customer.objects.all()
    total_customers = customers.count()

    # creating a paginator with 1 customer per page
    paginator_customers = Paginator(customers, 5)
    # getting the desired page number from url
    page_number_customers = request.GET.get('customers_page')
    # return the desired page object
    page_obj_customers = paginator_customers.get_page(page_number_customers)

    paginator_reservations = Paginator(reservations, 5)
    page_number_reservations = request.GET.get('reservations_page')
    page_obj_reservations = paginator_reservations.get_page(page_number_reservations)

    total_reservations = reservations.count()
    delivered = reservations.filter(status='Delivered').count()
    pending = reservations.filter(status='Pending').count()
    canceled = reservations.filter(status='Canceled').count()

    context = {'reservations': reservations, 'customers': customers, 'total_reservations': total_reservations, 'delivered': delivered, 'pending': pending, 'canceled': canceled, 'page_obj_customers': page_obj_customers, 'total_customers': total_customers, 'page_obj_reservations': page_obj_reservations}

    return render(request, 'reservations_management/dashboard.html', context)


@login_required(login_url='login')
@admin_only
def all_customers_from_admin(request):
    customers = Customer.objects.all()
    total_customers = customers.count()

    # creating a paginator with 1 customer per page
    paginator_customers = Paginator(customers, 5)
    # getting the desired page number from url
    page_number_customers = request.GET.get('customers_page')
    # return the desired page object
    page_obj_customers = paginator_customers.get_page(page_number_customers)

    context = {'customers': customers, 'page_obj_customers': page_obj_customers, 'total_customers': total_customers}

    return render(request, 'reservations_management/all_customers_from_admin.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customer_profile_from_admin(request, pk):
    customer = Customer.objects.get(id=pk)

    reservations = customer.reservation_set.all()
    reservation_count = reservations.count()

    myFilter = ReservationFilter(request.GET, queryset=reservations)
    reservations = myFilter.qs

    context = {'customer': customer, 'reservations': reservations, 'reservation_count': reservation_count, 'myFilter': myFilter}
    return render(request, 'reservations_management/customer_profile_from_admin.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def delete_customer_from_admin(request, pk):
    customer = Customer.objects.get(pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.warning(request, f'{customer} has beed deleted !')
        return redirect('reservations_management:dashboard')
    else:
        context = {'customer': customer}
        return render(request, 'reservations_management/delete_customer_admin.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def create_reservation_from_admin_1(request):
    customers = Customer.objects.all()
    cars = Car.objects.all()
    if request.method == 'POST':
        form = request.POST
        customer_pk = form['customer_id']
        car_pk = form['car_id']
        return redirect("reservations_management:create_reservation_from_admin_2", customer_pk, car_pk)

    context = {'cars': cars, 'customers': customers}
    return render(request, 'reservations_management/reservation_from_admin_car.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def create_reservation_from_admin_2(request, customer_pk, car_pk):
    car_price = Price.objects.all().filter(car=car_pk)
    customer = Customer.objects.get(pk=customer_pk)
    car = Car.objects.get(pk=car_pk)
    form = ReservationFormFromAdmin2()

    # I have to reformat fields in modelform
    # For the datetime i need a calendar

    context = {'car_price': car_price, 'customer': customer, 'car': car, 'form': form}

    if request.method == 'POST':
        form = ReservationFormFromAdmin2(request.POST)
        normalform = request.POST
        if form.is_valid():
            Reservation.objects.create(
                customer=customer,
                car=car,
                hours_kms_price=normalform['hours_kms_price'],
                status=form.cleaned_data.get('status'),
                note=form.cleaned_data.get('note'),
                date_location_start=form.cleaned_data.get('date_location_start'),
            )

            date_location = form.cleaned_data.get('date_location_start')
            status = form.cleaned_data.get('status')
            note = form.cleaned_data.get('note')
            hours_kms_price = normalform['hours_kms_price']

            contextformail = {'date_location': date_location, 'status': status, 'note': note, 'hours_kms_price': hours_kms_price, 'customer': customer, 'car': car}

            subject = f'Your reservation for {car}'
            html_message = render_to_string('reservations_management/reservation_confirm_mail.html', contextformail)
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to_email = customer.email

            # date_location_start = form.cleaned_data.get('date_location_start')
            # status = form.cleaned_data.get('status')
            # hours_kms_price = form['hours_kms_price']
            # note = form.cleaned_data.get('note')
            # if note == '':
            #     note = ''
            # else:
            #     note = f"Comment : {note}"
            #
            # subject = f'Your reservation for car {car}'
            # body = {
            #     'note': form.cleaned_data.get('note'),
            # }
            # message = "\n".join(body.values())

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

            messages.success(request, f'reservation for {customer} is done !')
            return redirect('reservations_management:dashboard')

        else:
            return HttpResponse('Invalid form.')

    return render(request, 'reservations_management/reservation_from_admin_price.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def update_reservation_from_admin_1(request, reservation_pk):
    reservation = Reservation.objects.get(pk=reservation_pk)
    form = ReservationFormFromAdmin1(instance=reservation)
    if request.method == 'POST':
        form = ReservationFormFromAdmin1(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect("reservations_management:update_reservation_from_admin_2", reservation_pk=reservation.pk)

    else:
        context = {'form': form}
        return render(request, 'reservations_management/update_reservation_from_admin_1.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def update_reservation_from_admin_2(request, reservation_pk):
    reservation = Reservation.objects.get(pk=reservation_pk)
    car = reservation.car
    customer = reservation.customer
    form = ReservationFormFromAdmin2(instance=reservation)
    car_price = Price.objects.all().filter(car=car.pk) # car in red must be the name in the Price field
    if request.method == 'POST':
        form = ReservationFormFromAdmin2(request.POST, instance=reservation)
        normalform = request.POST
        if form.is_valid():
            form.save()

        status = form.cleaned_data.get('status')
        date_location = form.cleaned_data.get('date_location_start')
        note = form.cleaned_data.get('note')
        hours_kms_price = normalform['hours_kms_price']


        # if status == 'Confirmed':
        contextformail = {'date_location': date_location, 'status': status, 'note': note, 'hours_kms_price': hours_kms_price, 'customer': customer, 'car': car}

        subject = f'Your reservation update'
        html_message = render_to_string('reservations_management/reservation_confirm_mail.html', contextformail)
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to_email = customer.email

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

        messages.success(request, f'Update done for {customer} !')
        return redirect("reservations_management:dashboard")

    else:
        context = {'form': form, 'car_price': car_price, 'car': car}
        return render(request, 'reservations_management/update_reservation_from_admin_2.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def delete_reservation_from_admin(request, pk):
    reservation = Reservation.objects.get(id=pk)
    if request.method == "POST":
        reservation.delete()
        return redirect('reservations_management:dashboard')

    context = {'reservation': reservation}
    return render(request, 'reservations_management/delete_reservation.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def create_customer_from_admin(request):
    form = NewUserForm()
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'New account created {username}')
            return redirect('reservations_management:dashboard')
        else:
            for msg in form.error_messages:
                messages.error(request, f'{msg} : {form.error_messages[msg]}')
            return render(request, 'reservations_management/create_customer.html', {'form': form})

    else:
        return render(request, 'reservations_management/create_customer.html', {'form': form})

