from django.contrib import admin
from .models import *
from .forms import *
from django.contrib.auth.admin import UserAdmin

'''
class CustomerUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationFom

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User role',
            {
                'fields': (
                    'is_director',
                    'is_producer',
                )
            }
        )
    )

admin.site.register(CustomUser, CustomerUserAdmin)
'''

admin.site.register(Customer)