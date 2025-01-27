from django.urls import path
from . import views

app_name="main"
urlpatterns = [
    path('',views.popular_list,name='popular_list'),
    path('<slug:slug>/',views.producr_detail,name='product_detail'),
]
