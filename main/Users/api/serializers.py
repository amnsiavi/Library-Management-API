from rest_framework.serializers import ModelSerializer
from django.contrib.auth.hashers import make_password

from Users.models import (
    BaseAuthModel, AdminUser,
    LibrarianUser, MemberUser
)

class BaseAuthModelSerializer(ModelSerializer):
    
    class Meta:
        model = BaseAuthModel
        fields = ['id','username','email','password']

class AdminUserSerializer(ModelSerializer):
    
    class Meta:
        model = AdminUser
        fields = ['admin_id', 'admin_name', 'gender', 'email', 'username', 'password','is_staff']
    
    def create(self,validated_data):
        validated_data['is_staff'] = True
        return super().create(validated_data)
    
    def update(self,instance,validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().update(instance,validated_data)
    

class LibrarianUserSerializer(ModelSerializer):
    
    class Meta:
        model = LibrarianUser
        fields = ['librarian_id','librarian_name','gender','email','username','password']
        
    def update(self,instance,validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().update(instance,validated_data)

class MemberUserSerializer(ModelSerializer):
    
    class Meta:
        model = MemberUser
        fields = ['member_id','member_name','gender','email','username','password']
        