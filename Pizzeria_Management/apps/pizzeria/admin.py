from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe
from imagekit.admin import AdminThumbnail


from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from Pizzeria_Management.apps.pizzeria.models.dishes import Topping, Item, PizzaSize, Pizza, ToppingRecipe
from Pizzeria_Management.apps.pizzeria.models.orders import ItemOrder, PizzaOrder, Order

admin.site.register(Topping)
admin.site.register(Item)
admin.site.register(ItemOrder)

class PizzaSizeInline(admin.TabularInline):
    model = PizzaSize
    max_num = 4

class PizzaAdmin(admin.ModelAdmin):

    inlines = [
        PizzaSizeInline

    ]

admin.site.register(Pizza, PizzaAdmin)


class PizzaToppingsInline(admin.TabularInline):
    model = ToppingRecipe
    verbose_name = "additional Topping"

class PizzaOrderAdmin(admin.ModelAdmin):

    inlines = [
        PizzaToppingsInline
    ]

admin.site.register(PizzaOrder, PizzaOrderAdmin)


class PizzaToppingsTwoInline(NestedStackedInline):
    model = ToppingRecipe
    extra = 0
    verbose_name = "additional Topping"


class PizzaOrderInLine(NestedStackedInline):
    model = PizzaOrder
    extra = 1

    inlines = [PizzaToppingsTwoInline]

class ItemInLine(NestedStackedInline):
    model = Item
    verbose_name = 'Danie'

class ItemOrderInLine(NestedStackedInline):
    model = ItemOrder

    inlines = [ItemInLine]

class OrderAdmin(NestedModelAdmin):
    model = Order
    readonly_fields = ['total_price']


    inlines = [
        PizzaOrderInLine,
        ItemOrderInLine

    ]



admin.site.register(Order, OrderAdmin)

