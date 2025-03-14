from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from main.models import Products,Category
from .serializers import ProductsSerializer,CategorySerializer
# АПИ ДЛЯ БОТА СТАРТ
@api_view(['GET'])
def get_products(request,category_slug=None):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Products.objects.filter(category=category)
        serializer=ProductsSerializer(products,many=True,context={'request':request})
    else:
        products=Products.objects.all()
        serializer=ProductsSerializer(products,many=True,context={'request':request})
    return Response(serializer.data)

@api_view(['GET'])
def get_categories(request):
    category=Category.objects.all()
    serializer=CategorySerializer(category,many=True,context={'request':request})
    return Response(serializer.data)


