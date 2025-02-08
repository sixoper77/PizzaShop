from django.db import models
from django.db import models

from main.models import Products
from users.models import User

class Order(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.SET_DEFAULT,blank=True,null=True,default=None)
    first_name=models.CharField(max_length=225)
    last_name=models.CharField(max_length=225)
    email=models.EmailField()
    city=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    postal_code=models.CharField(max_length=255)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now=True)
    paid=models.BooleanField(default=False)
    
    class Meta:
        ordering=['-created']
        indexes=[
            models.Index(fields=['-created'])
        ]
    
    def __str__(self):
        return f'Order {self.id}'
    
    def get_total_const(self):
        return sum(item.get_const() for item in self.items.all())

class OrderItem(models.Model):
    order=models.ForeignKey(Order,related_name='item',on_delete=models.CASCADE)
    product=models.ForeignKey(Products,related_name='order_items',on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.PositiveBigIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)
    
    def get_const(self):
        return self.price*self.quantity
