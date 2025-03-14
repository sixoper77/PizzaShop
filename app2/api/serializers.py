from rest_framework import serializers
from main.models import Products,Category

class ProductsSerializer(serializers.ModelSerializer):
    image_url=serializers.SerializerMethodField()
    class Meta:
        model=Products
        fields=['name','description','price','image_url','category']
    def get_image_url(self,obj):
        request=self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'