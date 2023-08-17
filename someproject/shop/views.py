from django.db.models import Prefetch
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from my_auth.models import CustomUser
from shop.models import Shoe, Cart, CartItem
from shop.serializers import ShoeSerializer, CartSerializer


class ShoeView(ListAPIView):
    serializer_class = ShoeSerializer
    queryset = Shoe.objects.all().select_related('name__brand', 'price')


class CartDetailView(APIView):
    def get(self, request, user_id):
        cart = Cart.objects.prefetch_related(
            Prefetch('items__shoe', Shoe.objects.all().select_related('name__brand', 'price')),
        ).get(user_id=user_id)
        serializer = CartSerializer(cart)
        return Response(serializer.data)