from django.db import models


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

    pizza_order = models.ForeignKey('PizzaOrder', related_name='topping_amounts', on_delete=models.CASCADE, null=True)

    topping = models.ForeignKey('Topping', related_name='topping_amounts', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Składnik')
    amount = models.PositiveIntegerField(default=1, verbose_name='Ilość',null=True, blank=True )

    class Meta:
        verbose_name_plural = 'Dodatki'
        verbose_name = 'Dodatek'

    def total_price(self):
        return self.topping.unit_price * self.amount


class PizzaSize(models.Model):

    choices = (
        ('SM', '20 (small)'),
        ('MD', '31 (medium)'),
        ('BG', '40 (big)'),
        ('FM', '51 (family size)')
    )

    size = models.CharField(choices=choices, max_length=30)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name='pizza_size')
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
