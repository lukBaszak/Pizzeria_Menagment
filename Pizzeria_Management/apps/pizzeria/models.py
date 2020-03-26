import datetime
import re
from decimal import Decimal

from django.db import models


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import ValidationError

from Pizzeria_Management.apps.accounts.models import Account






