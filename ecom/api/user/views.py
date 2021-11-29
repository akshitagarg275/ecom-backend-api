from django.contrib.auth.models import Permission
from django.shortcuts import render
import random
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .models import CustomUser
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,logout
from django.http import JsonResponse
import re

def generate_session_token(length=10):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97,123)]+[str(i) for i in range(10)]) for _ in range(length))

@csrf_exempt
def signin(request):
    if not request.method == "POST":
        return JsonResponse({'ERROR': 'Send a post request with valid parameters'})
    
    username=request.POST['email']
    password=request.POST['password']

    if not re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$",username):
        return JsonResponse({'error':'Enter a valid email'})

    if len(password)<3 :
        return JsonResponse({'error':'Min password lengthshould be of 3 characters'})
    
    UserModel=get_user_model()

    try:
        user=UserModel.objects.get(email=username)
        if user.check_password(password):
            usr_dict = UserModel.objects.filter(
                email=username).values().first()
            usr_dict.pop('password')


            if user.session_token != '0':
                user.session_token='0'
                user.save()
                return JsonResponse({'INFO':'Previous session Exists'})

            token=generate_session_token()
            user.session_token=token
            user.save()
            login(request,user)
            return JsonResponse({'token':token,'user':usr_dict})
        else:
            return JsonResponse({'error':'Invalid Password'})
        
    except UserModel.DoesNotExist:
        return JsonResponse({'ERROR': 'Email does not exist'})

def signout(request,id):
    logout(request)

    UserModel=get_user_model

    try:
        user=UserModel.objects.get(pk=id)
        user.session_token='0'
        user.save()
    except UserModel.DoesNotExist:
        return JsonResponse({'error':'Invalid User ID'})
    
    return JsonResponse({'success':'User logout successfully'})

class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action={'create':[AllowAny]}

    queryset=CustomUser.objects.all().order_by('id')
    serializer_class=UserSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]