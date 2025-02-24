from django.shortcuts import render,get_object_or_404
from .models import Products,Category
from django.core.paginator import Paginator
from cart.forms import CartAddProductForm
from .utils import *
def popular_list(request):
    products=Products.objects.filter(available=True)[:3]
    return render(request,'main/index.html',{'products':products})

def producr_detail(request,slug):
    product=get_object_or_404(Products,slug=slug,available=True)
    cart_product_form=CartAddProductForm
    return render(request,'main/detail.html',{'product':product,'cart_product_form':cart_product_form})
def product_list(request, category_slug=None):
    query = request.GET.get('q', None)
    page = request.GET.get('page', 1)
    category = None
    categories = Category.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Products.objects.filter(category=category)
    elif query:
        products = q_search(query)
    else:
        products = Products.objects.all()
    paginator = Paginator(products, 5)
    current_page = paginator.get_page(page)
    # print(products)
    print(request.GET)
    return render(request, 'main/list.html', {
        'category': category,
        'categories': categories,
        'products': current_page,
        'slug_url': category_slug
    })
