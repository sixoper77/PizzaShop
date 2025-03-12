from django.urls import path
from . import  views
app_name='api'
urlpatterns = [
    path('get-products/',views.get_products,name='get-products')
]
