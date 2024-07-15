from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from Users.api.serializers import (
    BaseAuthModelSerializer, 
    LibrarianUserSerializer,
    AdminUserSerializer,
    MemberUserSerializer
)
from Users.permissions import AdminPerm, LibrarianPerm, MemberPerm, BaseAuthModelUser
from Users.models import  AdminUser, LibrarianUser, MemberUser, BaseAuthModel


# BASE AUTH MODEL USERS VIEWS
@api_view(['GET'])
@permission_classes([IsAuthenticated, BaseAuthModelUser])
@authentication_classes([JWTAuthentication])
def get_users_all(request):
    
    try:
        instance = BaseAuthModel.objects.all()
        serializer = BaseAuthModelSerializer(instance,many=True)
        return Response({'data':serializer.data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)






# ADMIN USERS VIEWS

@api_view(['GET'])
@permission_classes([IsAuthenticated, BaseAuthModelUser])
@authentication_classes([JWTAuthentication])
def get_admins(request):
    
    try:
        instance = AdminUser.objects.all()
        serializer = AdminUserSerializer(instance,many=True)
        return Response({'data':serializer.data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated, BaseAuthModelUser])
@authentication_classes([JWTAuthentication])
def get_admin(request):
    
    try:
        if request.method == 'GET':
            if not 'admin_id' in request.query_params:
                return Response({'errors':'Admin_Id is required in params'},status=status.HTTP_400_BAD_REQUEST)
            admin_id = request.request.query_params['admin_id']
            instance = AdminUser.objects.filter(admin_id=admin_id).first()
            serializer = AdminUserSerializer(instance)
            return Response({'data':serializer.data},status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            if not 'admin_id' in request.query_params:
                return Response({'errors':'Admin_ID required in params'},status=status.HTTP_400_BAD_REQUEST)
            admin_id = request.query_params['admin_id']
            instance = AdminUser.objects.filter(admin_id=admin_id).first()
            instance.delete()
            return Response({
                'msg':' Admin Removed Sucessfully',
            },status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            if request.user:
                if len(request.data) == 0:
                    return Response({'errors':'Recieved Empty Object'}, status=status.HTTP_400_BAD_REQUEST)
                if not 'admin_id' in request.query_params:
                    return Response({'errors':'Admin ID required in Params'},status=status.HTTP_400_BAD_REQUEST)
                admin_id = AdminUser.objects.filter(admin_id-admin_id).first()
                serializer = AdminUserSerializer(instance,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'msg':'Admin User Updated','data':serializer.data},status=status.HTTP_200_OK)
                else:
                    return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'PATCH':
                if request.user:
                    if len(request.data) == 0:
                        return Response({'errors':'Recieved Empty Objects'},status=status.HTTP_400_BAD_REQUEST)
                    if not 'admin_id' in request.query_params:
                        return Response({'errors':'Admin ID Required in Params'}, status=status.HTTP_400_BAD_REQUEST)
                    admin_id = request.query_params['admin_id']
                    instance = AdminUser.objects.filter(admin_id=admin_id).first()
                    serializer = AdminUserSerializer(instance,data=request.data,partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'msg':'User Updated','data':serializer.data},status=status.HTTP_200_OK)
                    else:
                        return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
                    
            
    except ValidationError as ve:
        return Response({'errors':ve.detail},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['POST'])
@permission_classes([IsAuthenticated, BaseAuthModelUser])
@authentication_classes([JWTAuthentication])
def create_admin(request):
    
    try:
        if request.user:
            if len(request.data) == 0:
                return Response({'errors':'Recieved Empty Object'},status=status.HTTP_400_BAD_REQUEST)
            serializer = AdminUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Admin Created'},status=status.HTTP_201_CREATED)
            else:
                return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            
    except ValidationError as ve:
        return Response({'errors':ve.detail},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



# Librarian Routes
@api_view(['POST'])
@permission_classes([IsAuthenticated,AdminPerm])
@authentication_classes([JWTAuthentication])
def create_librarian(request):
    
    try:
        if request.user:
            if len(request.data) == 0:
                return Response({'errors':'Recieved Empty Obejct'},status=status.HTTP_400_BAD_REQUEST)
            serializer = LibrarianUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Librarian Created'},status=status.HTTP_201_CREATED)
            else:
                return Response({'errors':serializer.errors},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except ValidationError as ve:
        return Response({'errors':ve.detail},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, AdminPerm|LibrarianPerm])
@authentication_classes([JWTAuthentication])
def get_librarians(request):
    
    try:
        instance = LibrarianUser.objects.all()
        serilaizer = LibrarianUserSerializer(instance,many=True)
        return Response({'data':serilaizer.data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated,AdminPerm|LibrarianPerm])
@authentication_classes([JWTAuthentication])
def get_librarian(request):
    
    try:
        if request.method == 'GET':
            if 'librarian_id' not in request.query_params:
                return Response({'errors':'Librarin ID is required'},status=status.HTTP_400_BAD_REQUEST)
            librarian_id = request.query_params.get('librarian_id')
            instance = LibrarianUser.objects.filter(librarian_id= librarian_id).first()
            serializer = LibrarianUserSerializer(instance)
            return Response({'data':serializer.data},status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            if request.user:
                if 'librarian_id' not in request.query_params:
                    return Response({'errors':'Libraribian ID is required'},status=status.HTTP_400_BAD_REQUEST)
                if len(request.data) == 0:
                    return Response({'errors':'Revieved Empty Object'},status=status.HTTP_400_BAD_REQUEST)
                librarian_id = request.query_params.get('librarian_id')
                instance = LibrarianUser.objects.filter( librarian_id= librarian_id).first()
                serializer = LibrarianUserSerializer(instance,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'msg':'Librarian Updated'},status=status.HTTP_200_OK)
                else:
                    return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            if request.user:
                if 'librarian_id' not in request.query_params:
                    return Response({'errors':'Librian ID is required'},status=status.HTTP_400_BAD_REQUEST)
                librarian_id = request.query_params.get('librarian_id')
                instance = LibrarianUser.objects.filter( librarian_id= librarian_id).first()
                instance.delete()
                return Response({'Librarian Deleted'},status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            if request.user:
                if 'librarian_id' not in request.query_params:
                    return Response({'errors':'Librarian ID is required'},status=status.HTTP_400_BAD_REQUEST)
                librarian_id = request.query_params.get('librarian_id')
                instance = LibrarianUser.objects.filter(librarian_id=librarian_id).first()
                serializer = LibrarianUserSerializer(instance,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'Librarian Updated'},status=status.HTTP_200_OK)
                else:
                    return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
    except ValidationError as ve:
        return Response({"errors":ve.detail},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"errors":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# Member Routes
@api_view(['POST'])
@permission_classes([IsAuthenticated,LibrarianPerm])
@authentication_classes([JWTAuthentication])
def create_member(request):
    
    try:
        if request.user:
            if len(request.data) == 0:
                return Response({'errors':'Recieved Empty Objects'},status=status.HTTP_400_BAD_REQUEST)
            serializer = MemberUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Member Created'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    except ValidationError as ve:
        return Response({'errors':ve.detail},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated,AdminPerm|LibrarianPerm])
@authentication_classes([JWTAuthentication])
def get_memebers(request):
    
    try:
        instance = MemberUser.objects.all()
        serilaizer = MemberUserSerializer(instance,many=True)
        return Response({'data':serilaizer.data},status=status.HTTP_200_OK)
        
            
    except ValidationError as ve:
        return Response({'errors':ve.detail},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated,LibrarianPerm])
@authentication_classes([JWTAuthentication])
def get_memeber(request):
    
    try:
        if request.method == 'GET':
            if request.user:
                if 'member_id' not in request.query_params:
                    return Response({'errors':'Member ID is required'},status=status.HTTP_400_BAD_REQUEST)
                member_id = request.query_params.get('member_id')
                instance = MemberUser.objects.filter(member_id=member_id).first()
                serilizer = MemberUserSerializer(instance)
                return Response({'data':serilizer.data},status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            if request.user:
                if len(request.data) == 0:
                    return Response({'errors':'Recieved Empty Object'},status=status.HTTP_400_BAD_REQUEST)
                if 'member_id' not in request.query_params:
                    return Response({'errors':'Member ID is required'},status=status.HTTP_400_BAD_REQUEST)
                instance = MemberUser.objects.filter(member_id=member_id).first()
                serializer = MemberUserSerializer(instance,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'msg':'Member Updated'},status=status.HTTP_200_OK)
                else:
                    return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'PATCH':
            if request.user:
                if len(request.data) == 0:
                    return Response({'errors':'Recieved Empty Object'},status=status.HTTP_400_BAD_REQUEST)
                if 'member_id' not in request.query_params:
                    return Response({'errors':'Member Id is required'})
                member_id = request.query_params.get('member_id')
                instance = MemberUser.objects.filter(member_id=member_id).first()
                serializer = MemberUserSerializer(instance,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'msg':'Member Updated'},status=status.HTTP_200_OK)
                else:
                    return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            if request.user:
                if 'member_id' not in request.query_params:
                    return Response({'errors':"Member ID is reqiured"},status=status.HTTP_400_BAD_REQUEST)
                member_id=request.query_params.get('member_id')
                instance = MemberUser.objects.filter(member_id=member_id)
                instance.delete()
                return Response({'msg':'Member Deleted'},status=status.HTTP_200_OK)
            
    except ValidationError as ve:
        return Response({'errors':ve.detail},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)