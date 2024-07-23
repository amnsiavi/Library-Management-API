from django.urls import path
from Books.api.views import (add_book,get_books,get_book, book_issue, get_issued_books, deleted_issued_book, pdf_report_view, csv_report_view)


urlpatterns = [
    path('create/',add_book,name='add_book'),
    path('list/',get_books,name='get_books'),
    path('',get_book,name='get_book'),
    path('issue/',book_issue,name='book_issue'),
    path('issue/list',get_issued_books,name='get_issued_books'),
    path('issue/<int:pk>', deleted_issued_book,name='get_deleted_book'),
    path('pdf-report',pdf_report_view, name='pdf_report_view'),
    path('csv-report',csv_report_view, name='csv_report_view'),
    
    
]