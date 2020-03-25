from django.contrib import admin

# Register your models here.
from Pizzeria_Management.apps.accounts.models import Profile, Address, Account

admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(Account)