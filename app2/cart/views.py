from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_POST
from main.models import Products
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def card_add(request,product_id):
    cart=Cart(request)
    product=get_object_or_404(Products,id=product_id)

# Create your views here.
