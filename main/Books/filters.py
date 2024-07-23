import django_filters
from Books.models import LibraryModel


class BookFilter(django_filters.FilterSet):
    
    ISBN = django_filters.CharFilter(lookup_expr='exact')
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(lookup_expr='icontains')
    genre = django_filters.CharFilter(lookup_expr='icontains')
    publication_year = django_filters.DateFilter(lookup_expr='icontains')
    avaliable = django_filters.BooleanFilter()
    
    class Meta:
        model = LibraryModel
        fields = ['ISBN','title','author','genre','publication_year','avaliable']
    