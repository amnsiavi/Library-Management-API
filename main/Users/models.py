from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class BaseAuthModel(AbstractUser):
    
    email = models.EmailField(unique=True,null=False,blank=False)
    username = models.CharField(max_length=100,unique=True,blank=False,null=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['username']
    
    def __str__(self):
        return self.username



class AdminUser(BaseAuthModel):
    
    GENDER_CHOICES = (
        ('M','Male'),
        ('F','Female')
    )
    
    class Meta:
        verbose_name = 'Admin User'
        verbose_name_plural = 'Admin Users'
    
    admin_id = models.CharField(max_length=10, unique=True, editable=False)
    admin_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
    
    def save(self,*args,**kwargs):
        if not self.admin_id:
            last_admin = AdminUser.objects.order_by('-admin_id').first()
            if last_admin:
                last_id = int(last_admin.admin_id.split('-')[1])
                new_id = 'ADM-'+str(last_id+1)
            else:
                new_id = 'ADM-1'
            self.admin_id = new_id
        super().save(*args,**kwargs)


class LibrarianUser(BaseAuthModel):
    
    GENDER_CHOICES = (
        ('M','Male'),
        ('F','Female')
    )
    
    class Meta:
        verbose_name = 'Librarian User',
        verbose_name_plural = 'Librarian Users'
        
    librarian_id = models.CharField(max_length=10, unique=True, editable=False)
    librarian_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
    
    def save(self,*args,**kwargs):
        if not self.librarian_id:
            last_librarian = LibrarianUser.objects.order_by('-librarian_id').first()
            if last_librarian:
                last_id = int(last_librarian.librarian_id.split('-')[1])
                new_id = 'LBY-'+str(last_id+1)
            else:
                new_id = 'LBY-1'
            self.librarian_id = new_id
        super().save(*args,**kwargs)

class MemberUser(BaseAuthModel):
    
    GENDER_CHOICES = (
        ('M','Male'),
        ('F','Female')
    )
    MEMEBER_TYPE = (
        ('PEM','premium'),
        ('REG','regular')
    )
    member_id = models.CharField(max_length=10, unique=True, editable=False)
    member_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    active = models.BooleanField(default=True)
    member_type = models.CharField(max_length=3,choices=MEMEBER_TYPE)
    
    
    def save(self, *args, **kwargs):
        if not self.member_id:
            last_member = MemberUser.objects.order_by('-member_id').first()
            if last_member:
                last_id = int(last_member.member_id.split('-')[1])
                new_id = 'MEM-'+str(last_id+1)
            else:
                new_id = 'MEM-1'
            self.member_id = new_id
        super().save(*args,**kwargs)
        