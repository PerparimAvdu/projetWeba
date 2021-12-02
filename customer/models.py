from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser

''' a tester pour le fixtures always create a custom user model in the beginning of the projet
class CustomUser(AbstractUser):
    is_client = models.BooleanField(default=False, null=True, blank=True)
    is_employe = models.BooleanField(default=False, null=True, blank=True)
'''


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True, unique=True)
    profile_pic = models.ImageField(default="tn_cool.jpg", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    @property
    def profileURL(self):
        try:
            url = self.profile_pic.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.email