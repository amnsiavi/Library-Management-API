from django.db import models
from Users.models import MemberUser
from datetime import datetime
# Create your models here.

class LibraryModel(models.Model):
    GENERES = (
        ('Action', 'Action'),
        ('Adventure', 'Adventure'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Fantasy', 'Fantasy'),
        ('Horror', 'Horror'),
        ('Mystery', 'Mystery'),
        ('Romance', 'Romance'),
        ('Sci-Fi', 'Sci-Fi'),
        ('Thriller', 'Thriller'),
        ('Western', 'Western'),
        ('Crime','Crime'),
    )
    #title, author(s), ISBN, genre publication year, quantity
    title = models.CharField(max_length=100)
    synopsis = models.TextField()
    author = models.CharField(max_length=50)
    genre = models.CharField(max_length=10,choices=GENERES)
    publication_year = models.DateField(null=True,blank=True)
    quantity = models.PositiveIntegerField(default=0)
    ISBN = models.CharField(max_length=10,unique=True,editable=False)
    avaliable = models.BooleanField(default=True)
   
    
    
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        if not self.ISBN:
            last_ISBN = LibraryModel.objects.order_by('-ISBN').first()
            if last_ISBN:
                last_id = int(last_ISBN.ISBN.split('-')[1])
                new_id = 'ISBN-'+str(last_id+1)
            else:
                new_id = 'ISBN-1'
            self.ISBN = new_id
        super().save(*args,**kwargs)
    
class Book_Issue(models.Model):
    
    books = models.ForeignKey(LibraryModel,on_delete=models.CASCADE)
    member = models.ForeignKey(MemberUser,on_delete=models.CASCADE)
    issue_date = models.DateField(default = datetime.now())
    return_date = models.DateField(null=True, blank=True)
    returned = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.member)
    