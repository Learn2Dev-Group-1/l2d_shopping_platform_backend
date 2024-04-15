from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    is_available = models.BooleanField()
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    category = TreeForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
