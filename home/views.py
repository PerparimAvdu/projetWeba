from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import *
from cars.models import Car
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def homepage(request):
    cars = Car.objects.all()
    context = {'cars': cars}
    return render(request, 'home/homepage.html', context)


def about_us(request):
    context = {}
    return render(request, 'home/about_us.html', context)


def contact_us(request):
    if request.method == "POST":
        form = request.POST
        Contact.objects.create(
            name=form['name'],
            email=form['email'],
            phone=form['phone'],
            message=form['message'],
        )

        name = form['name']
        email = form['email']
        phone = form['phone']
        message = form['message']

        contextformail = {'name': name, 'email': email, 'phone': phone, 'message': message}

        subject = f'Message from {name} from the contact form'
        html_message = render_to_string('home/contact_mail_sent.html', contextformail)
        plain_message = strip_tags(html_message)
        from_email = email
        to_email = settings.EMAIL_HOST_USER

        try:
            send_mail(
                subject,
                plain_message,
                from_email,
                [to_email],
                html_message=html_message,
                fail_silently=False
            )
        except BadHeaderError:
            return HttpResponse('Invalid header found')

        messages.success(request, 'Your message has been sent to an admin !')
        return redirect('home:homepage')

    return render(request, 'home/contact_us.html')

def recherche(request, insert):
    cars = Brand.objects.filter(name__icontains=insert)
    items = {"item": []}
    for car in cars:
        items["item"].append(car.name)
    time.sleep(5)
    return JsonResponse({'items': items})


# Another way to send mail
# send_mail(
#         subject,
#         form['message'] + '\n from \n' + form['email'],
#         settings.EMAIL_HOST_USER,
#         #[form['email']],
#         ['GentilleOurson@gmail.com'],
#         fail_silently=False
#     )
