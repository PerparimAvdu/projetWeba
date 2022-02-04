from django.forms import *

from cars.models import Price_category, Price
from .models import *
from django import forms


class ReservationFormFromAdmin1(ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'
        exclude = ['status', 'date_location_start', 'date_location_start', 'note', 'hours_kms_price',
                   'date_location_end']


class ReservationFormFromAdmin2(ModelForm):
    date_location_start = forms.DateTimeField(widget=DateTimeInput({'type': 'datetime-local'}))

    status = forms.ChoiceField(label='Choose a status', choices=STATUS)
    #hours_kms_price = forms.CharField(label='Current options', disabled=True)

    #NumberInput

    def save(self, commit=True):
        reservation = super(ReservationFormFromAdmin2, self).save(commit=False)
        reservation.date_location_start = self.cleaned_data['date_location_start']
        # reservation.note = self.cleaned_data['note']
        reservation.status = self.cleaned_data['status']
        if commit:
            reservation.save()
        return reservation

    class Meta:
        model = Reservation
        fields = '__all__'
        exclude = ['car', 'customer', 'hours_kms_price']

        #widgets = {'note': forms.Select(attrs={'class': 'status_reservation_admin'})}


class CategoryForm(ModelForm):
    class Meta:
        model = Price_category
        fields = '__all__'


class PriceForm(ModelForm):
    class Meta:
        model = Price
        fields = '__all__'
        exclude = ['car', 'price_category', ]


'''
class ReservationFormFromAdmin2(ModelForm):
    date_location_start = forms.DateTimeField(required=True)
    status = forms.CharField(required=True) # how to take back choice in model ?
    note = forms.CharField(required=True)

    def save(self, commit=True):
        reservation = super(ReservationFormFromAdmin2, self).save(commit=False)
        reservation.date_location_start = self.cleaned_data['date_location_start']
        reservation.status = self.cleaned_data['status']
        reservation.note = self.cleaned_data['note']
        if commit:
            reservation.save()
        return reservation

    class Meta:
        model = Reservation
        fields = '__all__'
        exclude = ['car', 'customer']


                widgets = {
                    'name': Textarea(attrs={'cols': 80, 'rows': 20}),
                }

        overriding modelform fields dont work
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['status'].widget.attrs.update(size='10')

'''
#
# date_location_start = forms.DateTimeField(input_formats='2006-10-25 14:30',
#                                           error_messages={'required': 'Choose an option'},
#                                           help_text='You have to choose a date',
#                                           widget=DateTimeInput(attrs={'id': 'testmagique', 'type': 'datetime-local'}))
#
# note = forms.CharField(error_messages={'required': 'put a note'}, initial='test again', help_text='Max 100 character',
#                        required=True)
#
# status = forms.ChoiceField(label='Choose a status', label_suffix=' =', choices=STATUS)
