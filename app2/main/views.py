from django.shortcuts import render,get_object_or_404
from .models import Products,Category
from django.core.paginator import Paginator
def popular_list(request):
    products=Products.objects.filter(available=True)[:3]
    return render(request,'main/index.html',{'products':products})

def producr_detail(request,slug):
    product=get_object_or_404(Products,slug=slug,available=True)
    
    return render(request,'main/detail.html',{'product':product})
def product_list(request,category_slug=None):
    # получаем страницу
    page=request.GET.get('page',1)
    category=None
    products=Products.objects.all()
    # создание пагинатора
    paginator=Paginator(products,5)
    # задаю страницу
    current_page=paginator.page(int(page))
    categories=Category.objects.all()
    if category_slug:
        category=get_object_or_404(Category,slug=category_slug)
        paginator=Paginator(products.filter(category=category),5)
        current_page=paginator.page(int(page))
    return render(request,'main/list.html',{'category':category,
                                            'categories':categories,
                                            'products':current_page,
                                            'slug_url':category_slug})