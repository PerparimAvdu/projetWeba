from django.db import models
from django.utils import timezone
from customer.models import Customer
from cars.models import Car

STATUS = [
    ('Confirmed', 'Confirmed'),
    ('Pending', 'Pending'),
    ('Delivered', 'Delivered'),
    ('Canceled', 'Canceled'),
]


class Reservation(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    car = models.ForeignKey(Car, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # auto_now_add=True   each time a new object is created it set a date
    #date_modified....
    status = models.CharField(max_length=200, null=True, blank=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True, blank=True)
    #date_location_start = models.DateField(default=timezone.now, null=True, blank=True)
    date_location_start = models.DateTimeField(default=timezone.now, null=True, blank=True)
    hours_kms_price = models.CharField(max_length=100, null=True, blank=True)
    #hours_kms_price = models.CharField(max_length=200, null=True, blank=True)
    #hours = models.TimeField(null=True, blank=True)
    # kms = models.IntegerField(null=True, blank=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return f'{self.car}'





