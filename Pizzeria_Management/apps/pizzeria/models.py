from django.db import models


# Create your models here.
from django.utils.safestring import mark_safe


class Topping(models.Model):
    name = models.CharField(max_length=30, unique=True)
    unit_price = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=30, unique=True)
    pizza_image = models.ImageField(upload_to='pizza_photos/', default='pizza_photos/index.jpeg')
    toppings = models.ManyToManyField(Topping)

    def image_tag(self):
        if self.pizza_image:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.pizza_image.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'

    def __str__(self):
        return self.name


class PizzaOrder(models.Model):

    choices = (
        ('SM', '20 (small)'),
        ('MD', '31 (medium)'),
        ('BG', '40 (big)'),
        ('FM', '51 (family size)')
    )

    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, null=False, blank=True)
    pizza_quantity = models.SmallIntegerField(default=1)
    pizza_size = models.CharField(choices=choices, max_length=30, null=False, blank=True)
    additional_toppings = models.ManyToManyField(Topping, through='ToppingRecipe')

    total_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total_price = PizzaSize.objects.get(size=self.pizza_size,pizza__name=self.pizza.name).unit_price * self.pizza_quantity
        super(PizzaOrder, self).save(*args, **kwargs)


class ToppingRecipe(models.Model):

    pizza_order = models.ForeignKey('PizzaOrder', related_name='topping_amounts', on_delete=models.SET_NULL, null=True)
    topping = models.ForeignKey('Topping', related_name='topping_amounts', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Toppings'
        verbose_name = 'Topping'

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



