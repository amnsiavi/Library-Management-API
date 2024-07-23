from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import csv
from Users.permissions import LibrarianPerm, MemberPerm
from Books.models import LibraryModel, Book_Issue
from Books.api.serializers import LibraryModelSerializer, BookIssueSerializer
from Users.models import MemberUser


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
    
    


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated,LibrarianPerm])
def book_issue(request):
    
    try:
        if request.user:
            if 'ISBN' not in request.query_params:
                return Response({'errors':'ISBN not provided'},status=status.HTTP_400_BAD_REQUEST)
            if 'member_id' not in request.query_params:
                return Response({'errors':'Member ID not Provided'},status=status.HTTP_400_BAD_REQUEST)
            if len(request.data) == 0:
                return Response({'errors':'Recieved Empty Objects'},status=status.HTTP_400_BAD_REQUEST)
            if 'ISBN' and 'member_id' in request.query_params:
                ISBN = request.query_params.get('ISBN')
                member_id = request.query_params.get('member_id')
                book = LibraryModel.objects.filter(ISBN=ISBN).first()
                member = MemberUser.objects.filter(member_id=member_id).first()
                
                if book.quantity <= 0:
                    return Response({'errors':'No copies of book avaliable'},status=status.HTTP_400_BAD_REQUEST)
                
                if book.avaliable and member.active:
                    serializer = BookIssueSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.validated_data['books'] = book
                        serializer.validated_data['member'] = member
                        serializer.save()
                        
                        book.quantity -= 1
                        book.save()
                        return Response({'msg':'Book Issued'},status=status.HTTP_200_OK)
                    else:
                        return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
                    
                
                
            else:
                return Response({'errors':'ISBN and MEMBER ID not provided'})
    except ValidationError as ve:
        return Response({'errors':ve.detail},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def get_issued_books(request):
    
    try:
        instance = Book_Issue.objects.all()
        serializer = BookIssueSerializer(instance,many=True)
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errors':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET','DELETE', 'PUT', 'PATCH'])
@permission_classes([])
@authentication_classes([])
def deleted_issued_book(request, pk):
    
    try:
        if request.method == 'DELETE':
            instance = Book_Issue.objects.get(pk=pk)
            instance.delete()
            return Response({'Issued Book Deleted From Reccord'}, status=status.HTTP_200_OK)
        elif request.method == 'GET':
            instance = Book_Issue.objects.get(pk=pk)
            serializer = BookIssueSerializer(data=request.data)
            return Response({'data':serializer.data},status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            instance = Book_Issue.objects.get(pk=pk)
            serializer = BookIssueSerializer(instance,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Reccord Updated'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'PATCH':
            instance = Book_Issue.objects.get(pk=pk)
            serializer = BookIssueSerializer(instance,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Reccord Updated'},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errors':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
@authentication_classes([])  # Add authentication classes if needed
@permission_classes([])       # Add permission classes if needed
def pdf_report_view(request):
    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()
    
    # Create a canvas object and set up the PDF
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Fetch data from the database
    books = LibraryModel.objects.all()
    
    # Set up some basic PDF formatting
    p.setTitle("Library Report")
    p.setFont("Helvetica", 12)
    
    # Define starting position
    y = height - 40
    
    # Draw a title
    p.drawString(30, y, "Library Report")
    y -= 40
    
    # Draw table headers
    p.drawString(30, y, "ISBN")
    p.drawString(150, y, "Title")
    p.drawString(350, y, "Available Copies")
    y -= 20
    
    # Draw table rows
    for book in books:
        p.drawString(30, y, str(book.ISBN))
        p.drawString(150, y, book.title)
        p.drawString(350, y, str(book.quantity))
        y -= 20
    
    # Save the PDF
    p.showPage()
    p.save()
    
    # Return the PDF response
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf', headers={'Content-Disposition': 'attachment; filename="library_report.pdf"'})
     


@api_view(['GET'])
@authentication_classes([])  # Add authentication classes if needed
@permission_classes([])       # Add permission classes if needed
def csv_report_view(request):
    # Create an HTTP response with CSV content
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="library_report.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['ISBN', 'Title', 'Available Copies'])

    # Fetch data from the database
    books = LibraryModel.objects.all()

    # Write data rows
    for book in books:
        writer.writerow([book.ISBN, book.title, book.quantity])

    return response