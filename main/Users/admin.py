from django.contrib import admin
from Users.models import BaseAuthModel, AdminUser, LibrarianUser, MemberUser
# Register your models here.
admin.site.register(BaseAuthModel)
admin.site.register(AdminUser)
admin.site.register(LibrarianUser)
admin.site.register(MemberUser)

