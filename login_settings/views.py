import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .decorators import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import *
from django.forms import inlineformset_factory
from django.urls import reverse
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from customer .forms import *
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@unauthenticated_user
def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account Created: {username}")
            login(request, user)

            contextformail = {'username': username}

            subject = f'New account created at 44Location.'
            html_message = render_to_string('login_settings/register_confirm_mail.html', contextformail)
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to_email = user.email

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

            messages.info(request, f"You are now logged in as: {username}")
            return redirect("home:homepage")
        else:
            # We have to override the passwordvalidator
            # for msg in form.error_messages:
            #     messages.error(request, f"{msg}: {form.error_messages[msg]}")
            return render(request, "login_settings/register.html", {'form': form})
    else:
        form = NewUserForm
        return render(request, "login_settings/register.html", {'form': form})


@unauthenticated_user
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            user = authenticate(username=username, password=password, email=email)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    messages.info(request, f"You are now logged in as {username}")
                    return redirect("reservations_management:dashboard")
                else:
                    messages.info(request, f"You are now logged in as {username}")
                    return redirect("home:homepage")
            else:
                messages.error(request, "Invalid username or password")
                form = AuthenticationForm()
                return render(request, "login_settings/login.html", {"form": form})
        else:
            messages.error(request, "Invalid username or password")
            form = AuthenticationForm()
            return render(request, "login_settings/login.html", {"form": form})
    else:
        form = AuthenticationForm()
        return render(request, "login_settings/login.html", {"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home:homepage")


@unauthenticated_user
def password_reset_request(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_user = User.objects.filter(Q(email=data))
            if associated_user.exists():
                for user in associated_user:
                    subject = "Password Reset Requested"
                    email_template_name = "login_settings/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '44location.pythonanywhere.com',
                        'site_name': '44Location',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'GentilleOurson@gmail.com', [user.email], fail_silently=False)
                    except BadHeaderError:

                        return HttpResponse('Invalid header found')

                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("/password_reset_done/")

            messages.error(request, 'An invalid email has been entered.')

    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="login_settings/password_reset.html", context={"password_reset_form": password_reset_form})









