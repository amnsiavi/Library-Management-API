from rest_framework.permissions import BasePermission, IsAuthenticated

class AdminPerm(BasePermission):
    
    def has_permission(self,request,view):
        return request.user and request.user.is_staff and IsAuthenticated().has_permission(request,view)

class LibrarianPerm(BasePermission):
    
    def has_permission(self, request, view):
        return request.user and not request.user.is_superuser and IsAuthenticated().has_permission(request,view)

class MemberPerm(BasePermission):
    def has_permission(self, request, view):
        return request.user and not request.user.is_superuser and IsAuthenticated().has_permission(request,view)

class BaseAuthModelUser(BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser and IsAuthenticated().has_permission(request,view)
    