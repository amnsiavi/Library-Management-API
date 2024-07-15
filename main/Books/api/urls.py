from django.urls import path
from Books.api.views import (add_book,get_books,get_book)


urlpatterns = [
    path('create/',add_book,name='add_book'),
    path('list/',get_books,name='get_books'),
    path('',get_book,name='get_book'),
    
]