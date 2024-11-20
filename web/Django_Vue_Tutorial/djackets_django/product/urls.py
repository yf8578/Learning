"""
Author: zhangyifan1
Date: 2024-06-12 01:08:19
LastEditors: zhangyifan1 zhangyifan1@genomics.cn
LastEditTime: 2024-06-12 10:14:34
FilePath: //Django_Vue_Tutorial//djackets_django//product//urls.py
Description: 

"""

from django.urls import path, include

# from views import LatestProductsList
from product import views

# 定义了一个 URL 路由，该路由映射到你的 LatestProductsList 视图。这段代码确保了当用户访问 latest-products/ URL 时，Django 会调用 LatestProductsList 视图并返回响应
# 当你访问 http://127.0.0.1:8000/latest-products/ 时，这个 URL 路由会触发 LatestProductsList 视图，并返回最新的产品列表。具体来说，这段代码实现了一个简单的 API 端点，用于返回前 4 个产品的信息，序列化为 JSON 格式。
urlpatterns = [
    path(
        "latest-products/", views.LatestProductsList.as_view()
    ),  # 调用 LatestProductsList 视图的 as_view() 方法，将其转换为可以处理请求的视图函数。
    path("products/<slug:category_slug>/<slug:product_slug>",views.ProductDetail.as_view()),
]
