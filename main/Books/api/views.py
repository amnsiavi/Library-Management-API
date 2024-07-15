from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes


from Users.permissions import LibrarianPerm, MemberPerm
from Books.models import LibraryModel
from Books.api.serializers import LibraryModelSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated,LibrarianPerm])
@authentication_classes([JWTAuthentication])
def add_book(request):
    
    try:
        if request.user:
            if len(request.data) == 0:
                return Response({'errors':'Recieved Empty Object'},status=status.HTTP_400_BAD_REQUEST)
            serializer = LibraryModelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Book Added'},status=status.HTTP_201_CREATED)
            else:
                return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    except ValidationError as ve:
        return Response({'errors':ve.detail},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated,LibrarianPerm|MemberPerm])
@authentication_classes([JWTAuthentication])
def get_books(request):
    
    try:
        instance = LibraryModel.objects.all()
        serializer = LibraryModelSerializer(instance,many=True)
        return Response({'books':serializer.data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated,LibrarianPerm|MemberPerm])
@authentication_classes([JWTAuthentication])
def get_book(request):
    
    try:
        if request.user:
            if 'ISBN' not in request.query_params:
                return Response({'errors':'ISBN is required'},status=status.HTTP_400_BAD_REQUEST)
            ISBN = request.query_params['ISBN']
            instance = LibraryModel.objects.filter(ISBN=ISBN).first()
            serializer = LibraryModelSerializer(instance)
            return Response({'book':serializer.data},status=status.HTTP_200_OK)
            
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE','PUT','PATCH'])
@permission_classes([IsAuthenticated,LibrarianPerm])
@authentication_classes([JWTAuthentication])
def update_delete_books(request):
    
    try:
        if request.method == 'DELETE':
            if 'ISBN' not in request.query_params:
                return Response({'errors':'ISBN is required'},status=status.HTTP_400_BAD_REQUEST)
            ISBN = request.query_params.get('ISBN')
            instance = LibraryModel.objects.filter(ISBN=ISBN).first()
            instance.delete()
            return Response({'msg':'Book Removed'},status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            if 'ISBN' not in request.query_params:
                return Response({'errors':'ISBN is required'},status=status.HTTP_400_BAD_REQUEST)
            ISBN = request.query_params.get('ISBN')
            instance = LibraryModel.objects.filter(ISBN=ISBN).first()
            serializer = LibraryModelSerializer(instance,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Book Updated'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'PATCH':
            if 'ISBN' not in request.query_params:
                return Response({'errors':'ISBN ID is required'},status=status.HTTP_400_BAD_REQUEST)
            ISBN = request.query_params.get('ISBN')
            instance = LibraryModel.objects.filter(ISBN=ISBN).first()
            serializer = LibraryModelSerializer(instance,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data},status=status.HTTP_200_OK)
            else:
                return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            
            
    except ValidationError as ve:
        return Response({'errors':ve.detail},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    