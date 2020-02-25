from django.contrib import admin

# Register your models here.
from Pizzeria_Management.apps.accounts.models import Profile, Address

admin.site.register(Profile)
admin.site.register(Address)