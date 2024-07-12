from rest_framework.permissions import BasePermission, IsAuthenticated

class AdminUser(BasePermission):
    
    def has_permission(self,request,view):
        return request.user and request.user.is_staff and IsAuthenticated().has_permission(request,view)

class LibrarianUser(BasePermission):
    
    def has_permission(self, request, view):
        return request.user and not request.user.is_superuser and IsAuthenticated().has_permission(request,view)

class MemberUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and not request.user.is_superuser and IsAuthenticated().has_permission(request,view)

class BaseAuthModelUser(BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser and IsAuthenticated().has_permission(request,view)
    