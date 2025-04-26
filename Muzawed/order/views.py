from django.shortcuts import render
from django.http import HttpRequest
# Create your views here.
from .models import Product

def cart_view(request:HttpRequest):
    items =Product.objects.all()
    return render(request, "order/cart.html",{"items":items})
