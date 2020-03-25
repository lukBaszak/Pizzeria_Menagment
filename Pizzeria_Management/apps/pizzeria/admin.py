from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe
from imagekit.admin import AdminThumbnail

from Pizzeria_Management.apps.pizzeria.models import Pizza, Topping, PizzaSize, PizzaOrder, Item, ToppingRecipe, Order, \
    ItemOrder

from nested_inline.admin import NestedStackedInline, NestedModelAdmin

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
    verbose_name = "additional Topping"


class PizzaOrderInLine(NestedStackedInline):
    model = PizzaOrder
    extra = 1

    inlines = [PizzaToppingsTwoInline]

class OrderAdmin(NestedModelAdmin):
    model = Order

    inlines = [
        PizzaOrderInLine,

    ]

admin.site.register(Order, OrderAdmin)

