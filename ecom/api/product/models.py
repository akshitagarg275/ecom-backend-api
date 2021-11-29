from django.db import models
from django.db.models.deletion import SET_NULL
from api import category
from api.category.models import Category 
# Create your models here.

class Product(models.Model):
    name=models.CharField(max_length=150)
    description=models.CharField(max_length=250)
    stock=models.CharField(max_length=10)
    price=models.CharField(max_length=10)
    is_active=models.BooleanField(default=False,blank=True,null=True)
    image=models.ImageField(upload_to='images/')
    category=models.ForeignKey(Category,on_delete=SET_NULL,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name