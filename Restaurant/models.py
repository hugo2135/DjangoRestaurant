from pyexpat import model
from django.db import models

class Restaurant(models.Model):
    STYLE_CHOICES = ()
    Name = models.CharField(max_length=50,
                            verbose_name='餐廳名字')
    
    Style = models.CharField(max_length=50,
                            # choices=STYLE_CHOICES,                            
                            verbose_name='餐廳類型')
    
    Price = models.DecimalField(max_digits=7,
                                decimal_places=1,
                                blank=True,
                                null=True,
                                verbose_name='價位')
    
    Img = models.ImageField(upload_to='Restaurant_Image/',
                            blank=True,
                            verbose_name='餐廳圖片')
    
    Distance = models.DecimalField(max_digits=7,
                                decimal_places=1,
                                blank=True,
                                null=True,
                                verbose_name='與學校距離')
    
    Address = models.CharField(max_length=50,
                            # choices=STYLE_CHOICES,                            
                            verbose_name='餐廳地址')
    
    Rating = models.DecimalField(max_digits=7,
                                decimal_places=1,
                                blank=True,
                                null=True,
                                verbose_name='評價')
    
    def __str__(self):
        return self.Name
    
# publishDate = models.DateTimeField(max_length=20,
#                                    default=timezone.now,
#                                    verbose_name='发布时间')
# views = models.PositiveIntegerField('浏览量', default=0)
# class ProductImg(models.Model):
#     product = models.ForeignKey(Product,
#                                 related_name='productImgs',
#                                 verbose_name='产品',
#                                 on_delete=models.CASCADE)
#     photo = models.ImageField(upload_to='Product/',
#                               blank=True,
#                               verbose_name='产品图片')