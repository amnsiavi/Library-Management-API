from django.urls import path

from Users.api.views import get_users_all, get_admins, create_admin, get_admin, create_librarian

urlpatterns = [
    
    # Super Admin Routes
    path('all/',get_users_all,name='get_users_all'),
    
    
    #Admin Routes OR URL PATTERNS
    path('admin/list',get_admins,name='get_admins'),
    path('admin/create',create_admin,name='create_admin'),
    path('admin/',get_admin,name='get_admin'),
    
    # Librarian User
    path('librarian/create',create_librarian,name='create_librarian'),
    
]
