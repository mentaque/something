from django.contrib import admin

from shop.models import Shoe, Brand, Name, ShoePrice, Cart, CartItem

admin.site.register(Shoe)
admin.site.register(Brand)
admin.site.register(Name)
admin.site.register(ShoePrice)
admin.site.register(Cart)
admin.site.register(CartItem)
