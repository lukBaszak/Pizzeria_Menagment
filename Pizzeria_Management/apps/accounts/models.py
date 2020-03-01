from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
import re


def validate_postal_code(value):
    pattern = re.compile('^\\d{2}[- ]{0,1}\\d{3}$')
    if not pattern.match(value):
        raise ValidationError('Invalid format, should be XX-XXX')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    phone_number = PhoneNumberField()

    def __str__(self):
        return str(self.user.username)


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
        verbose_name_plural = 'Addresses'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Profile)
def create_profile_address(sender, instance, created, **kwargs):
    if created:
        Address.objects.create(profile=instance)
