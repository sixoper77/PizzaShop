from django.urls import path
from . import  views
app_name='api'
urlpatterns = [
    path('get-products/<slug:category_slug>/',views.get_products,name='get-products'),
    path('get-products/',views.get_products,name='get-products'),
    path('get_categories/',views.get_categories,name='get_categories'),
]
