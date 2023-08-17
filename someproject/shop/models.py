
from django.db import models

from my_auth.models import CustomUser


class Brand(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Name(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=False, null=False)
    model = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.brand} {self.model}'


class ShoePrice(models.Model):
    name = models.ForeignKey(Name, on_delete=models.CASCADE, blank=False, null=False)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.name} {self.price}'


class Shoe(models.Model):
    SIZE_CHOICES = [
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
        ('39', '39'),
        ('40', '40'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'),
        ('44', '44'),
    ]
    name = models.ForeignKey(Name, on_delete=models.CASCADE, blank=False, null=False)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, blank=False, null=False)
    description = models.TextField()
    price = models.ForeignKey(ShoePrice, on_delete=models.CASCADE, blank=False, null=False)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - {self.size}' + ' в наличии' if self.in_stock else 'нет в наличии'

    class Meta:
        unique_together = ['name', 'size']


class CartItem(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE, blank=False, null=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.shoe.name} - {self.quantity}'

class Cart(models.Model):
    items = models.ManyToManyField(CartItem)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f'cart {self.user.username}'

