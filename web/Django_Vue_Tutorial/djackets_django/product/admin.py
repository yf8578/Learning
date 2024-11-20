"""
Author: zhangyifan1
Date: 2024-06-11 22:51:53
LastEditors: zhangyifan1 zhangyifan1@genomics.cn
LastEditTime: 2024-06-12 10:38:53
FilePath: //Django_Vue_Tutorial//djackets_django//product//admin.py
Description: 

"""

from django.contrib import admin

# Register your models here.
from .models import Category, Product


# admin.site.register(Category)
# admin.site.register(Product)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'date_added')
    search_fields = ('name', 'description')
    list_filter = ('category', 'date_added')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
