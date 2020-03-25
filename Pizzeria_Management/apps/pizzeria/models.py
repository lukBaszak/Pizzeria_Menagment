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




class Topping(models.Model):
    name = models.CharField(max_length=30, unique=True)
    unit_price = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Składnik'
        verbose_name_plural = 'Składniki'


class Pizza(models.Model):
    name = models.CharField(max_length=30, unique=True)
    toppings = models.ManyToManyField(Topping)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Pizza'
        verbose_name_plural = 'Pizze'




class ToppingRecipe(models.Model):

    pizza_order = models.ForeignKey('PizzaOrder', related_name='topping_amounts', on_delete=models.SET_NULL, null=True)

    topping = models.ForeignKey('Topping', related_name='topping_amounts', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Składnik')
    amount = models.IntegerField(default=0, verbose_name='Ilość')

    class Meta:
        verbose_name_plural = 'Dodatki'
        verbose_name = 'Dodatek'

    def total_price(self):
        return self.topping.unit_price * self.amount

    def __str__(self):
        return str(self.amount) + ' ' + self.topping.name


class PizzaSize(models.Model):
    choices = (
        ('SM', '20 (small)'),
        ('MD', '31 (medium)'),
        ('BG', '40 (big)'),
        ('FM', '51 (family size)')
    )

    size = models.CharField(choices=choices, max_length=30)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, )
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.pizza.name + ' ' + self.size


class Item(models.Model):

    name = models.CharField(max_length=30, unique=True)
    unit_price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Danie'
        verbose_name_plural = 'Dania'

class Order(models.Model):

    NOTPAID = 0
    PAID = 1
    PARTPAID = 2

    PAYMENT_STATUS = (
        (NOTPAID, 'Not Paid'),
        (PARTPAID, 'Partial Paid'),
        (PAID, 'Paid'),
    )

    payment_status = models.IntegerField(default=NOTPAID, choices=PAYMENT_STATUS, null=False)
    lock = models.BooleanField(default=False, null=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    time = models.DateTimeField(auto_now=True)


    total_price = models.DecimalField(max_digits=6, decimal_places=2)


    def subtotal(self):
        total = Decimal('0.00').quantize(Decimal('0.01'))
        for item in self.orderitems.all().filter(status=True):
            total = total + Decimal(item.subtotal()).quantize(Decimal('0.01'))
        return str(total)

    def total(self):
        total = Decimal('0.00').quantize(Decimal('0.01'))
        for item in self.orderitems.all().filter(status=True):
            total = total + Decimal(item.total()).quantize(Decimal('0.01'))
        return str(total - self.discount)


    class Meta:
        verbose_name = 'Zamówienie'
        verbose_name_plural = 'Zamówienia'


class PizzaOrder(models.Model):

    order = models.ForeignKey(Order, on_delete=models.PROTECT, null=True, verbose_name='Zamówienie')

    choices = (
        ('SM', '20 (small)'),
        ('MD', '31 (medium)'),
        ('BG', '40 (big)'),
        ('FM', '51 (family size)')
    )

    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, null=False, blank=True)
    pizza_quantity = models.SmallIntegerField(default=1, verbose_name='Ilość')
    pizza_size = models.CharField(choices=choices, max_length=30, null=False, blank=True)
    additional_toppings = models.ManyToManyField(Topping, through='ToppingRecipe')

    total_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    #TODO ogarnąć te ceny z kosmosu

    def save(self, *args, **kwargs):
        self.total_price = PizzaSize.objects.get(size=self.pizza_size,pizza__name=self.pizza.name).unit_price * self.pizza_quantity
        super(PizzaOrder, self).save(*args, **kwargs)

    def subtotal(self):
        total = ((self.price * Decimal(self.pizza_quantity)).quantize(
            Decimal('0.01')) - self.discount)
        return str(total)

    def taxtotal(self):
        subtotal = Decimal(self.subtotal()).quantize(Decimal('0.01'))
        total = subtotal * self.tax
        return str(Decimal(total).quantize(Decimal('0.01')))

    def total(self):
        total = Decimal(self.subtotal()).quantize(Decimal('0.01')) + Decimal(
            self.taxtotal()).quantize(Decimal('0.01'))
        return str(total)

    class Meta:
        verbose_name = 'Zamówienie (Pizza)'
        verbose_name_plural = 'Zamówienia (Pizza)'

    def __str__(self):
        return str(self.pizza_quantity) + 'x ' + self.pizza.name




class ItemOrder(models.Model):

    order = models.ForeignKey(Order, on_delete=models.PROTECT,
                              related_name='orderitems', null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()

    def __str__(self):
        return str(self.quantity) + 'x' + ' ' + self.item.name

    class Meta:
        verbose_name = 'Zamówienie (Danie)'
        verbose_name_plural = 'Zamówienia (Dania)'



