from rest_framework import serializers
from .models import Category,Product
class ProductSerializer(serializers.ModelSerializer):# ProductSerializer：这是一个继承自 serializers.ModelSerializer 的序列化器类。ModelSerializer 是一个快捷方式，可以自动生成用于序列化和反序列化模型实例的序列化器。
    class Meta:
        model=Product #model：指定与这个序列化器关联的模型。在这里是 Product 模型。
        fields=(#指定要包含在序列化器中的模型字段
            'id',
            'name',
            'get_absolute_url',
            'description',
            'price',
            'get_image',
            'get_thumbnail'
        )