from main.models import Category, Products
from orders.models import Order, OrderItem
from rest_framework import serializers
from users.models import User


class ProductsSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ["id", "name", "description", "price", "image_url", "category"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CartProductsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    image_url = serializers.CharField()


class CartSerializer(serializers.Serializer):
    product = CartProductsSerializer
    quantity = serializers.IntegerField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["telegram_id"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"
