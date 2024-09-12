from django.db import models

class Book(models.Model):
    book_id = models.CharField(max_length=10,primary_key=True)
    book_name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    count = models.IntegerField()
    rack = models.CharField(max_length=50)
    shelf = models.CharField(max_length=50)

    def __str__(self):
        return self.book_id
    
    
class Faculty(models.Model):
    name = models.CharField(max_length=200)
    id_number = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100 ,default="null")
    books_borrowed = models.ManyToManyField('Book', blank=True, related_name='borrowers')
    is_first_login = models.BooleanField(default=True)

    def __str__(self):
        return self.name