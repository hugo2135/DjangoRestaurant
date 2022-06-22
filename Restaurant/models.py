from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating


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
    
    Rating = GenericRelation(Rating, related_query_name='foos')
    
    def __str__(self):
        return self.Name
    
