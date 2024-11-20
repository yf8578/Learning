"""
URL configuration for djackets_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

# 在 Django 项目中，urls.py 文件的作用是定义 URL 路由配置。这个文件告诉 Django，当用户访问某个 URL 时，该执行哪个视图函数或视图类。
# 每个 Django 项目通常会有一个主 urls.py 文件，而每个应用也可以有自己的 urls.py 文件。通过这种方式，可以使 URL 配置更加模块化和易于管理。
# 项目的主 urls.py 文件，它包含了对 Django 管理后台和其他应用 URL 配置的路由
urlpatterns = [
    path('admin/', admin.site.urls),#将 /admin/ 路径映射到 Django 管理后台。
    path('api/v1/',include('djoser.urls')),#path('api/v1/', include('djoser.urls')) 和 path('api/v1/', include('djoser.urls.authtoken'))：包括 djoser 提供的认证相关 URL。
    path('api/v1/',include('djoser.urls.authtoken')),
    path('api/v1/',include('product.urls')),#将 /api/v1/ 路径下的 URL 映射到 product 应用的 urls.py 文件中的 URL 配置。

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)#配置媒体文件的 URL 路径，使它们在开发环境下可访问。
