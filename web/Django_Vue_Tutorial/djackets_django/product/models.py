from io import BytesIO #处理字节数据
from PIL import Image #处理图像

from django.core.files import File # 处理文件对象
from django.db import models # 定义数据库表和字段

class Category(models.Model):
    name = models.CharField(max_length=255)# 存储分类的名称，最大长度为 255 个字符
    slug = models.SlugField() #存储URL友好的文本，通常是分类名称的简化版本
    
    class Meta: #定义模型的元数据
        ordering = ('name',)#设置默认按照name字段进行升序排列
        
    def __str__(self): #定义模型实例的字符串表示，返回分类名称
        return self.name
    
    def get_absolute_url(self): #返回分类的绝对 URL，格式为 /{self.slug}/
        return f'/{self.slug}/'

class Product(models.Model):
    category=models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)#一个 ForeignKey 字段，建立与 Category 模型的外键关系
    # related_name='products'：通过这个反向关系名，可以通过 Category 实例访问相关的 Product 实例集合。
    # on_delete=models.CASCADE：定义了当关联的 Category 实例被删除时，所有与之关联的 Product 实例也会被删除。
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description=models.TextField(blank=True,null=True)
    price=models.DecimalField(max_digits=6,decimal_places=2)
    image=models.ImageField(upload_to='uploads/',blank=True,null=True)
    thumbnail=models.ImageField(upload_to='uploads/',blank=True,null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-date_added',)
            
    def __str__(self):#返回产品名称
        return self.name
    
    def get_absolute_url(self):#产品的绝对 URL，格式为 /{self.category.slug}/{self.slug}/。
        return f'/{self.category.slug}/{self.slug}/'
    
    
    def get_image(self): #返回产品图片的完整 URL
        if self.image:
            return 'http://127.0.0.1:8000'+self.image.url
        return ''
    
    def get_thumbnail(self):#返回产品缩略图的完整 URL,如果没有缩略图但有图片，则生成缩略图并保存。
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail=self.make_thumbnail(self.image)
                self.save()
                
                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''
            
    def make_thumbnail(self,image,size=(300,200)):#生成缩略图并返回一个文件对象
        img=Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io=BytesIO()#创建一个内存中的二进制流
        img.save(thumb_io,'JPEG',quality=85)#将缩略图保存到二进制流中
        thumbnail=File(thumb_io,name=image.name)#将二进制流转换为 Django 文件对象
        return thumbnail
    