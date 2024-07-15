from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes


from Users.permissions import AdminUser, LibrarianUser, MemberUser
from Books.models import LibraryModel
from Books.api.serializers import LibraryModelSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated,AdminUser|LibrarianUser|MemberUser])
@authentication_classes([JWTAuthentication])
def add_book(request):
    
    try:
        if request.user:
            if len(request.data) == 0:
                return Response({'errors':'Recieved Empty Object'},status=status.HTTP_400_BAD_REQUEST)
            serializer = LibraryModelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(member=request.user)
                return Response({'msg':'User Created'},status=status.HTTP_201_CREATED)
            else:
                return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    except ValidationError as ve:
        return Response({'errors':ve.detail},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


