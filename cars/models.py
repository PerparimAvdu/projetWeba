from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User


class Article(models.Model):
    Titre = models.CharField(max_length=100, null=True, blank=True)
    Texte = models.TextField(null=True, blank=True)


class Brand(models.Model):
    name = models.CharField(max_length=200)
    brand_image = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name


class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    model = models.CharField(max_length=200)
    max_speed = models.CharField(max_length=200)
    description = models.TextField()
    car_image1 = models.ImageField(null=True, blank=True)
    car_image2 = models.ImageField(null=True, blank=True)
    car_image3 = models.ImageField(null=True, blank=True)
    car_image4 = models.ImageField(null=True, blank=True)
    buy_date = models.DateField(null=True, blank=True)
    transmission = models.CharField(max_length=200, null=True, blank=True)
    carburant = models.CharField(max_length=200, null=True, blank=True)
    consumption = models.CharField(max_length=200, null=True, blank=True)
    price_categories = models.ManyToManyField('Price_category', through='Price', blank=True)

    @property
    def image1(self):
        try:
            url = self.car_image1.url
        except:
            url = ''
        return url

    @property
    def image2(self):
        try:
            url = self.car_image2.url
        except:
            url = ''
        return url

    @property
    def image3(self):
        try:
            url = self.car_image3.url
        except:
            url = ''
        return url

    @property
    def image4(self):
        try:
            url = self.car_image4.url
        except:
            url = ''
        return url

    @property
    def get_reservation_car_detail(self):
        prices = self.price_set.all()

        return ''

    def __str__(self):
        return self.model


class Price_category(models.Model):
    nb_hours = (
        ('4h', '4h'),
        ('6h', '6h'),
        ('12h', '12h'),
        ('24h', '24h'),
        ('Week-end', 'Week-end'),
    )
    nb_kms = (
        ('150 kms', '150 kms'),
        ('200 kms', '200 kms'),
        ('350 kms', '350 kms'),
        ('500 kms', '500 kms'),
        ('900 kms', '900 kms'),
        ('illimited kms', 'illimited kms'),
    )
    hours = models.CharField(max_length=40, null=True, blank=True, choices=nb_hours)
    kms = models.CharField(null=True, blank=True, max_length=40, choices=nb_kms)

    def __str__(self):
        return f' {self.kms} for {self.hours}'


class Price(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    price_category = models.ForeignKey(Price_category, on_delete=models.SET_NULL, null=True, blank=True)
    car_price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.price_category.hours} {self.price_category.kms} = {self.car_price} Chf'

'''
    def __str__(self):
        return self.car_price
        '''

