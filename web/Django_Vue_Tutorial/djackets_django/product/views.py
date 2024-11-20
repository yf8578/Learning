"""
Author: zhangyifan1
Date: 2024-06-11 22:51:53
LastEditors: zhangyifan1 zhangyifan1@genomics.cn
LastEditTime: 2024-06-12 10:09:34
FilePath: //Django_Vue_Tutorial//djackets_django//product//views.py
Description: 

"""
# from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView#导入 APIView，用于创建基于类的视图
from rest_framework.response import Response#导入 Response 类，用于返回 API 响应。

from .models import Product
from .serializers import ProductSerializer

class LatestProductsList(APIView):#：继承自 APIView 的视图类，用于处理 HTTP GET 请求
    def get(self, request, format=None):
        products = Product.objects.all()[:4] #从数据库中获取前 4 个 Product 实例。objects.all() 获取所有产品实例，[:4] 切片操作获取前 4 个。
        serializer = ProductSerializer(products, many=True) #使用 ProductSerializer 将产品实例列表序列化。many=True 表示我们序列化的是一个产品列表。
        return Response(serializer.data)#return Response(serializer.data)：将序列化的数据作为响应返回。

class ProductDetail(APIView):
    def get_object(self,category_slug,product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
        
    def get(self,request,category_slug,product_slug,format=None):
        product=self.get_object(category_slug,product_slug)
        serializer=ProductSerializer(product)
        return Response(serializer.data)