from rest_framework.serializers import ModelSerializer



from Books.models import LibraryModel




class LibraryModelSerializer(ModelSerializer):
    
    class Meta:
        model = LibraryModel
        fields = ['ISBN','title','author','synopsis','genre','publication_year','quantity','avaliable']
        