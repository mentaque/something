from rest_framework import serializers

from shop.models import Shoe, Cart, CartItem


class ShoeSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField(source='name.brand.title')
    name = serializers.StringRelatedField()
    price = serializers.IntegerField(source='price.price')


    class Meta:
        model = Shoe
        fields = ['brand', 'name', 'size', 'description', 'price', 'in_stock']


class CartItemSerializer(serializers.ModelSerializer):
    shoe = serializers.StringRelatedField(source='shoe.name')
    price = serializers.SerializerMethodField()
    size = serializers.IntegerField(source='shoe.size')

    class Meta:
        model = CartItem
        fields = ['shoe', 'size', 'quantity', 'price']

    def get_price(self, obj):
        return obj.shoe.price.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']
