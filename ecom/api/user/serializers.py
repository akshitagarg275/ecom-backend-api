from rest_framework import serializers
from .models import CustomUser

# allows to bring password in clear text or to hash the password
from django.contrib.auth.hashers import identify_hasher, make_password

from rest_framework.decorators import authentication_classes,permission_classes

class UserSerializer(serializers.HyperlinkedModelSerializer):
    def create(self,validated_data):
        password=validated_data.pop('password',None)
        instance=self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self,instance,validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance,attr,value)
        return instance

    class Meta:
        model=CustomUser
        extra_kwargs={'password':{'write_only':True}}
        fields=('name','email','password','phone','gender','is_active','is_superuser','is_staff')