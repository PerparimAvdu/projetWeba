from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from reservations_management.models import *
from .models import *
from django.db import models
from django.forms import ModelForm


''' A tester pour le fixture
class CustomUserCreationFom(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
'''


# Permet de créer un formulaire qui va reprendre le formulaire de base de Django
# pour y ajouter un champ email qui sera obligatoire afin de rajouter tous ces champs
# au model User prédéfini de Django
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


# Permet de créer un formulaire sans le customiser en reprenant directement
# le formulaire de base de Django et en y ajoutant la référance du model User de
# Django qui est aussi prédéfini
# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']


class ReservationFormByCustomer1(ModelForm):

    class Meta:

        model = Reservation
        fields = '__all__'
        exclude = ['date_location_start', 'hours_kms_price', 'note', 'customer', 'status', 'date_location_end']


class ReservationFormByCustomer2(ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'
        exclude = ['status', 'car', 'customer', 'date_location_end', 'hours_kms_price', 'date_location_start']







