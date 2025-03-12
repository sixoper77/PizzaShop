from rest_framework.response import Response
from rest_framework.decorators import api_view
from main.models import Products
from .serializers import ProductsSerializer
# АПИ ДЛЯ БОТА СТАРТ
@api_view(['GET'])
def get_products(request):
    products=Products.objects.all()
    serializer=ProductsSerializer(products,many=True)
    return Response(serializer.data)

