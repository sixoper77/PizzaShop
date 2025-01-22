from django.contrib import admin

from . models import Products,Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','slug']
    prepopulated_fields={'slug':('name',)}
    
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name','slug','price','available','created','updated','discount']
    list_filter = ['available','created','updated']
    list_editable = ['price','available','discount']
    prepopulated_fields = {'slug': ('name',)}  
    