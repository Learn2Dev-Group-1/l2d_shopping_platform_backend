from django.db import models
import uuid

from catalog_api.models import Product

# Create your models here.


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class CartItems(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='cartitems'
    )
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Cart Items"
