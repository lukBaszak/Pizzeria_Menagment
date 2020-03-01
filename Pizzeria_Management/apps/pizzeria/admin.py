from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe
from imagekit.admin import AdminThumbnail

from Pizzeria_Management.apps.pizzeria.models import Pizza, Topping, PizzaSize, PizzaOrder, Item, ToppingRecipe

admin.site.register(Topping)
admin.site.register(Item)




class PizzaSizeInline(admin.TabularInline):
    model = PizzaSize
    max_num = 4

class PizzaAdmin(admin.ModelAdmin):

    readonly_fields = ["pizza_imag",]

    def pizza_imag(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.pizza_image.url,
            width=obj.pizza_image.width,
            height=obj.pizza_image.height,
            )
    )

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
