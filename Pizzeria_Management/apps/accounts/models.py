
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import User, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
import re

from rest_framework.authtoken.models import Token

from Pizzeria_Management import settings


class AccountManager(BaseUserManager):

    def create_user(self, password=None, **kwargs):

        account = self.model(
            email=kwargs.get('email'),

        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, password, **kwargs):

        account = self.create_user(password, **kwargs)

        account.is_admin = True
        account.is_superuser = True
        account.is_staff = True
        account.save()

        return account


class Account(PermissionsMixin, AbstractBaseUser):

    email = models.EmailField(verbose_name=('email address'), max_length=255, unique=True)
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('staff status', default=False)
    is_admin = models.BooleanField(default=False)

    date_joined = models.DateTimeField('date joined', default=timezone.now)

    #TODO add last_logged field

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = 'Konto'
        verbose_name_plural = 'Konta'


    def __str__(self):
        return str(self.id) + " " + self.email


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):

    if created:
        Token.objects.create(user=instance)


def validate_postal_code(value):
    pattern = re.compile('^\\d{2}[- ]{0,1}\\d{3}$')
    if not pattern.match(value):
        raise ValidationError('Invalid format, should be XX-XXX')



class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    phone_number = PhoneNumberField()

    def __str__(self):
        return str(self.user.email)

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profile'


@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Account)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Profile)
def create_profile_address(sender, instance, created, **kwargs):
    if created:
        Address.objects.create(profile=instance)



class Address(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)
    city = models.CharField(max_length=30, null=True, blank=False)
    zip_code = models.CharField(max_length=10, null=True, blank=False, validators=[validate_postal_code])
    street = models.CharField(max_length=30, null=True, blank=False)
    house_number = models.SmallIntegerField(null=True, blank=False)
    flat_number = models.SmallIntegerField(null=True, blank=True)

    type_choices = (
        ('HM', 'Home'),
        ('WRK', 'Work'),
        ('OTHER', 'Other')
    )

    address_type = models.CharField(max_length=20, choices=type_choices, default='HOME', null=True, blank=False)

    class Meta:

        verbose_name = 'Adres'
        verbose_name_plural = 'Adresy'



