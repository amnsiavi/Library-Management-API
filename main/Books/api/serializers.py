from rest_framework.serializers import ModelSerializer, SerializerMethodField



from Books.models import LibraryModel, Book_Issue




class LibraryModelSerializer(ModelSerializer):
    
    class Meta:
        model = LibraryModel
        fields = ['ISBN','title','author','synopsis','genre','publication_year','quantity','avaliable']
        

class BookIssueSerializer(ModelSerializer):
    
    book_title = SerializerMethodField()
    member_name = SerializerMethodField()
    
    class Meta:
        model = Book_Issue
        fields = ['issue_date','return_date','book_title','member_name']
        
    def get_book_title(self,obj):
        return obj.books.title if obj.books else None
    
    def get_member_name(self,obj):
        return obj.member.member_name if obj.member else None
    

        