from decimal import Decimal

from django.db import models

from Pizzeria_Management.apps.accounts.models import Account
from Pizzeria_Management.apps.pizzeria.models.dishes import PizzaSize, Pizza, Topping, Item


class Order(models.Model):

    user = models.ForeignKey(Account, on_delete=models.CASCADE,null=True)

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
    created = models.DateTimeField(auto_now_add=True, null=True)
    time = models.DateTimeField(auto_now=True)


    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)


    def total(self):

        total = Decimal('0.00').quantize(Decimal('0.01'))

        for pizza_order in self.pizza_order_items.all():
            total = total + Decimal(pizza_order.subtotal()).quantize(Decimal('0.01'))

        for item_order in self.item_orders_items.all():
            total = total + Decimal(item_order.subtotal()).quantize(Decimal('0.01'))

        return total-self.discount

    def save(self, *args, **kwargs):
        self.total_price = self.total()
        super(Order, self).save(*args, **kwargs)



    class Meta:
        verbose_name = 'Zamówienie'
        verbose_name_plural = 'Zamówienia'


class PizzaOrder(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, verbose_name='Zamówienie', related_name='pizza_order_items')

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


    def save(self, *args, **kwargs):
        self.total_price = PizzaSize.objects.get(size=self.pizza_size,pizza__name=self.pizza.name).unit_price * self.pizza_quantity
        super(PizzaOrder, self).save(*args, **kwargs)

    def subtotal(self):
        total = 0

        total = ((PizzaSize.objects.get(pizza=self.pizza, size=self.pizza_size).unit_price * Decimal(self.pizza_quantity)).quantize(
            Decimal('0.01')))
        return str(total)

    def taxtotal(self):
        subtotal = Decimal(self.subtotal()).quantize(Decimal('0.01'))
        total = subtotal * 0.23
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
                              related_name='item_orders_items', null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()

    def __str__(self):
        return str(self.quantity) + 'x' + ' ' + self.item.name

    def subtotal(self):
        total = ((self.item.unit_price * Decimal(
            self.quantity)).quantize(
            Decimal('0.01')))
        return str(total)

    def taxtotal(self):
        subtotal = Decimal(self.subtotal()).quantize(Decimal('0.01'))
        total = subtotal * 0.23
        return str(Decimal(total).quantize(Decimal('0.01')))

    def total(self):
        total = Decimal(self.subtotal()).quantize(Decimal('0.01')) + Decimal(
            self.taxtotal()).quantize(Decimal('0.01'))
        return str(total)

    class Meta:
        verbose_name = 'Zamówienie (Danie)'
        verbose_name_plural = 'Zamówienia (Dania)'

