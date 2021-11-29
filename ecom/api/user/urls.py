from django.urls import path,include
from rest_framework import routers
from . import views

# 127.0.0.1:8000/api/user
# 127.0.0.1:8000/api/user/signin
# 127.0.0.1:8000/api/user/signout

router=routers.DefaultRouter()
router.register('',views.UserViewSet)

urlpatterns = [
    path('login/',views.signin,name="signin"),
    path('signout/<str:id>/',views.signout,name="signout"),
    path('',include(router.urls))
]

