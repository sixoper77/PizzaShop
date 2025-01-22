from django.shortcuts import render,get_object_or_404
from .models import Products,Category

def popular_list(request):
    products=Products.objects.filter(available=True)[:3]
    return render(request,'main/index.html',{'products':products})

def producr_detail(request,slug):
    product=get_object_or_404(Products,slug=slug,available=True)
    
    return render(request,'main/detail.html',{'product':product})
    

