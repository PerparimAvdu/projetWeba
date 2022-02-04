from django.contrib import admin
from .models import *
from django.db import models


class CarAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Infos Cars', {'fields': ['brand', 'model', 'car_image1', 'car_image2', 'car_image3', 'car_image4', 'max_speed', 'consumption', 'buy_date', 'transmission', 'carburant']}),
        ('Content', {'fields': ['description']}),
    ]


admin.site.register(Car, CarAdmin)
admin.site.register(Brand)
admin.site.register(Price_category)
admin.site.register(Price)
admin.site.register(Article)
