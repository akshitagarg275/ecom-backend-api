from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from . import views

# 127.0.0.1:8000/api/category

router=routers.DefaultRouter()
router.register('',views.CategoryViewSet)

urlpatterns = [
    path('',include(router.urls))
]

