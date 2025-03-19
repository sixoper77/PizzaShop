from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from main.models import Products,Category
from cart.cart import Cart
from .serializers import ProductsSerializer,CategorySerializer,CartSerializer,OrderItemSerializer,OrderSerializer
from users.models import User
from decimal import Decimal
from orders.models import Order,OrderItem
@api_view(['GET'])
def get_products(request,category_slug=None):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Products.objects.filter(category=category)
        serializer=ProductsSerializer(products,many=True,context={'request':request})
    else:
        serializer=ProductsSerializer(Products.objects.all(),many=True,context={'request':request})
    return Response(serializer.data)

@api_view(['GET'])
def get_categories(request):
    category=Category.objects.all()
    serializer=CategorySerializer(category,many=True,context={'request':request})
    return Response(serializer.data)

@api_view(['POST'])
def add_to_cart(request):
    telegram_id=request.query_params.get('telegram_id')
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)
    product = get_object_or_404(Products, id=product_id)
    
    cart = Cart(request,telegram_id=telegram_id)
    cart.add(product=product, quantity=int(quantity))
    request.session.save()
    total_price = Decimal(cart.get_total_price()).quantize(Decimal('0.01'))

    return Response({'message': 'Товары добавлены в корзину', 'cart_total': str(total_price)})

@api_view(['GET'])
def show_cart(request):
    telegram_id=request.query_params.get('telegram_id')
    cart = Cart(request,telegram_id=telegram_id)
    serialized_items = []
    for item in cart:
        product = item['product']
        serialized_items.append({
            'id': product.id,
            'name': product.name,
            'price': item['price'],
            'image_url': request.build_absolute_uri(product.image.url) if product.image else None,
            'quantity': item['quantity'],
            'total_price': item['total_price']
        })

    return Response({'cart': serialized_items, 'total_price': cart.get_total_price()})

@api_view(['GET','POST'])
def clear_cart(request):
    telegram_id=request.query_params.get('telegram_id')
    cart=Cart(request,telegram_id=telegram_id)
    cart.clear()
    return Response({'message':'корзина очищена'})

@api_view(['POST'])
def save_telegram_id(request):
    telegram_id=request.data.get('telegram_id')
    username=request.data.get('username')
    if not telegram_id:
        return Response({'message':'Ошибка '})
    else:
        user,created=User.objects.get_or_create(telegram_id=telegram_id,defaults={'username':username})
    return Response({'message:':'Telegram id сохранен','id':user.id})

@api_view(['POST'])
def order(request):
    telegram_id = request.query_params.get('telegram_id')
    if not telegram_id:
        return Response({"error": "Не указан telegram_id"}, status=400)
    cart = Cart(request=None, telegram_id=telegram_id)
    if not cart.cart:
        return Response({"error": "Корзина пуста"}, status=400)
    order_data = {
        'user': request.data.get('user'),
        'first_name': request.data.get('first_name'),
        'last_name': request.data.get('last_name'),
        'email': request.data.get('email'),
        'city': request.data.get('city'),
        'address': request.data.get('address'),
        'postal_code': request.data.get('postal_code'),
    }
    
    order_serializer = OrderSerializer(data=order_data)
    if order_serializer.is_valid():
        order = order_serializer.save()
    else:
        return Response(order_serializer.errors, status=400)
    order_items = []
    for item in cart:
        order_item = {
            "order": order.id,
            "product": item["product"].id,
            "price": item["price"],
            "quantity": item["quantity"]
        }
        order_items.append(order_item)
    order_item_serializer = OrderItemSerializer(data=order_items, many=True)
    if order_item_serializer.is_valid():
        order_item_serializer.save()
    else:
        order.delete()
        return Response(order_item_serializer.errors, status=400)
    cart.clear()
    
    return Response({"order_id": order.id, "status": "success"})
    
    