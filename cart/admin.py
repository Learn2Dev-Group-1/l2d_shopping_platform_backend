from django.contrib import admin
from .models import Cart, CartItems

# Register your models here.


class CartAdmin(admin.ModelAdmin):
    model = Cart


class CartItemsAdmin(admin.ModelAdmin):
    model = CartItems


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItems, CartItemsAdmin)
