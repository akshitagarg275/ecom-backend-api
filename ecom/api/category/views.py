from django.shortcuts import render
from .models import Category
from .serializers import CategorySerializer
from rest_framework import viewsets
'''
1) what is query(data to bring from DB)
2) serialized the data into json
'''

class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all().order_by('name')
    serializer_class=CategorySerializer